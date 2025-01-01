import subprocess
from typing import List, Optional

def run_subprocess(cmd_list: List[str], capture_output: bool = False) -> Optional[subprocess.CompletedProcess]:
    """
    Executes a subprocess command and handles errors consistently.
    
    Args:
        cmd_list: List of command arguments
        capture_output: Whether to capture and return command output
    
    Returns:
        CompletedProcess if capture_output is True, None otherwise
    """
    try:
        if capture_output:
            return subprocess.run(
                cmd_list,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            subprocess.run(cmd_list, check=True)
            return None
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {' '.join(cmd_list)}\n{str(e)}") 