import os
import traceback
from unittest import TestCase
from subprocess import run, CalledProcessError
import subprocess
import logging


class TestExamples(TestCase):
    def run_example(self, example_name):
        try:
            logging.basicConfig(level=logging.INFO, format='%(message)s')
            logging.info(f"\nTest running {example_name}")
            run(["python", os.path.join(os.path.dirname(__file__), f"../examples/{example_name}")], 
                check=True, stdout=subprocess.DEVNULL)
        except CalledProcessError as e:
            self.fail(f"Failed with exception: {e}\n{traceback.format_exc()}")
        logging.info(f"Test {example_name} completed.")

    def test_data(self):
        self.run_example("example_data.py")

    def test_json(self):
        self.run_example("example_json.py")

    def test_object(self):
        self.run_example("example_object.py")

    def test_embed(self):
        self.run_example("example_embed.py")