# Requirements Aggregator

Requirements Aggregator is a handy tool designed to scan and combine the contents of `requirements.txt` files from nested directories into a unified `requirements.txt` file. It provides insights into which packages are required in which directories and highlights overlapping requirements.

## Features

- **Deep Scanning**: Recursively scans directories up to a user-specified depth.
- **Unified Output**: Combines multiple `requirements.txt` files into one, providing clear annotations.
- **Overlapping Detection**: Detects and comments out overlapping requirements, indicating the directories they are found in.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```
2. Navigate to the directory:
```bash
cd path-to-requirements-aggregator
```

## Usage

Run the script using Python:

```bash
python requirements_aggregator.py
```

Follow the on-screen prompts to provide the root directory and the desired scanning depth.

## Contributing

Contributions are welcome! Please submit a pull request or create an issue to discuss potential changes/additions.

## License

This project is open-source, available under the [MIT License](LICENSE).

## Acknowledgments

Thanks to all contributors and users who find value in this tool and provide feedback for continuous improvement.