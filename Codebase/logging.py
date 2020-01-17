from enum import IntEnum

# Create log level enum
class LogLevel(IntEnum):
    INFO = 0
    WARN = 1
    ERROR = 2

# Function to set the current log level
def set_log_level(level):
    # Set the log level
    global current_level
    current_level = level
    # Maximise/ minimise bounds
    if (current_level < 0):
        current_level = LogLevel.INFO
    elif (current_level > 2):
        current_level = LogLevel.ERROR
    # Log message to confirm level change
    log(LogLevel.INFO, "Set log level to " + level.name)

# Create function to log a message
def log(level, msg):
    # Check if the message should be logged
    global current_level
    if (current_level <= level):
        # Print with the enum prefix
        print("[" + level.name + "] " + msg)

# Variable to store the current log level
current_level = LogLevel.ERROR