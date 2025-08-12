import click
from dbt_yamer.utils.subprocess_utils import run_subprocess

@click.command()
@click.option(
    "--select",
    "-s",
    multiple=True,
    help="Specify models to run using dbt's node selection syntax (supports tag selectors, e.g., tag:nightly)"
)
@click.option(
    "--exclude",
    "-e",
    multiple=True,
    help="Specify models to exclude using dbt's node selection syntax"
)
@click.option(
    "--target",
    "-t",
    default=None,
    help="Specify the target profile to run against"
)
def run(select, exclude, target):
    """
    Run one or more dbt models using dbt-style selection syntax.

    Example:
      dbt-yamer run -s model_a model_b
      dbt-yamer run --select tag:nightly
      dbt-yamer run -s model_a -e model_b
      dbt-yamer run -s model_a -t prod
    """
    if not select:
        click.echo("No selection criteria provided. Please specify models using --select/-s.")
        return

    cmd_list = ["dbt", "run"]

    # Validate and add select criteria
    for selector in select:
        if '+' in selector:
            click.echo(f"Error: '+' selector is not supported: {selector}")
            return
        cmd_list.extend(["--select", selector])

    # Add exclude criteria
    for exclusion in exclude:
        if '+' in exclusion:
            click.echo(f"Error: '+' selector is not supported in exclusions: {exclusion}")
            return
        cmd_list.extend(["--exclude", exclusion])

    # Add target if specified
    if target:
        cmd_list.extend(["--target", target])

    try:
        run_subprocess(cmd_list)
    except RuntimeError as e:
        click.echo(f"Error running dbt models: {e}")
        raise click.Abort()
