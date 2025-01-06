import click
from pathlib import Path
import subprocess
from dbt_yamer.handlers.markdown_handlers import create_md_file
from dbt_yamer.handlers.file_handlers import find_dbt_project_root

@click.command(name="md")
@click.option(
    "--model",
    "-m",
    required=True,
    help="Model name to generate markdown documentation for."
)
def generate_markdown(model):
    """
    Generate markdown documentation for a dbt model and place it next to its .sql source.

    Example:
      dbt-yamer md -m model_name
      dbt-yamer md --model model_name
    """
    click.echo(f"Generating markdown for model: {model}")

    try:
        project_dir = find_dbt_project_root()
    except FileNotFoundError as e:
        click.echo(f"Error: {e}. Please run this command from within a dbt project.")
        return

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
        click.echo(f"Unable to locate model '{model}':\n{e.stderr}")
        return

    paths = ls_result.stdout.strip().splitlines()
    if not paths:
        click.echo(f"Warning: Could not find path for '{model}' (dbt ls returned no results).")
        return

    sql_file_path = Path(paths[0])
    dir_for_sql = sql_file_path.parent
    
    try:
        create_md_file(model, dir_for_sql)
    except OSError as e:
        click.echo(f"Could not write markdown file for '{model}': {e}") 