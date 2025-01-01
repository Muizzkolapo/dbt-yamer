# dbt-yamer

## Overview
`dbt-yamer` is a Python wrapper for dbt designed to enhance the management of dbt projects by automating YAML generation for dbt models. It provides a CLI tool for creating YAML schema files with integrated support for dbt documentation blocks, ensuring consistency and improving developer productivity.

### Key Features
- Automates YAML schema generation for dbt models.
- Integrates doc blocks directly into column descriptions.
- Supports fuzzy matching to map columns to the best documentation blocks.
- CLI tool for seamless usage.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

### Installing `dbt-yamer`
```bash
pip install dbt-yamer
```

## Usage

### Command Line Interface (CLI)
The primary interface for `dbt-yamer` is through the CLI.

#### Generate YAML Files
Generate YAML schema files for one or more dbt models:
```bash
dbt-yamer generate-yaml <model_name1> <model_name2>
```

#### Example
To generate YAML for a model named `customer_data`, run:
```bash
dbt-yamer generate-yaml customer_data
```

#### Usage Examples
With this updated code, your CLI command can be used as follows:

```bash
# By default, loads manifest from target/manifest.json
dbt-yamer generate-yaml -m model_a model_b

# Specifying a custom manifest path
dbt-yamer generate-yaml --manifest path/to/another_manifest.json -m model_a

# Specifying a custom target label (dbt's "target" as in --target <env>)
dbt-yamer generate-yaml -t uat -m model_a

# A combination of manifest, target, and multiple models
dbt-yamer generate-yaml --manifest path/to/another_manifest.json -t uat -m model_a -m model_b
```

- `--manifest` defaults to `target/manifest.json`.
- `--target`/`-t` defaults to `models/schema.yml`, but also can be overridden (e.g., `-t uat`).
- `--models`/`-m` requires at least one model name, and you can pass in multiple.

### Output
- YAML schema files are created in the same directory as their corresponding `.sql` files.
- If a schema file already exists, new files are versioned with `_v1`, `_v2`, etc.
- Doc blocks are automatically added to column descriptions in the format:
  ```yaml
  description: "{{ doc('doc_block_name') }}"
  ```

## Development

### Setting Up
Clone the repository and install dependencies:
```bash
git clone <repository-url>
cd dbt-yamer
pip install -e .
```

### Running Tests
Run the test suite to verify functionality:
```bash
pytest
```

## Contributing
We welcome contributions to `dbt-yamer`! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and write tests.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Support
For issues and feature requests, please create an issue in the [GitHub repository](<repository-url>/issues).


## Authors
- [Muizz Lateef](mailto:lateefmuizz@gmail.com)

