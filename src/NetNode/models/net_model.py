import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.model import *

class NetModel:
    def __init__(self, host, model):
        self.host = OllamaHost(host)
        self.model = model
        self.pullModel()

    def getModelResponse(self, context):
        pass

    def pullModel(self):
        if not self.checkModelExists():
            print(f"Model {self.model} not found. Pulling model...")
            stream = self.host.client.pull(model=self.model, stream=True)
            for chunk in stream:
                print(chunk['status'], end='\n', flush=True)
            print(f"Model {self.model} pulled successfully.")
        else:
            print(f"Model {self.model} ready on the server.")
    
    def checkModelExists(self):
        modellist = self.host.client.list()
        model_names = [model['name'] for model in modellist['models']]
        if self.model in model_names:
            return True
        else:
            for model in model_names:
                if model.split(':')[0] == self.model.split(':')[0]:
                    return True
        return False
    
    def printStream(self, stream):
        pass

    def printResult(self, stream):
        pass

    def getResponseResult(self, stream):
        pass