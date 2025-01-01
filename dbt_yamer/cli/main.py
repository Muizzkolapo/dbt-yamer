import click
from dbt_yamer.cli.run import run
from dbt_yamer.cli.generate_yaml import generate_yaml

@click.group()
def cli():
    """
    dbt-yamer CLI

    Use this tool to:
      - Run dbt models
      - Generate YAML configs (with contract enforcement)
    """
    pass

cli.add_command(run)
cli.add_command(generate_yaml)

if __name__ == "__main__":
    cli()
