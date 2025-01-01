from pathlib import Path


def get_unique_yaml_path(dir_path: Path, base_name: str) -> tuple[Path, str]:
    """
    Return a tuple of (file_path, versioned_name) where:
    - file_path is of the form dir_path/base_name.yml
    - versioned_name is either base_name or base_name_v{n}
    If base_name.yml exists, try base_name_v1.yml, _v2, etc.
    """
    candidate = dir_path / f"{base_name}.yml"
    if not candidate.exists():
        return candidate, base_name

    version_num = 1
    while True:
        versioned_name = f"{base_name}_v{version_num}"
        candidate = dir_path / f"{versioned_name}.yml"
        if not candidate.exists():
            return candidate, versioned_name
        version_num += 1


def find_dbt_project_root() -> Path:
    """
    Find the dbt project root by looking for dbt_project.yml in current and parent directories.
    Raises FileNotFoundError if no dbt project root is found.
    """
    current = Path(".").resolve()
    
    # Look in current and parent directories
    while current != current.parent:
        if (current / "dbt_project.yml").exists():
            return current
        current = current.parent
    
    raise FileNotFoundError("Could not find dbt_project.yml in current or parent directories")