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


def get_save_path(base_dir, default_name="combined_requirements.txt"):
    """
    Presents the user with choices of where to save the output files and gets the save path.

    Parameters:
    - base_dir (str): The base directory from where the relative paths will be determined.

    Returns:
    - list: The paths to save the output files.
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
