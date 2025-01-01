import json
import sys
from fuzzywuzzy import fuzz

def load_manifest(manifest_path: str) -> dict:
    """
    Loads the dbt manifest JSON file and returns it as a Python dictionary.
    """
    try:
        with open(manifest_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Manifest file '{manifest_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON. {e}")
        sys.exit(1)


def extract_doc_block_names(docs: dict) -> list:
    """
    Extracts the names of all 'doc.' blocks from the manifest.

    :param docs: Dictionary of doc blocks from the manifest.
    :return: List of doc block names.
    """
    return [doc_info["name"] for key, doc_info in docs.items() if key.startswith("doc.")]


def find_best_match(target_name: str, doc_block_names: list) -> str | None:
    """
    Uses fuzzy string matching to find the best match for a column name in the doc block names.
    Returns the best matching name if score > 80%, otherwise returns None.

    Args:
        target_name: The name to match.
        doc_block_names: List of doc block names.
    Returns:
        str | None: The name of the best matching doc block or None if no good match found.
    """
    best_match = None
    best_ratio = 0.0
    
    for doc_name in doc_block_names:
        ratio = fuzz.ratio(target_name.lower(), doc_name.lower())
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = doc_name
    
    # Return best match only if it's above 80% confidence
    if best_match and (best_ratio > 80):
        return best_match
    
    return None


def apply_doc_blocks(model_yaml: dict, manifest_data: dict) -> dict:
    """
    Apply doc blocks to model YAML. Leave description empty if no good match is found.
    """
    doc_block_names = extract_doc_block_names(manifest_data)
    
    # If the model has columns defined
    if 'columns' in model_yaml:
        for column in model_yaml['columns']:
            column_name = column['name']
            best_match = find_best_match(column_name, doc_block_names)
            
            if best_match and best_match in manifest_data['docs']:
                column['description'] = manifest_data['docs'][best_match]['block_contents']
            else:
                column['description'] = ''
    
    return model_yaml


def main():
    if len(sys.argv) != 3:
        print("Usage: python fuzzy_match_doc_blocks.py <path_to_manifest.json> <column_name>")
        sys.exit(1)

    manifest_path = sys.argv[1]
    column_name = sys.argv[2]

    print(f"Loading manifest from: {manifest_path}")
    manifest = load_manifest(manifest_path)

    docs = manifest.get("docs", {})
    if not docs:
        print("No 'docs' found in the manifest file.")
        sys.exit(1)

    print("Extracting doc block names...")
    doc_block_names = extract_doc_block_names(docs)

    print("Finding the best match for column name...")
    best_match = find_best_match(column_name, doc_block_names)

    if best_match:
        print("\nBest match found:")
        print(f"  Doc Block Name: {best_match}")
    else:
        print(f"No matching doc block found for column name '{column_name}'.")


if __name__ == "__main__":
    main()