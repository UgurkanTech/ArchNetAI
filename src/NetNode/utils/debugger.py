#Todo: Add colored logger with log levels and functionality for logging to a file.
class Debug:
    debug = False

    def on():
        Debug.debug = True

    def off():
        Debug.debug = False

    def set(debug):
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