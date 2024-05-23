#Todo: Add colored logger with log levels and functionality for logging to a file.
class Debug:
    """
    A class for managing debug mode and printing debug messages.
    """

    debug = False

    def on():
        """
        Turns on debug mode.
        """
        Debug.debug = True

    def off():
        """
        Turns off debug mode.
        """
        Debug.debug = False

    def set(debug):
        """
        Sets the debug mode to the specified value.

        Parameters:
            debug (bool): The value to set the debug mode to.
        """
        Debug.debug = debug

    def print(*args):
        """
        Prints the specified arguments if debug mode is enabled.

        Parameters:
            *args: The arguments to print.
        """
        if Debug.debug:
            print(*args)

    def printError(*args):
        """
        Prints the specified arguments as an error message if debug mode is enabled.

        Parameters:
            *args: The arguments to print as an error message.
        """
        if Debug.debug:
            print(f"Error: ", *args)

    def printWarning(*args):
        """
        Prints the specified arguments as a warning message if debug mode is enabled.

        Parameters:
            *args: The arguments to print as a warning message.
        """
        if Debug.debug:
            print(f"Warning: ", *args)