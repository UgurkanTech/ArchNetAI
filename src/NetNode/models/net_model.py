from enum import Enum
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.model import *

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

    def createModelResponse(self, context):
        self.modelResponse = None
        pass

    def getResponse(self, resultType):
        res = ResponseFactory(mask=self.resultMask)
        return res.GenerateResponse(self.modelResponse, self.isChat, resultType)

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
            stream = self.host.client.pull(model=self.model, stream=True)
            for chunk in stream:
                print(chunk['status'], end='\n', flush=True)
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
    