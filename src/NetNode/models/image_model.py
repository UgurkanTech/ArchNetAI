from typing import override
from .net_model import NetModel
from utils.tools import Timer, File
from utils.model import *

class ImageModel(NetModel):
    """
    Represents an image model that interacts with a host and a model.

    Args:
        host (str): The host of the model.
        model (str): The name of the model.

    Attributes:
        client: The client associated with the host.
        image: The image in base64 format.

    Methods:
        setImage: Sets the image attribute by converting the given image path to base64.
        getModelResponse: Retrieves the model response for the given context.
        printStream: Prints the model response stream.
        getResponseResult: Retrieves the concatenated model response from the stream.
    """
    @override
    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client

        self.resultMask.addType(ResultType.STRING)
        self.resultMask.addType(ResultType.STREAM)
        
        self.isChat = True
        
    def setImage(self, imagePath):
        self.image = File.convert_to_base64(imagePath)
    
    @override
    def createModelResponse(self, context):
        self.modelResponse = self.client.chat(
            model=self.model,
            messages=[{
            'role': 'user',
            'content': context,
            'images': [self.image],
            'temperature': 0,
            }],
            stream=True,
            options={
            'use_mlock': True
            },
            keep_alive='1m'
        )
