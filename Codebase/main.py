from optparse import OptionParser
import sys
import gui
import cli

# All code under here will only run if this file is being executed directly
# If it's imported, it won't run.
if __name__ == "__main__":
    # Create a new option parser and add options
    parser = OptionParser()
    parser.add_option("--nogui", "--nogui", action="store_false", default=True, dest="gui", help="Option to disable the GUI")
    parser.add_option("-i", "--input", action="store", type="string", default="", dest="input", help="The input files to process (comma separated)")
    parser.add_option("-o", "--output", action="store", type="string", default=".", dest="output", help="The output location for the processed files")
    # Parse the input rguments
    (opts, args) = parser.parse_args(sys.argv)
    # Check if the GUI should be shown
    if (opts.gui):
        # Show the GUI
        gui.show_gui()
    else:
        # Print help if no input is given
        if (opts.input == "" or opts.input.isspace()):
            print("Error: No input files have been provided!")
            parser.print_help()
            sys.exit(1)
        # Run the CLI
        cli.open_cli(opts.input.split(','), opts.output)
