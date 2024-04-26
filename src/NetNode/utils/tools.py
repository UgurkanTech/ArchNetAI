import time
import base64
class Timer:
    def __init__(self):
        self.start_time = time.time()
    def get_time(self):
        return time.time() - self.start_time
    def reset(self):
        self.start_time = time.time()
    def print_time(self):
        print(f"Total execution time: {self.get_time():.4f} seconds")

class File():
    def convert_to_base64(file):
        with open(file, "rb") as image_file:
            str = base64.b64encode(image_file.read())
        return str