# ./requirements_aggregator.py

"""
Requirements Aggregator with Dependency Matrix

This script scans for requirements.txt files inside imported directories 
and combines their content into a unified `combined_requirements.txt` file at the root of the specified directory. 
It provides a mapping of packages to directories and highlights overlapping requirements. 
Additionally, it generates a dependency matrix in the form of a `requirements_overview.csv`.

Usage:
    Run the script and provide the root directory to start scanning.
"""

import os
from file_discovery import find_requirements_files, aggregate_requirements
from output_handler import get_save_path, save_outputs, sanitize_path


def main():
    # Gather all user inputs first
    base_dir = sanitize_path(input("Enter the root directory to start scanning: "))
    depth = int(input("Enter the search depth (default 2): ") or 2)
    save_paths = get_save_path(base_dir)

    # Inform the user that processing is starting
    print("\nScanning and processing the directories...")

    # Execute the scanning and processing
    requirements_files = find_requirements_files(base_dir, depth)
    aggregated_data = aggregate_requirements(requirements_files, base_dir)

    # Save the outputs to the desired locations
    save_outputs(aggregated_data, save_paths)

    print("\nFiles have been generated at the specified locations.")


if __name__ == "__main__":
    main()
