#Todo: Add colored logger with log levels and functionality for logging to a file.
class Debug:
    debug = False

    def setDebug(debug):
        Debug.debug = debug

    def print(*args):
        if Debug.debug:
            print(*args)

    def printError(*args):
        if Debug.debug:
            print(f"Error: ", *args)

    def printWarning(*args):
        if Debug.debug:
            print(f"Warning: ", *args)