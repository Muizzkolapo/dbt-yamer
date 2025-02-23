import click
import subprocess
import yaml
from pathlib import Path
import tempfile
import shutil
from dbt_yamer.handlers.yaml_handlers import format_yaml
from dbt_yamer.handlers.docblock import load_manifest, extract_doc_block_names, find_best_match, extract_column_doc
from dbt_yamer.macros.macro_content import generate_yaml_macro
from dbt_yamer.handlers.file_handlers import get_unique_yaml_path, find_dbt_project_root


@click.command(name="yaml")
@click.option(
    "--select",
    "-s",
    is_flag=True,
    help="Use this flag before specifying models"
)
@click.argument('models', nargs=-1)
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
def generate_yaml(select, models, manifest, target):
    """
    Generate YAML schema files for one or more dbt models.

    Example:
      dbt-yamer yaml -s dim_promotion dim_voucher
      dbt-yamer yaml --select tag:nightly
      dbt-yamer yaml -s dim_promotion tag:nightly -t uat
    """
    if not select:
        click.echo("Please use --select/-s flag before specifying models.")
        return

    if not models:
        click.echo("No models specified. Please provide at least one model name.")
        return

    # Validate selectors (no '+' allowed)
    for model in models:
        if '+' in model:
            click.echo(f"Error: '+' selector is not supported: {model}")
            return

    # Track successful generations
    yaml_success = []
    
    click.echo("\n🔄 Generating YAML files...")

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
            # First, if we have a tag selector, get the list of models
            processed_models = []
            for model in models:
                if model.startswith('tag:'):
                    click.echo(f"\nExpanding tag selector: {model}")
                    ls_cmd = [
                        "dbt",
                        "--quiet",
                        "ls",
                        "--select", model
                    ]
                    try:
                        ls_result = subprocess.run(
                            ls_cmd,
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        # Split the fully qualified names and take the last part
                        tag_models = [
                            path.split('.')[-1] 
                            for path in ls_result.stdout.strip().splitlines()
                        ]
                        if not tag_models:
                            click.echo(f"Warning: No models found for tag selector '{model}'")
                            continue
                        processed_models.extend(tag_models)
                        click.echo(f"Found models for {model}: {', '.join(tag_models)}")
                    except subprocess.CalledProcessError as e:
                        click.echo(f"Error expanding tag selector '{model}':\n{e.stderr}")
                        continue
                else:
                    processed_models.append(model)

            if not processed_models:
                click.echo("No models found to process after expanding selectors.")
                return

            # Now process each model as before
            for model in processed_models:
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
                    click.echo(f"Unable to locate .sql for model '{model}':\n{e.stderr}")
                    continue

                paths = ls_result.stdout.strip().splitlines()
                if not paths:
                    click.echo(f"Warning: Could not find .sql path for '{model}' (dbt ls returned no results).")
                    continue

                sql_file_path = Path(paths[0])  # take the first if multiple
                dir_for_sql = sql_file_path.parent

                args_dict_str = f'{{"model_names": ["{model}"]}}'
                cmd_list = [
                    "dbt",
                    "--quiet",
                    "run-operation",
                    "--no-version-check",
                    "dbt_yamer_generate_contract_yaml",
                    "--args", args_dict_str
                ]
                if target:
                    cmd_list.extend(["-t", target])

                try:
                    result = subprocess.run(
                        cmd_list,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                except subprocess.CalledProcessError as e:
                    click.echo(f"Error generating YAML for model '{model}':\n{e.stderr}")
                    continue

                raw_yaml_output = result.stdout.strip()
                if not raw_yaml_output:
                    click.echo(
                        f"No YAML output returned by dbt for '{model}'. "
                        "Make sure the macro returns YAML, and that the model was run locally."
                    )
                    continue

                try:
                    parsed = yaml.safe_load(raw_yaml_output)
                except yaml.YAMLError as e:
                    click.echo(f"Failed to parse dbt's YAML output for '{model}'. Error:\n{e}")
                    continue

                if not parsed or "models" not in parsed:
                    click.echo(
                        f"The YAML structure is missing 'models' for '{model}'. "
                        "Check that your macro outputs 'version: 2' and 'models:'. "
                    )
                    continue

                all_models = parsed["models"]
                if not all_models:
                    click.echo(f"No 'models' were returned in the YAML for '{model}'.")
                    continue

                model_info = all_models[0]

                columns = model_info.get("columns") or []  
                columns_with_names = [(col, col.get("name")) for col in columns if col.get("name")]
                column_names = [col_name for _, col_name in columns_with_names]

                # First try to find exact column doc blocks
                best_doc_matches = {}
                for col_name in column_names:
                    # Try exact column doc block match first
                    col_doc_name = f"col_{model}_{col_name}"
                    if col_doc_name in doc_block_names:
                        best_doc_matches[col_name] = col_doc_name
                        continue
                    
                    # Try model-specific column match
                    model_col_doc = f"{model}_{col_name}"
                    if model_col_doc in doc_block_names:
                        best_doc_matches[col_name] = model_col_doc
                        continue
                    
                    # Try generic column match
                    generic_col_doc = f"col_{col_name}"
                    if generic_col_doc in doc_block_names:
                        best_doc_matches[col_name] = generic_col_doc
                        continue
                    
                    # If no specific matches found, try fuzzy matching
                    best_match = find_best_match(col_name, doc_block_names)
                    if best_match:
                        best_doc_matches[col_name] = best_match
                    else:
                        # If no match found, use the model's doc block as fallback
                        best_doc_matches[col_name] = ""

                # Apply the doc blocks to columns
                for col, col_name in columns_with_names:
                    doc_block = best_doc_matches.get(col_name)
                    if doc_block:
                        col["description"] = f'{{{{ doc("{doc_block}") }}}}'
                    else:
                        col.setdefault("description", "")
                        click.echo(f"Warning: No doc block found for column '{col_name}' in model '{model}'")

                if not columns:
                    click.echo(
                        f"Warning: Model '{model}' has 0 columns. "
                        f"Ensure you've run `dbt run --select {model}` so columns are discovered."
                    )
                    continue

                output_file, versioned_name = get_unique_yaml_path(dir_for_sql, model)

                model_info["name"] = versioned_name

                version_val = parsed.get("version", 2)
                single_model_yaml = {
                    "version": version_val,
                    "models": [model_info]
                }

                raw_single_yaml = yaml.dump(single_model_yaml, sort_keys=False)
                formatted_yaml = format_yaml(raw_single_yaml)

                try:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(formatted_yaml)
                    yaml_success.append(model)
                    click.echo(f"✅ YAML Generated for '{model}' (named '{versioned_name}') → {output_file}")
                except OSError as e:
                    click.echo(f"❌ Could not write file {output_file} for '{model}': {e}")

        finally:
            # -------------------------------------------------------------------
            # Clean up: Remove the temporary macro file from the user's macros directory
            # -------------------------------------------------------------------
            try:
                if destination_macro_path.exists():
                    destination_macro_path.unlink()
            except OSError as e:
                click.echo(f"Failed to remove temporary macros: {e}")

    # Summary
    click.echo("\n📊 Generation Summary:")
    if yaml_success:
        click.echo(f"✅ YAML generated successfully for: {', '.join(yaml_success)}")
    else:
        click.echo("❌ No YAML files were generated successfully")

    # Don't report tag selectors as failed models
    failed_models = set(processed_models) - set(yaml_success)
    if failed_models:
        click.echo(f"\n⚠️  Failed to generate YAML for: {', '.join(failed_models)}")
