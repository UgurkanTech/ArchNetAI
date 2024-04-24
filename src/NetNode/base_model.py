from rich.console import Console
import time
import instructor
from ollama import Client
from openai import OpenAI
from NetNode.utils import ChatMessage, File
import json
from enum import Enum

class OllamaHost():
    def __init__(self, host="http://localhost:11434/v1"):
        self._host = host
        self._openai = None
        self._client = None

    @property
    def openai(self):
        if self._openai is None:
            self._openai = OpenAI(base_url=self._host, api_key="Ollama")
        return self._openai

    @property
    def client(self):
        if self._client is None:
            self._client = Client(host=self._host)
        return self._client

class Timer:
    def __init__(self):
        self.start_time = time.time()
    def get_time(self):
        return time.time() - self.start_time
    def reset(self):
        self.start_time = time.time()
    def print_time(self):
        print(f"Total execution time: {self.get_time():.4f} seconds")

class ModelType(Enum):
    IMAGE = 1
    DATA = 2
    INSTRUCTOR = 3
    CHAT = 4

class NetModelFactory:
    @staticmethod
    def createModel(modelType, host = "http://localhost:11434/v1", model = "phi3"):
        if modelType == ModelType.IMAGE:
            return ImageModel(host, model)
        elif modelType == ModelType.DATA:
            return DataModel(host, model)
        elif modelType == ModelType.INSTRUCTOR:
            return InstructorModel(host, model)
        elif modelType == ModelType.CHAT:
            return ChatModel(host, model)
        else:
            raise ValueError("Invalid model type")

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


class ChatModel(NetModel):
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
            stream=True,
            options=self.options,
            keep_alive='1m'
        )
        return stream

    def ChatInteractive(self):
        while True:
            prompt = input("You: ")
            if prompt.lower() == "exit":
                break
            try:
                print("AI: ", end='')
                self.printStream(self.getModelResponse(prompt))
            except Exception as e:
                print("An error occurred: ", str(e))

    def printStream(self, stream):
        timer = Timer()
        for chunk in stream:
            print(chunk['response'], end='', flush=True)
            if 'usage' in chunk:
                print(f"\nTokens used: {chunk['usage']['total_tokens']}")
        print()
        timer.print_time()

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

    def printStream(self, stream):
        self.printResult(stream)

class InstructorModel(NetModel):
    def __init__(self, host, model):
        super().__init__(host, model)
        self.instructor = self._getJSONInstructor()

    def _getJSONInstructor(self):
        return instructor.from_openai(
            self.host.openai,
            mode=instructor.Mode.JSON,
        )
    
    def setJSONBaseModel(self, baseModel):
        self.baseModel = baseModel
    
    def getModelResponse(self, context):
        stream = self.instructor.completions.create(
            model= self.model,
            response_model=instructor.Partial[self.baseModel],
            messages=[
                {
                    "role": "user",
                    "content": f"In JSON format. {context}",
                },
            ],
            stream=True,
        )
        return stream
    
    def printStream(self, stream):
        console = Console()
        timer = Timer()
        for extraction in stream:
            obj = extraction.model_dump()
            console.clear()
            console.print(obj)
        timer.print_time()


    

