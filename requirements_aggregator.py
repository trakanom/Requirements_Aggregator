# ./requirements_aggregator.py

"""
Requirements Aggregator

This script scans for requirements.txt files inside imported directories 
and combines their content into a single unified requirements.txt file. 
It provides a mapping of packages to directories and highlights overlapping requirements.

Usage:
    Run the script and provide the root directory to start scanning.
"""

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
    if depth < 0:
        return []

    requirements_files = []
    for root, _, files in os.walk(base_dir):
        if "requirements.txt" in files:
            requirements_files.append(os.path.join(root, "requirements.txt"))
        for _ in root.split(os.sep):
            depth -= 1

    return requirements_files


def aggregate_requirements(requirements_files):
    """
    Aggregate content of multiple requirements.txt files.

    Parameters:
    - requirements_files (list): List of paths to requirements.txt files.

    Returns:
    - dict: A dictionary with packages as keys and directories as values.
    """
    aggregated_data = {}
    for req_file in requirements_files:
        with open(req_file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    if line in aggregated_data:
                        aggregated_data[line].append(os.path.dirname(req_file))
                    else:
                        aggregated_data[line] = [os.path.dirname(req_file)]
    return aggregated_data


def main():
    base_dir = input("Enter the root directory to start scanning: ")
    depth = int(input("Enter the search depth (default 2): ") or 2)

    requirements_files = find_requirements_files(base_dir, depth)
    aggregated_data = aggregate_requirements(requirements_files)

    with open("combined_requirements.txt", "w") as out:
        for pkg, dirs in aggregated_data.items():
            if len(dirs) > 1:
                out.write(f"# {pkg} is required in: {', '.join(dirs)}\n")
                out.write(f"#{pkg}\n")
            else:
                out.write(f"# {pkg} is required in: {dirs[0]}\n")
                out.write(f"{pkg}\n")

    print(
        "Combined requirements.txt file has been generated as 'combined_requirements.txt'."
    )


if __name__ == "__main__":
    main()
