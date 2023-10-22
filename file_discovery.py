# ./file_discovery.py

import os


def find_requirements_files(base_dir, depth):
    """
    Recursively find all requirements.txt files up to a specified depth.

    Parameters:
    - base_dir (str): The directory to start the search from.
    - depth (int): How deep to search for requirements.txt files.

    Returns:
    - list: A list of paths to found requirements.txt files.
    """
    requirements_files = []
    count = 0

    for root, _, files in os.walk(base_dir):
        if "requirements.txt" in files:
            requirements_files.append(os.path.join(root, "requirements.txt"))
        for _ in root.split(os.sep):
            depth -= 1
        count += 1
        # Display progress without spamming the console
        if count % 50 == 0:
            print(f"Scanned {count} directories...")

    print(
        f"Finished scanning! Found {len(requirements_files)} requirements.txt files in {count} directories."
    )
    return requirements_files


def aggregate_requirements(requirements_files, base_dir):
    """
    Aggregate content of multiple requirements.txt files.

    Parameters:
    - requirements_files (list): List of paths to requirements.txt files.
    - base_dir (str): The base directory from where the relative paths will be determined.

    Returns:
    - dict: A dictionary with packages as keys and directories as values.
    """
    aggregated_data = {}
    for req_file in requirements_files:
        relative_path = os.path.relpath(os.path.dirname(req_file), base_dir)
        with open(req_file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    if line in aggregated_data:
                        aggregated_data[line].append(relative_path)
                    else:
                        aggregated_data[line] = [relative_path]
    return aggregated_data
