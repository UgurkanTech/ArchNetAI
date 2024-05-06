from enum import Enum
from .net_model import NetModel
from utils.tools import *
from utils.model import *
from typing import override

class ChatModel(NetModel):
    """
    Represents a chat model that interacts with a host and generates responses using a specified model.

    Args:
        host (Host): The host object representing the connection to the model server.
        model (str): The name or ID of the model to use for generating responses.

    Attributes:
        client (Client): The client object representing the connection to the model server.
        options (dict): The options to be used for generating responses.

    Methods:
        setOptions: Sets the options for generating responses.
        getModelResponse: Generates a response from the model given a context.
        ChatInteractive: Starts an interactive chat session with the model.
        printStream: Prints the generated response stream.

    """
    @override
    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client

        self.resultMask.addType(ResultType.STRING)
        self.resultMask.addType(ResultType.STREAM)
        self.resultMask.addType(ResultType.INTERACTIVE)
        

    @override
    def createModelResponse(self, context):
        """
        Generates a response from the model given a context.

        Args:
            context (str): The context or prompt for generating the response.

        """
        self.modelResponse = self.client.generate(
            model=self.model,
            prompt=context,
            images=[],
            stream=True,
            options=self.options,
            keep_alive='1m'
        )

    @override
    def getResponse(self, resultType):
        """
        Returns the result based on the specified type.

        """
        res = ResponseFactory(mask=self.resultMask)

        if resultType == ResultType.INTERACTIVE:
            return self._chatInteractive()
        else:
            return res.GenerateResponse(self.modelResponse, self.isChat, resultType)

    def _chatInteractive(self):
        """
        Starts an interactive chat session with the model.

        The user can input prompts and receive responses from the model until they enter "exit".

        """
        while True:
            prompt = input("You: ")
            if prompt.lower() == "exit":
                break
            try:
                print("AI: ", end='')
                self.createModelResponse(prompt)
                StreamResponse(self.modelResponse, self.isChat).GetResult()
            except Exception as e:
                print("An error occurred: ", str(e))