import ast
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="Write parameters & function descriptions from a python file")
    parser.add_argument("-p", "--path", help="Path to the python file or folder with python files to describe")
    parser.add_argument("-o", "--out", help="Name of the output file")
    args = parser.parse_args()
    path = args.path
    out_name = args.out
    return out_name, path


def prepare_files(out_name, path):
    if not out_name.endswith(".md"):
        # remove previous if . is there
        if "." in out_name:
            out_name = out_name[:out_name.rindex(".")]
        out_name += ".md"
    # check if path is a directory or a file
    if os.path.isdir(path):
        # if path is a directory, get all python files in the directory
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.py')]
    else:
        # if path is a file, read the file
        files = [path]
    return files, out_name


def parse_function(functions, node):
    if node.name != "main":
        docstring = ast.get_docstring(node)
        if docstring is None:
            desc = "No description available"
        else:
            docstring = docstring.split("\n")
            desc = ""
            for line in docstring:
                if not line.startswith(":param") and not line.startswith(":return") and not line.startswith(":type"):
                    desc += line + " "
        functions.append(f"**{node.name}**: {desc}\n")


def parse_parameter(node, parameters):
    if isinstance(node.targets[0], ast.Name):
        if node.targets[0].id.isupper():
            parameters.append(f"**{node.targets[0].id}**: {node.value.value}\n")


def parse_class(classes, node):
    docstring = ast.get_docstring(node)
    if docstring is None:
        desc = "No class description available"
    else:
        desc = docstring
    classes.append(f"**{node.name}**: {desc}\n")


def parse_file(file, out_file):
    out_file.write(f"# {os.path.basename(file)}\n")
    with open(file, 'r') as f:
        code = f.read()
    # parse the code using ast.walk. For each node, if it is a global variable that is all caps, write Parameter name: value.
    # If it is a function, write Function name: description without the variable descriptions.
    tree = ast.parse(code)
    parameters = []
    functions = []
    classes = []
    skip = []
    for node in ast.walk(tree):
        if node in skip:
            continue
        if isinstance(node, ast.ClassDef):
            parse_class(classes, node)
            skip.extend(list(ast.walk(node)))
        if isinstance(node, ast.Assign):
            parse_parameter(node, parameters)
        elif isinstance(node, ast.FunctionDef):
            parse_function(functions, node)
            skip.extend(list(ast.walk(node)))
    return functions, parameters, classes


def main():
    # parse filename/directory path from command line
    out_name, path = parse_arguments()

    # remove file type if exists and replace with md
    files, out_name = prepare_files(out_name, path)

    with open(out_name, 'w') as out_file:
        # iterate over all files
        for file in files:
            # read the file
            functions, parameters, classes = parse_file(file, out_file)

            # write the parameters and functions to the output file
            if len(parameters) == 0 and len(functions) == 0 and len(classes) == 0:
                out_file.write("No parameters, functions or classes found in this file\n")
            if len(parameters) > 0:
                out_file.write("### Parameters\n")
                for param in parameters:
                    out_file.write(f"* {param}")

            if len(classes) > 0:
                out_file.write("\n### Classes\n")
                for cls in classes:
                    out_file.write(f"* {cls}")

            if len(functions) > 0:
                out_file.write("\n### Functions\n")
                for func in functions:
                    out_file.write(f"* {func}")


if __name__ == '__main__':
    main()
