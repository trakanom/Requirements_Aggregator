# ./output_handler.py

import os
import csv


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


def get_save_path(base_dir):
    """
    Prompt the user for where to save the output files.

    Returns:
    - list: List of paths to save the output files.
    """
    print("\nWhere would you like to save the output files?")
    print("1. Root folder of directory scanned.")
    print(
        "2. Inside the requirements_aggregator directory, under `outputs/<short-path-to-folder>/`."
    )
    print("3. A custom directory of your choosing.")
    print("4. A combination of the above (use comma-separated values, e.g., '1,3').")

    choices = input("Enter your choice(s): ").strip().split(",")
    save_paths = []

    if "1" in choices:
        save_paths.append(os.path.join(base_dir, "combined_requirements.txt"))

    if "2" in choices:
        short_path = base_dir.replace(os.getcwd(), "").replace(os.sep, "-").lstrip("-")
        path = os.path.join(
            os.getcwd(), "outputs", short_path, "combined_requirements.txt"
        )
        save_paths.append(path)

    if "3" in choices:
        custom_path = sanitize_path(input("Enter the custom directory path: "))
        save_paths.append(os.path.join(custom_path, "combined_requirements.txt"))

    return save_paths


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
