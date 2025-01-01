import click
import subprocess
import shlex

@click.command()
@click.argument("models", nargs=-1)
def run(models):
    """
    Run one or more dbt models.

    Example:
      dbt-yamer run n model_a
    """
    if not models:
        click.echo("No model names provided. Please specify at least one model to run.")
        return

    cmd_list = ["dbt", "run", "--select"] + list(models)


    try:
        subprocess.run(cmd_list, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running dbt models: {e}")
        raise click.Abort()
