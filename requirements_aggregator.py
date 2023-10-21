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


def get_save_path(base_dir, default_name="combined_requirements.txt"):
    """
    Presents the user with choices of where to save the output files and gets the save path.

    Parameters:
    - base_dir (str): The base directory from where the relative paths will be determined.

    Returns:
    - str: The path to save the output files.
    """
    print("\nWhere would you like to save the output files?")
    print("0. Root folder of the directory scanned.")
    print(
        "1. Inside the requirements_aggregator directory under outputs/<short-path-to-folder>/"
    )
    print("2. A custom directory of your choosing.")
    choice = input(
        "Enter choice number (or multiple numbers separated by comma for multiple locations): "
    )

    short_path = base_dir.replace(os.sep, "-").strip("-")
    aggregator_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir_inside_aggregator = os.path.join(aggregator_dir, "outputs", short_path)

    save_paths = {
        "0": base_dir,
        "1": output_dir_inside_aggregator,
        "2": input("Enter the path to the custom directory: ").strip(),
    }

    selected_paths = [
        save_paths[str(c)] for c in choice.split(",") if str(c) in save_paths
    ]
    print(
        choice, short_path, aggregator_dir, output_dir_inside_aggregator, selected_paths
    )
    # Ask for custom output filename
    custom_name = input(
        f"Enter a custom name for the output requirements file (default: {default_name}): "
    ).strip()
    filename = custom_name if custom_name else default_name

    return [os.path.join(path, filename) for path in selected_paths]


def save_outputs(aggregated_data, save_paths):
    """
    Saves the aggregated requirements and the dependency matrix to the specified paths.

    Parameters:
    - aggregated_data (dict): The aggregated requirements data.
    - save_paths (list): List of paths to save the output files.

    Returns:
    - None
    """
    # Saving the combined requirements
    for path in save_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as out:
            for pkg, dirs in aggregated_data.items():
                out.write(f"# {pkg} is required in: {', '.join(dirs)}\n")
                out.write(f"{pkg}\n")
        print(f"File saved at {path}")

    # Saving the dependency matrix
    matrix_paths = [
        os.path.join(os.path.dirname(path), "requirements_overview.csv")
        for path in save_paths
    ]
    for path in matrix_paths:
        generate_dependency_matrix(aggregated_data, os.path.dirname(path))
        print(f"Dependency matrix saved at {path}")


def main():
    base_dir = sanitize_path(input("Enter the root directory to start scanning: "))
    depth = int(input("Enter the search depth (default 2): ") or 2)

    requirements_files = find_requirements_files(base_dir, depth)
    aggregated_data = aggregate_requirements(requirements_files, base_dir)

    save_paths = get_save_path(base_dir)

    save_outputs(aggregated_data, save_paths)

    print("Files have been generated at the specified locations.")


if __name__ == "__main__":
    main()
