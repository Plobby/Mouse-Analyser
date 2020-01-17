import os.path
import sys
import iomanager

# Function to open the command-line interface with a setp of inputs and an output directory
def open_cli(inputs, output):
    # Parse all input files
    for inp in inputs:
        # Check the path exists
        if (not os.path.exists(inp)):
            print("Error: Input file does not exist at path: \"" + inp + "\"")
            sys.exit(1)
        # Check the path is a file, not a directory
        if (not os.path.isfile(inp)):
            print("Error: Input path provided is not a file: \"" + inp + "\"")
            sys.exit(1)
        # Check the path is a valid filetype
        if (not inp.endswith(".mp4") and not inp.endswith(".avi") and not inp.endswith("mpg")):
            print("Error: File provided is not of a valid type (mp4, avi, mpg): \"" + inp + "\"")
            sys.exit(1)
    # Check the path exists
    if (not os.path.exists(output)):
        print("Error: Output directory does not exist at path: \"" + output + "\"")
        sys.exit(1)
    # Check the path is a directory
    if (not os.path.isdir(output)):
        print("Error: Output path provided is not a directory: \"" + output + "\"")
        sys.exit(1)
    # Process the files
    iomanager.open_files(inputs)