# dbt-yamer

## Overview

`dbt-yamer` is a Python wrapper designed to simplify and enhance the generation of YAML schema files for dbt projects. With a focus on faster schema YAML and doc block generation, dbt-yamer aids development and helps avoid documentation and contract technical debt. By leveraging this CLI tool built on the dbt context, developers can streamline the management of dbt models and associated metadata.

### Key Features

- Automates YAML schema generation for dbt models.
- Integrates doc blocks directly into column descriptions.
- Supports fuzzy matching to map columns to the best documentation blocks.
- CLI tool for seamless usage.

## Installation

### Prerequisites

Ensure you have the following prerequisites:

- Python 3.8 or higher
- pip (Python package installer)
- dbt
- A working dbt project

### Installing `dbt-yamer`

```bash
pip install dbt-yamer
```

## Usage

### Command Line Interface (CLI)

The primary interface for `dbt-yamer` is through the CLI.

#### Generate YAML Files

Generate YAML schema files for one or more dbt models using the `dbt-yamer yaml -m` or `--models` switch:

```bash
dbt-yamer yaml -m <model_name1> <model_name2>
```

### Example

To generate YAML for a model named `customer_data`, run:

```bash
dbt-yamer yaml -m customer_data
```

This command will generate a YAML schema file for the `customer_data` model, including:

- Column definitions with descriptions.
- Automatically integrated doc blocks for relevant columns.
- Fuzzy-matched documentation for improved accuracy.

#### Usage Examples

With this updated code, your CLI command can be used as follows:

```bash
# By default, loads manifest from target/manifest.json
dbt-yamer yaml -m model_a model_b

# Specifying a custom manifest path
dbt-yamer yaml -m model_a --manifest path/to/another_manifest.json

# Specifying a custom target label (dbt's "target" as in --target <env>)
dbt-yamer yaml -m model_a -t uat

# A combination of manifest, target, and multiple models
dbt-yamer yaml -m model_a -m model_b --manifest path/to/another_manifest.json -t uat
```

- `--manifest` defaults to `target/manifest.json`.
- `--target`/`-t` defaults to local environment, but also can be overridden (e.g., `-t uat`).
- `--models`/`-m` requires at least one model name, and you can pass in multiple.

### Output

- YAML schema files are created in the same directory as their corresponding `.sql` files.
- If a schema file already exists, new files are versioned with `_v1`, `_v2`, etc.
- Doc blocks are automatically added to column descriptions in the format:
  ```yaml
  description: "{{ doc('doc_block_name') }}"
  ```

## Development and Contributing

### Development Environment Setup

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd dbt-yamer
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Development Dependencies**

   Instead of `pytest`, the project uses Makefile commands for setup and testing. Use the following commands:

   **To Clean and Restart the Environment**:

   ```bash
   make clean restart
   ```

   This will clean up any existing environment and install the package along with its dependencies.

4. **Run Makefile Commands**

   Use the provided Makefile for various tasks. For example:

   - `make restart`: Reinstalls the package.
   - `make clean`: Removes temporary files and builds.

### Contributing Guidelines

1. **Feature Development**:

   - Create a new branch for your feature or bug fix.

     ```bash
     git checkout -b feature/your-feature-name
     ```

2. **Adhere to Code Standards**:

   - Follow PEP 8 guidelines.
   - Use type hints where applicable.
   - Run `pylint` to ensure code quality.

3. **Submit a Pull Request**:

   - Push your branch to the repository.

     ```bash
     git push origin feature/your-feature-name
     ```

   - Open a pull request with a clear description of your changes.

## Support

For issues and feature requests, please create an issue in the dbt-yamer  [GitHub repository](https://github.com/Muizzkolapo/dbt-yamer/issues).

## Authors

- [Muizz Lateef](mailto:lateefmuizz@gmail.com)  
  [https://muizzkolapo.github.io/blog/](https://muizzkolapo.github.io/blog/)
  
