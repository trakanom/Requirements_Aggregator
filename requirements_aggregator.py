# ./requirements_aggregator.py

"""
Requirements Aggregator with Dependency Matrix

This script scans for requirements.txt files inside imported directories 
and combines their content into a unified `combined_requirements.txt` file at the root of the specified directory. 
It provides a mapping of packages to directories and highlights overlapping requirements. 
Additionally, it generates a dependency matrix in the form of a `requirements_overview.txt`.

Usage:
    Run the script and provide the root directory to start scanning.
"""

import os
import csv


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


def aggregate_requirements(requirements_files, base_dir):
    """
    Aggregate content of multiple requirements.txt files and generate a dependency matrix.

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


def sanitize_path(path):
    """
    Remove terminal escape sequences from a string.

    Parameters:
    - path (str): The string to sanitize.

    Returns:
    - str: The sanitized string.
    """
    return "".join([char for char in path if ord(char) > 31 or ord(char) == 9])


def generate_dependency_matrix(aggregated_data, base_dir):
    """
    Generate a dependency matrix in CSV format showing the relationship between directories and packages.

    Parameters:
    - aggregated_data (dict): Data containing packages and their associated directories.
    - base_dir (str): The base directory where the output file will be saved.

    Returns:
    - None
    """
    matrix = []
    header = ["Directory"] + list(aggregated_data.keys())
    matrix.append(header)

    # Get unique directories
    unique_dirs = list(
        set([item for sublist in aggregated_data.values() for item in sublist])
    )

    for directory in unique_dirs:
        row = [directory] + [
            "X" if directory in aggregated_data[pkg] else "" for pkg in header[1:]
        ]
        matrix.append(row)

    with open(
        os.path.join(base_dir, "requirements_overview.csv"), "w", newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerows(matrix)


def main():
    base_dir = sanitize_path(input("Enter the root directory to start scanning: "))

    depth = int(input("Enter the search depth (default 2): ") or 2)

    requirements_files = find_requirements_files(base_dir, depth)
    aggregated_data = aggregate_requirements(requirements_files, base_dir)

    with open(os.path.join(base_dir, "combined_requirements.txt"), "w") as out:
        for pkg, dirs in aggregated_data.items():
            out.write(f"# {pkg} is required in: {', '.join(dirs)}\n")
            out.write(f"{pkg}\n")

    generate_dependency_matrix(aggregated_data, base_dir)

    print(
        "Files 'combined_requirements.txt' and 'requirements_overview.txt' have been generated in the specified directory."
    )


if __name__ == "__main__":
    main()
