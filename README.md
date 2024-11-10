# Module description to MD

This project provides a script to extract and document parameters, functions, and classes from Python files. The script generates a Markdown file with the extracted information.

## Features

- Extracts global parameters (constants) from Python files.
- Extracts function names and their docstrings.
- Extracts class names and their docstrings.
- Supports processing a single file or all Python files in a directory.

## Usage

### Command Line Arguments

- `-p`, `--path`: Path to the Python file or folder containing Python files to describe.
- `-o`, `--out`: Name of the output Markdown file.

### Example

To run the script on a single file:

```sh
python module_description_to_md.py -p simulation_file.py -o parameter_description.md
```

## Output
The script generates a Markdown file with the following structure:  
* Parameters: Lists all global parameters (constants) found in the file(s).
* Functions: Lists all functions with their descriptions.
* Classes: Lists all classes with their descriptions.

## Requirements
Python 3.x

## Installation
Clone the repository:
```sh
git clone https://github.com/odedwer/module_description_to_md.git
cd parameter-dump
```
