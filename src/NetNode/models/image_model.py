from .net_model import NetModel
from utils.tools import Timer, File

class ImageModel(NetModel):
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