from .net_model import NetModel
from utils.tools import *

class DataModel(NetModel):
    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client

    def setOptions(self, options):
        self.options = options

    def getModelResponse(self, context):
        stream = self.client.generate(
            model=self.model,
            prompt= context,
            images=[],
            stream=False,
            format='json',
            options=self.options,
            keep_alive='1m'
        )
        return stream
    
    def printResult(self, stream):
        timer = Timer()
        response = stream['response'].strip()
        print(response)
        timer.print_time()

    def getResponseResult(self, stream):
        return stream['response'].strip()

    def printStream(self, stream):
        self.printResult(stream)