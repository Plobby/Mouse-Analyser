import os.path
import sys
import iomanager
import cli_logger
from cli_logger import LogLevel
import videoproc
import configparser

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
    
    # Get config setting for output path
    config = configparser.ConfigParser()
    config.read("config.ini")
    output_location = config.get("General", "outputPath")
    generate_bounded_video = True if config.get("Video", "generate_video") == "1" else False
    # Create new thread
    process_videos(inputs, generate_bounded_video, output_location)

# Function to process videos on a separate thread
def process_videos(videos, generate_bounded_video, output_location):
    # Counter for video being processed
    processing_index = 1
    processing_total = len(videos)
    # Process all videos and append output to mouseData
    for video in videos:
        # Update status
        print("Processing video " + str(processing_index) + " of " + str(processing_total))
        # Start processing video
        videoproc.process_video(video, generate_bounded_video, output_location, progress_update)
        # Increment processing counter
        processing_index += 1
    print("All videos have finished processing!")

# Function to update the progress of the tracker
def progress_update(percentage):
    # Set processing status
    print("{:.1f} processed".format(percentage))