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

    @override
    def createModelResponse(self, context):
        self.modelResponse = self.client.chat(
            model=self.model,
            messages=[{
            'role': 'user',
            'content': context,
            'images': self.options['images'],
            }],
            stream= self.options['stream'],
            options={
                'temperature': self.options['temperature'],
                'top_k': self.options['top_k'],
                'top_p': self.options['top_p'],
                'repeat_penalty': self.options['repeat_penalty'],
                'seed': self.options['seed'],
                'num_ctx': self.options['num_ctx'],
                'num_predict': self.options['num_predict'],
                'use_mlock': self.options['use_mlock'],
            },
            keep_alive= self.options['keep_alive']
        )
