from .net_model import NetModel
from utils.tools import Timer, File

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

    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client
        
    def setImage(self, imagePath):
        self.image = File.convert_to_base64(imagePath)

    def getModelResponse(self, context):
        stream = self.client.chat(
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
        return stream

    def printStream(self, stream):
        timer = Timer()
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
        print()
        timer.print_time()

    def getResponseResult(self, stream):
        response = ""
        for chunk in stream:
            response += chunk['message']['content']
        return response