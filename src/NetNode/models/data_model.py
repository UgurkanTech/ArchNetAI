from .net_model import NetModel
from utils.tools import *

class DataModel(NetModel):
    """
    Represents a data model used in the ArchNetAI system.

    Args:
        host (str): The host of the model.
        model (str): The model name.

    Attributes:
        client: The client associated with the host.
        options: The options for the model.

    Methods:
        setOptions: Sets the options for the model.
        getModelResponse: Generates a response from the model based on the given context.
        printResult: Prints the response and the time taken to generate it.
        getResponseResult: Returns the response generated by the model.
        printStream: Prints the response and the time taken to generate it.

    """

    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client

    def setOptions(self, options):
        """
        Sets the options for the model.

        Args:
            options (dict): The options for the model.

        """
        self.options = options

    def getModelResponse(self, context):
        """
        Generates a response from the model based on the given context.

        Args:
            context (str): The context for generating the response.

        Returns:
            dict: The generated response.

        """
        stream = self.client.generate(
            model=self.model,
            prompt=context,
            images=[],
            stream=False,
            format='json',
            options=self.options,
            keep_alive='1m'
        )
        return stream
    
    def printResult(self, stream):
        """
        Prints the response and the time taken to generate it.

        Args:
            stream (dict): The generated response.

        """
        timer = Timer()
        response = stream['response'].strip()
        print(response)
        timer.print_time()

    def getResponseResult(self, stream):
        """
        Returns the response generated by the model.

        Args:
            stream (dict): The generated response.

        Returns:
            str: The response generated by the model.

        """
        return stream['response'].strip()

    def printStream(self, stream):
        """
        Prints the response and the time taken to generate it.

        Args:
            stream (dict): The generated response.

        """
        self.printResult(stream)