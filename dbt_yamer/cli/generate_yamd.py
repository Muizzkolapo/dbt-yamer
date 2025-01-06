import click
from pathlib import Path
from dbt_yamer.handlers.markdown_handlers import create_md_file
from dbt_yamer.handlers.file_handlers import find_dbt_project_root
import subprocess
from dbt_yamer.handlers.yaml_handlers import format_yaml
from dbt_yamer.doc_handler.docblock import load_manifest, extract_doc_block_names, find_best_match, extract_column_doc
from dbt_yamer.macros.macro_content import generate_yaml_macro
from dbt_yamer.handlers.file_handlers import get_unique_yaml_path
import tempfile
import shutil

@click.command(name="yamd")
@click.option(
    "--manifest",
    default="target/manifest.json",
    show_default=True,
    help="Path to the dbt manifest JSON file."
)
@click.option(
    "--target",
    "-t",
    default=None,
    help="Specify a target (e.g., uat) if the table already exists in a remote environment."
)
@click.option(
    "--models",
    "-m",
    multiple=True,
    required=True,
    help="One or more model names to generate YAML and markdown for."
)
def generate_yamd(models, manifest, target):
    """
    Generate both YAML and markdown documentation for one or more dbt models.

    Example:
      dbt-yamer yamd -m model_a -m model_b
      dbt-yamer yamd -t uat -m model_a
    """
    if not models:
        click.echo("No model names provided. Please specify at least one model using --models/-m.")
        return

    # First generate YAML files
    click.echo("Generating YAML files...")
    
    manifest_data = load_manifest(manifest)
    if not manifest_data:
        click.echo(f"Could not load manifest at: {manifest}")
        return

    docs = manifest_data.get("docs", {})
    doc_block_names = extract_doc_block_names(docs)
    wrote_any_files = False

    with tempfile.TemporaryDirectory() as temp_macros_dir:
        temp_macros_path = Path(temp_macros_dir) / "tmp_dbt_yammer_dbt_yamer_generate_yaml_macro.sql"
        try:
            with open(temp_macros_path, "w", encoding="utf-8") as f:
                f.write(generate_yaml_macro)
        except OSError as e:
            click.echo(f"Failed to write temporary macros: {e}")
            return

        try:
            project_dir = find_dbt_project_root()
        except FileNotFoundError as e:
            click.echo(f"Error: {e}. Please run this command from within a dbt project.")
            return

        user_macros_dir = project_dir / "macros"
        if not user_macros_dir.exists():
            user_macros_dir.mkdir(parents=True)

        temp_macro_filename = "tmp_dbt_yammer_dbt_yamer_generate_yaml_macro.sql"
        destination_macro_path = user_macros_dir / temp_macro_filename
        
        try:
            shutil.copy(temp_macros_path, destination_macro_path)
        except OSError as e:
            click.echo(f"Failed to copy temporary macros to the project: {e}")
            return

        try:
            # Process each model
            for model in models:
                # ... [YAML generation code from generate_yaml.py] ...
                # (Copy the model processing loop from generate_yaml.py here)
                pass

        finally:
            try:
                if destination_macro_path.exists():
                    destination_macro_path.unlink()
            except OSError as e:
                click.echo(f"Failed to remove temporary macros: {e}")

    # Then generate markdown files
    click.echo("\nGenerating markdown documentation...")
    
    for model in models:
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
            continue

        paths = ls_result.stdout.strip().splitlines()
        if not paths:
            click.echo(f"Warning: Could not find path for '{model}' (dbt ls returned no results).")
            continue

        sql_file_path = Path(paths[0])
        dir_for_sql = sql_file_path.parent
        
        try:
            create_md_file(model, dir_for_sql)
            click.echo(f"✅ Markdown documentation generated for '{model}'")
        except OSError as e:
            click.echo(f"❌ Could not write markdown file for '{model}': {e}")
