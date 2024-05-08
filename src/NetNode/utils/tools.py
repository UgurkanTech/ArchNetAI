import time
import base64
import time

class Timer:
    """
    A simple timer class to measure execution time.
    """

    def __init__(self):
        self.start_time = time.time()

    def get_time(self):
        """
        Get the elapsed time since the timer was started.

        Returns:
            float: The elapsed time in seconds.
        """
        return time.time() - self.start_time

    def reset(self):
        """
        Reset the timer to start counting from the current time.
        """
        self.start_time = time.time()

    def print_time(self):
        """
        Print the total execution time in seconds.
        """
        print(f"Total execution time: {self.get_time():.4f} seconds")

class File():
    """A class for file operations."""

    def convert_to_base64(file):
        """Converts a file to base64 encoding.

        Args:
            file (str): The path to the file.

        Returns:
            str: The base64 encoded string representation of the file.
        """
        with open(file, "rb") as image_file:
            str = base64.b64encode(image_file.read())
        return str
    