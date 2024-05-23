import time
import base64
import time
import hashlib
import os
from .debugger import Debug

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

        Debug.print(f"Total execution time: {self.get_time():.4f} seconds")

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

class Hasher:
    @staticmethod
    def hash(input, chunk_size=8192, algorithm="sha1"):
        """
        Compute the hash of a file or text in chunks.

        Args:
            input (file-like object, str, or path-like object): The input to compute the hash of.
            chunk_size (int, optional): The size of the chunks to read. Default is 8192.
            algorithm (str, optional): The hash algorithm to use. Default is "sha1".

        Returns:
            str: The hash of the input.
        """
        hasher = hashlib.new(algorithm)
        if isinstance(input, str):
            # If input is a string, check if it's a file path
            if os.path.isfile(input):
                with open(input, 'rb') as f:
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        hasher.update(chunk)
            else:
                hasher.update(input.encode())
        else:
            # If input is a file-like object, read it in chunks
            while True:
                chunk = input.read(chunk_size)
                if not chunk:
                    break
                if isinstance(chunk, str):
                    chunk = chunk.encode()
                hasher.update(chunk)
        return hasher.hexdigest()