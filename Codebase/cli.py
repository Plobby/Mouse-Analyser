import os.path
import sys
import iomanager
import cli_logger
from cli_logger import LogLevel
import videoproc

# Function to open the command-line interface with a setp of inputs and an output directory
def open_cli(inputs, output):
    # Parse all input files
    for inp in inputs:
        # Check the path exists
        if (not os.path.exists(inp)):
            cli_logger.log(LogLevel.ERROR, "Input file does not exist at path: \"" + inp + "\"")
            sys.exit(1)
        # Check the path is a file, not a directory
        if (not os.path.isfile(inp)):
            cli_logger.log(LogLevel.ERROR, "Input path provided is not a file: \"" + inp + "\"")
            sys.exit(1)
        # Check the path is a valid filetype
        if (not inp.endswith(".mp4") and not inp.endswith(".avi") and not inp.endswith("mpg")):
            cli_logger.log(LogLevel.ERROR, "File provided is not of a valid type (mp4, avi, mpg): \"" + inp + "\"")
            sys.exit(1)
    # Check the output path exists
    if (not os.path.exists(output)):
        cli_logger.log(LogLevel.ERROR, "Output directory does not exist at path: \"" + output + "\"")
        sys.exit(1)
    # Check the output path is a directory
    if (not os.path.isdir(output)):
        cli_logger.log(LogLevel.ERROR, "Output path provided is not a directory: \"" + output + "\"")
        sys.exit(1)
    
    #Process each input video
    for inputVid in inputs:
        videoproc.processVideo(inputVid, doSaveVid=True, outputLocation=output)
        cli_logger.log(LogLevel.INFO, inputVid + " finished processing.")
    
    cli_logger.log(LogLevel.INFO, "All files processed.")