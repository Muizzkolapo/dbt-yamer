import click
from pathlib import Path
import subprocess
import tempfile
import shutil
from dbt_yamer.handlers.markdown_handlers import create_md_file
from dbt_yamer.handlers.file_handlers import find_dbt_project_root
from dbt_yamer.handlers.docblock import load_manifest
from dbt_yamer.macros.macro_content import generate_yaml_macro

def generate_yaml_for_model(model, target=None):
    """Helper function to generate YAML for a single model"""
    try:
        ls_cmd = [
            "dbt",
            "--quiet",
            "ls",
            "--resource-types", "model",
            "--select", model,
            "--output", "path"
        ]
        
        ls_result = subprocess.run(
            ls_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        paths = ls_result.stdout.strip().splitlines()
        if not paths:
            click.echo(f"⚠️  Warning: Could not find .sql path for '{model}' (dbt ls returned no results).")
            return None, None

        sql_file_path = Path(paths[0])
        dir_for_sql = sql_file_path.parent

        args_dict_str = f'{{"model_names": ["{model}"]}}'
        cmd_list = [
            "dbt",
            "--quiet",
            "run-operation",
            "dbt_yamer_generate_contract_yaml",
            "--args", args_dict_str
        ]
        if target:
            cmd_list.extend(["-t", target])

        result = subprocess.run(
            cmd_list,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        raw_yaml_output = result.stdout.strip()
        if not raw_yaml_output:
            click.echo(f"⚠️  No YAML output returned by dbt for '{model}'.")
            return None, None

        return dir_for_sql, raw_yaml_output

    except subprocess.CalledProcessError as e:
        click.echo(f"⚠️  Error generating YAML for '{model}':\n{e.stderr}")
        return None, None
    except Exception as e:
        click.echo(f"⚠️  Unexpected error generating YAML for '{model}': {str(e)}")
        return None, None

def generate_md_for_model(model, project_dir):
    """Helper function to generate markdown for a single model"""
    try:
        ls_cmd = [
            "dbt",
            "--quiet",
            "ls",
            "--resource-types", "model",
            "--select", model,
            "--output", "path"
        ]
        
        ls_result = subprocess.run(
            ls_cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        paths = ls_result.stdout.strip().splitlines()
        if not paths:
            click.echo(f"⚠️  Warning: Could not find path for '{model}' (dbt ls returned no results).")
            return False

        sql_file_path = Path(paths[0])
        dir_for_sql = sql_file_path.parent
        
        create_md_file(model, dir_for_sql)
        click.echo(f"✅ Markdown documentation generated for '{model}'")
        return True

    except subprocess.CalledProcessError as e:
        click.echo(f"⚠️  Error generating markdown for '{model}':\n{e.stderr}")
        return False
    except Exception as e:
        click.echo(f"⚠️  Unexpected error generating markdown for '{model}': {str(e)}")
        return False

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

    try:
        project_dir = find_dbt_project_root()
    except FileNotFoundError as e:
        click.echo(f"Error: {e}. Please run this command from within a dbt project.")
        return

    # Track overall success
    yaml_success = []
    md_success = []

    # First generate YAML files
    click.echo("\n🔄 Generating YAML files...")
    
    manifest_data = load_manifest(manifest)
    if not manifest_data:
        click.echo("⚠️  Could not load manifest. Skipping YAML generation but will attempt markdown generation.")
    else:
        with tempfile.TemporaryDirectory() as temp_macros_dir:
            temp_macros_path = Path(temp_macros_dir) / "tmp_dbt_yammer_dbt_yamer_generate_yaml_macro.sql"
            try:
                with open(temp_macros_path, "w", encoding="utf-8") as f:
                    f.write(generate_yaml_macro)
            except OSError as e:
                click.echo(f"⚠️  Failed to write temporary macros: {e}")
                manifest_data = None

            if manifest_data:
                user_macros_dir = project_dir / "macros"
                if not user_macros_dir.exists():
                    user_macros_dir.mkdir(parents=True)

                temp_macro_filename = "tmp_dbt_yammer_dbt_yamer_generate_yaml_macro.sql"
                destination_macro_path = user_macros_dir / temp_macro_filename
                
                try:
                    shutil.copy(temp_macros_path, destination_macro_path)
                    
                    for model in models:
                        dir_for_sql, raw_yaml_output = generate_yaml_for_model(
                            model, manifest_data, project_dir, target
                        )
                        if dir_for_sql and raw_yaml_output:
                            yaml_success.append(model)
                
                finally:
                    if destination_macro_path.exists():
                        destination_macro_path.unlink()

    # Then generate markdown files
    click.echo("\n🔄 Generating markdown documentation...")
    for model in models:
        if generate_md_for_model(model, project_dir):
            md_success.append(model)

    # Summary
    click.echo("\n📊 Generation Summary:")
    if yaml_success:
        click.echo(f"✅ YAML generated successfully for: {', '.join(yaml_success)}")
    else:
        click.echo("❌ No YAML files were generated successfully")
    
    if md_success:
        click.echo(f"✅ Markdown generated successfully for: {', '.join(md_success)}")
    else:
        click.echo("❌ No markdown files were generated successfully")

    # Models that failed both
    failed_both = set(models) - (set(yaml_success) | set(md_success))
    if failed_both:
        click.echo(f"\n⚠️  Complete failures (neither YAML nor markdown generated): {', '.join(failed_both)}")
