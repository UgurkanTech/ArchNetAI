from enum import Enum
from tqdm import tqdm
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.model import *
from utils.response import *

class NetModel:
    """
    Represents a network model. Do not use this class directly. Use the NetModelFactory to create models.

    Args:
        host (str): The host of the model.
        model (str): The name of the model.

    Attributes:
        host (OllamaHost): The host object representing the model's host.
        model (str): The name of the model.

    Methods:
        getModelResponse: Placeholder method for getting the model response.
        pullModel: Pulls the model from the server if it doesn't exist locally.
        checkModelExists: Checks if the model exists on the server.
        printStream: Placeholder method for printing the stream.
        printResult: Placeholder method for printing the result.
        getResponseResult: Placeholder method for getting the response result.
    """

    def __init__(self, host, model):
        self.host = OllamaHost(host)
        self.model = model
        self.pullModel()
        self.resultMask = ResultMask()
        self.isChat = False

        self.options = Options()

        print(f"{self.__class__.__name__} initialized")

    def createModelResponse(self, context):
        self.modelResponse = None
        pass

    def getResponse(self, resultType):
        res = ResponseFactory(mask=self.resultMask)
        return res.GenerateResponse(self.modelResponse, self.isChat, self.options.isStream(), resultType)

    def setOptions(self, options):
        """
        Sets the options for generating responses.

        Args:
            options (dict): The options to be used for generating responses.

        """
        self.options = options

    def pullModel(self):
        """
        Pulls the model to the server if it doesn't exist.
        """
        if not self.checkModelExists():
            print(f"Model {self.model} not found. Pulling model...")
            
            current_digest, bars = '', {}
            for progress in self.host.client.pull(model=self.model, stream=True):
                digest = progress.get('digest', '')
                if digest != current_digest and current_digest in bars:
                    bars[current_digest].close()

                if not digest:
                    print(progress.get('status'))
                    continue

                if digest not in bars and (total := progress.get('total')):
                    bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

                if completed := progress.get('completed'):
                    bars[digest].update(completed - bars[digest].n)

                current_digest = digest



            print(f"Model {self.model} pulled successfully.")
        else:
            print(f"Model {self.model} ready on the server.")
    
    def checkModelExists(self):
        """
        Checks if the model exists on the server.

        Returns:
            bool: True if the model exists, False otherwise.
        """
        modellist = self.host.client.list()
        model_names = [model['name'] for model in modellist['models']]
        if self.model in model_names:
            return True
        else:
            for model in model_names:
                if model.split(':')[0] == self.model.split(':')[0]:
                    return True
        return False
    