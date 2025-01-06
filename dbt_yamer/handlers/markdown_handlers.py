def create_md_file(model_name: str, path: str) -> None:
    """
    Creates a markdown file for a given model and stores it in the given path.
    
    Args:
        model_name: Name of the model
        path: Path where the markdown file will be stored
    """
    model_name = model_name.split('.', 1)[0]
    
    lines = [
        f'{{% docs {model_name} %}}',
        '## Overview',
        '###### Resources:',
        '### Unique Key:',
        '### Partitioned by:',
        '### Contains PII:',
        '### Sources:',
        '### Granularity:',
        '### Update Frequency:',
        '',
        '{% enddocs %}'
    ]
    
    md_path = path / f"{model_name}.md"
    with open(md_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(f"{line}\n\n")
    
    print(f"✅ Markdown file created: {md_path}") 