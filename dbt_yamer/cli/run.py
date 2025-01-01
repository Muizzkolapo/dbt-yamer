import click
from dbt_yamer.utils.subprocess_utils import run_subprocess

@click.command()
@click.argument("models", nargs=-1)
def run(models):
    """
    Run one or more dbt models.

    Example:
      dbt-yamer run model_a
    """
    if not models:
        click.echo("No model names provided. Please specify at least one model to run.")
        return

    cmd_list = ["dbt", "run", "--select"] + list(models)

    for model in models:
        click.echo(f"Generating YAML for model: {model}")

    try:
        result = run_subprocess(cmd_list, capture_output=True)
        # Process result if needed
    except RuntimeError as e:
        click.echo(f"Command execution failed: {e}")
        raise click.Abort()
