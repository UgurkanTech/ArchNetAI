from enum import Enum
from typing import override
from ollama import Client
from openai import OpenAI
from .tools import Timer
from rich.console import Console

class OllamaHost():
    """
    Represents a host for the Ollama service.

    Args:
        host (str): The base URL of the Ollama service. Defaults to "http://localhost:11434/v1".

    Attributes:
        _host (str): The base URL of the Ollama service.
        _openai (OpenAI): An instance of the OpenAI class.
        _client (Client): An instance of the Client class.

    """

    def __init__(self, host="http://localhost:11434/v1"):
        self._host = host
        self._openai = None
        self._client = None

    @property
    def openai(self):
        """
        Get an instance of the OpenAI class.

        Returns:
            OpenAI: An instance of the OpenAI class.

        """
        if self._openai is None:
            self._openai = OpenAI(base_url=self._host, api_key="Ollama")
        return self._openai

    @property
    def client(self):
        """
        Get an instance of the Client class.

        Returns:
            Client: An instance of the Client class.

        """
        if self._client is None:
            self._client = Client(host=self._host)
        return self._client

class ChatMessage(tuple):
    def __new__(cls, role, content):
        return super().__new__(cls, (role, f"{content}<|eot_id|>"))
    
class Options(dict):
    """
    A dictionary subclass representing the options for a model.

    Args:
        temperature (float): The temperature value for sampling.
        top_p (float): The top-p value for nucleus sampling.
        top_k (int): The top-k value for top-k sampling.
        repeat_penalty (float): The penalty value for repeating tokens.
        seed (int): The seed value for random number generation.
        num_ctx (int): The number of context tokens.
        num_pred (int): The number of predicted tokens.
        use_mlock (bool): Whether to use mlock for memory locking.
    """

    def __init__(self, temperature, top_p, top_k, repeat_penalty, seed, num_ctx, num_pred, use_mlock):
        super().__init__()
        self['temperature'] = temperature
        self['top_p'] = top_p
        self['top_k'] = top_k
        self['repeat_penalty'] = repeat_penalty
        self['seed'] = seed
        self['num_ctx'] = num_ctx
        self['num_predict'] = num_pred
        self['use_mlock'] = use_mlock

class ResultMask(dict):
    def __init__(self):
        super().__init__()

    def contains(self, resultType):
        return any(key.value == resultType.value for key in self.keys())
    
    def addType(self, resultType):
        self[resultType] = True

class ResultType(Enum):
    """
    Enum for the type of result.
    """
    STRING = 1
    STREAM = 2
    OBJECT = 3
    JSON_RESPONSE = 4
    JSON_STREAM_RESPONSE = 5
    INTERACTIVE = 6
    
    def __eq__(self, other):
        return other.value == self.value
    def __hash__(self):
        return self.value.__hash__()

class ResponseFactory():
    
    def __init__(self, mask):
        if mask is None:
            mask = ResultMask()
        self.mask = mask
    
    def GenerateResponse(self, modelResponse, isChat, resultType):
        if not self.mask.contains(resultType):
            raise ValueError("Result type not allowed.")

        if resultType == ResultType.STRING:
            return StringResponse(modelResponse, isChat).GetResult()
        elif resultType == ResultType.STREAM:
            StreamResponse(modelResponse, isChat).GetResult()
        elif resultType == ResultType.OBJECT:
            return ObjectResponse(modelResponse, isChat).GetResult()
        elif resultType == ResultType.JSON_RESPONSE:
            return JSONResponse(modelResponse, isChat).GetResult()
        elif resultType == ResultType.JSON_STREAM_RESPONSE:
            JSONStreamResponse(modelResponse, isChat).GetResult()
        elif resultType == ResultType.INTERACTIVE:
            raise NotImplementedError("Interactive response not implemented.")
        else:
            print(resultType)
            raise ValueError("Invalid result type.")


class Response():
    """
    Represents a response from a model.

    modelResponse: The response from the model.
    isChat (bool): True for client.chat, False for client.generate

    """

    def __init__(self, modelResponse, isChat):
        self.modelResponse = modelResponse
        self.isChat = isChat

    def GetResult(self):
        pass

class StringResponse(Response):
    """
    Represents a string response from a model.

    """

    def __init__(self, modelResponse, isChat):
        super().__init__(modelResponse, isChat)
    
    @override
    def GetResult(self):
        if self.isChat:
            response = ""
            for chunk in self.modelResponse:
                response += chunk['message']['content'].strip()
            return response
            #response = stream['response'].strip()
            #print(response)
        else:
            response = self.modelResponse['response'].strip()
            return response
            response = ""
            for chunk in self.modelResponse:
                response += chunk['response'].strip()
            return response

class StreamResponse(Response):
    """
    Represents a stream response from a model.

    """

    def __init__(self, modelResponse, isChat):
        super().__init__(modelResponse, isChat)

    def GetResult(self):
        if self.isChat:
            timer = Timer()
            for chunk in self.modelResponse:
                print(chunk['message']['content'], end='', flush=True)
                if 'usage' in chunk:
                    print(f"\nTokens used: {chunk['usage']['total_tokens']}")
            print()
            timer.print_time()
        else:
            timer = Timer()
            for chunk in self.modelResponse:
                print(chunk['response'], end='', flush=True)
                if 'usage' in chunk:
                    print(f"\nTokens used: {chunk['usage']['total_tokens']}")
            print()
            timer.print_time()

class ObjectResponse(Response):
    """
    Represents an object response from a model.

    """

    def __init__(self, modelResponse, isChat):
        super().__init__(modelResponse, isChat)

    def GetResult(self):
        return self.modelResponse
            

class JSONResponse(Response):
    """
    Represents a JSON response from a model.

    """

    def __init__(self, modelResponse, isChat):
        super().__init__(modelResponse, isChat)

    def GetResult(self):
        return self.modelResponse.model_dump()

class JSONStreamResponse(Response):
    """
    Represents a JSON stream response from a model.

    """

    def __init__(self, modelResponse, isChat):
        super().__init__(modelResponse, isChat)

    def GetResult(self):
        console = Console()
        timer = Timer()
        for extraction in self.modelResponse:
            obj = extraction.model_dump()
            console.clear()
            console.print(obj)
        timer.print_time()
