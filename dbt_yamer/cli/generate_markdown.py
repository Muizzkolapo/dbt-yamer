import click
from pathlib import Path
import subprocess
from dbt_yamer.handlers.markdown_handlers import create_md_file
from dbt_yamer.handlers.file_handlers import find_dbt_project_root

@click.command(name="md")
@click.option(
    "--models",
    "-m",
    multiple=True,
    required=True,
    help="One or more model names to generate markdown documentation for."
)
def generate_markdown(models):
    """
    Generate markdown documentation for one or more dbt models and place them next to their .sql sources.

    Example:
      dbt-yamer md -m model_a -m model_b
      dbt-yamer md --models model_name
    """
    if not models:
        click.echo("No model names provided. Please specify at least one model using --models/-m.")
        return

    # Track successful generations
    md_success = []

    click.echo("\n🔄 Generating markdown documentation...")

    try:
        project_dir = find_dbt_project_root()
    except FileNotFoundError as e:
        click.echo(f"Error: {e}. Please run this command from within a dbt project.")
        return

    for model in models:
        click.echo(f"\nProcessing model: {model}")
        
        ls_cmd = [
            "dbt",
            "--quiet",
            "ls",
            "--resource-types", "model",
            "--select", model,
            "--output", "path"
        ]
        
        try:
            ls_result = subprocess.run(
                ls_cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Unable to locate model '{model}':\n{e.stderr}")
            continue

        paths = ls_result.stdout.strip().splitlines()
        if not paths:
            click.echo(f"⚠️  Warning: Could not find path for '{model}' (dbt ls returned no results).")
            continue

        sql_file_path = Path(paths[0])
        dir_for_sql = sql_file_path.parent
        
        try:
            create_md_file(model, dir_for_sql)
            md_success.append(model)
            click.echo(f"✅ Markdown documentation generated for '{model}'")
        except OSError as e:
            click.echo(f"❌ Could not write markdown file for '{model}': {e}")

    # Summary
    click.echo("\n📊 Generation Summary:")
    if md_success:
        click.echo(f"✅ Markdown generated successfully for: {', '.join(md_success)}")
    else:
        click.echo("❌ No markdown files were generated successfully")

    # Failed models
    failed_models = set(models) - set(md_success)
    if failed_models:
        click.echo(f"\n⚠️  Failed to generate markdown for: {', '.join(failed_models)}") 