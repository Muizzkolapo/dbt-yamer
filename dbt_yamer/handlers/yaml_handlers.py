import yaml

class MyDumper(yaml.Dumper):
    """
    A custom YAML dumper that overrides the increase_indent and write_line_break methods
    to produce extra line breaks after top-level items.
    """

    def increase_indent(self, flow=False, indentless=False):
        """Always set 'indentless' to False to ensure proper indentation of nested blocks."""
        return super(MyDumper, self).increase_indent(flow, False)

    def write_line_break(self, data=None):
        """
        Override to add an extra line break after the top-level indentation.
        (Here, we check if len(self.indents) == 4 to control when to add the extra line.)
        """
        super(MyDumper, self).write_line_break(data)
        if len(self.indents) == 4:
            super(MyDumper, self).write_line_break()

def format_columns(columns):
    """
    Apply specific formatting to the columns list.
    """
    return [
        {
            'name': column['name'],
            'data_type': column['data_type'],
            'description': column.get('description', '')
        }
        for column in columns
    ]

def format_yaml2(input_yaml: str) -> str:
    """
    Alternate version of format function, demonstrating a second approach.
    Loads the YAML, applies column formatting, dumps with custom indentation,
    then adds a blank line after 'version: 2' if present.
    """
    data = yaml.safe_load(input_yaml)

    for model in data.get('models', []):
        if 'columns' in model:
            model['columns'] = format_columns(model['columns'])

    formatted = yaml.dump(data, Dumper=MyDumper, sort_keys=False)
    formatted = formatted.replace("version: 2\n", "version: 2\n\n")
    return formatted

def format_yaml(input_yaml: str) -> str:
    """
    Reformats the input YAML to match the desired structure with separate formatting
    for headers and columns, using a custom dumper to handle indentation and spacing.
    """
    data = yaml.safe_load(input_yaml)

    for model in data.get('models', []):
        if 'columns' in model:
            model['columns'] = format_columns(model['columns'])

    # Dump the YAML with adjusted formatting
    formatted_yaml = yaml.dump(data, Dumper=MyDumper, sort_keys=False)

    # Remove extra spacing in 'config' section if it appears double-spaced
    formatted_yaml = formatted_yaml.replace("  config:\n\n", "  config:\n")

    # Add an empty line after "version: 2"
    formatted_yaml = formatted_yaml.replace("version: 2\n", "version: 2\n\n")

    # Remove the newline immediately after "columns:"
    formatted_yaml = formatted_yaml.replace("columns:\n", "columns:")

    return formatted_yaml
