from optparse import OptionParser
import sys
import gui
import cli
import cli_logger
from cli_logger import LogLevel

# All code under here will only run if this file is being executed directly
# If it's imported, it won't run.
if __name__ == "__main__":
    # Create a new option parser and add options
    parser = OptionParser()
    parser.add_option("--nogui", "--nogui", action="store_false", default=True, dest="gui", help="Option to disable the GUI")
    parser.add_option("-i", "--input", action="store", type="string", default="", dest="input", help="The input files to process (comma separated)")
    parser.add_option("-o", "--output", action="store", type="string", default=".", dest="output", help="The output location for the processed files")
    parser.add_option("-l", "--loglevel", action="store", type="string", default="2", dest="loglevel", help="The level of logging to output (0 = INFO, 1 = WARN, 2 = ERROR)")
    # Parse the input rguments
    (opts, args) = parser.parse_args(sys.argv)
    # Set the logging level as appropriate
    log_level = opts.loglevel.lower()
    if (log_level == "0" or log_level == "info" or log_level == "i"):
        cli_logger.set_log_level(LogLevel.INFO)
    elif (log_level == "1" or log_level == "warn" or log_level == "w"):
        cli_logger.set_log_level(LogLevel.WARN)
    else:
        cli_logger.set_log_level(LogLevel.ERROR)
    # Check if the GUI should be shown
    if (opts.gui):
        # Show the GUI
        gui.show_window()
    else:
        # Print help if no input is given
        if (opts.input == "" or opts.input.isspace()):
            cli_logger.log(LogLevel.ERROR, "No input files have been provided!")
            parser.print_help()
            sys.exit(1)
        # Run the CLI
        cli.open_cli(opts.input.split(','), opts.output)
