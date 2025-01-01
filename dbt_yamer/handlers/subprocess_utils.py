import subprocess
import click
def run_command(cmd_list):
    """
    Run a subprocess command and return the output.
    """
    try:
        result = subprocess.run(
            cmd_list,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise click.ClickException(f"Command failed: {e}") from e
