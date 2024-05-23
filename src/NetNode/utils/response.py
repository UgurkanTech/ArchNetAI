from rich.console import Console
from .tools import Timer
from enum import Enum
from typing import override
from .debugger import Debug

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
    EMBEDDING = 7
    
    def __eq__(self, other):
        return other.value == self.value
    def __hash__(self):
        return self.value.__hash__()

class ResponseFactory():
    
    def __init__(self, mask):
        if mask is None:
            mask = ResultMask()
        self.mask = mask
    
    def GenerateResponse(self, modelResponse, isChat, isStream, resultType):
        if not self.mask.contains(resultType):
            raise ValueError("Result type not allowed.")

        match resultType:
            case ResultType.STRING:
                return StringResponse(modelResponse, isChat, isStream).GetResult()
            case ResultType.STREAM:
                return StreamResponse(modelResponse, isChat, isStream).GetResult()
            case ResultType.OBJECT:
                return ObjectResponse(modelResponse, isChat, isStream).GetResult()
            case ResultType.JSON_RESPONSE:
                return JSONResponse(modelResponse, isChat, isStream).GetResult()
            case ResultType.JSON_STREAM_RESPONSE:
                return JSONStreamResponse(modelResponse, isChat, isStream).GetResult()
            case ResultType.INTERACTIVE:
                raise NotImplementedError("Interactive response not implemented.")
            case ResultType.EMBEDDING:
                return EmbeddingResponse(modelResponse, isChat, isStream).GetResult()
            case _:
                raise ValueError(f"Invalid result type: {resultType}")


class Response():
    """
    Represents a response from a model.

    modelResponse: The response from the model.
    isChat (bool): True for client.chat, False for client.generate

    """

    def __init__(self, modelResponse, isChat, isStream):
        self.modelResponse = modelResponse
        self.isChat = isChat
        self.isStream = isStream

    def GetResult(self):
        pass

class StringResponse(Response):
    """
    Represents a string response from a model.

    """

    def __init__(self, modelResponse, isChat, isStream):
        super().__init__(modelResponse, isChat, isStream)
    
    @override
    def GetResult(self):
        if self.isStream:
            raise ValueError(f"Streaming must be disabled to use {self.__class__.__name__}")

        if self.isChat:
            response = self.modelResponse['message']['content'].strip()
            return response
        else:
            response = self.modelResponse['response'].strip()
            return response


class StreamResponse(Response):
    """
    Represents a stream response from a model.

    """

    def __init__(self, modelResponse, isChat, isStream):
        super().__init__(modelResponse, isChat, isStream)

    def GetResult(self):
        if not self.isStream:
            raise ValueError(f"Streaming must be enabled to use {self.__class__.__name__}")
        response = ""
        if self.isChat:
            timer = Timer()
            for chunk in self.modelResponse:
                msg = chunk['message']['content']
                response += msg
                print(msg, end='', flush=True)
                if 'eval_count' in chunk:
                    Debug.print(f"\nTokens created: {chunk['eval_count']}")
            print()
            timer.print_time()
        else:
            timer = Timer()
            for chunk in self.modelResponse:
                msg = chunk['response']
                response += msg
                print(msg, end='', flush=True)
                if 'eval_count' in chunk:
                    Debug.print(f"\nTokens created: {chunk['eval_count']}")
            print()
            timer.print_time()
        return response

class ObjectResponse(Response):
    """
    Represents an object response from a model.

    """

    def __init__(self, modelResponse, isChat, isStream):
        super().__init__(modelResponse, isChat, isStream)

    def GetResult(self):
        if self.isStream:
            raise ValueError(f"Streaming must be disabled to use {self.__class__.__name__}")

        return self.modelResponse
            

class JSONResponse(Response):
    """
    Represents a JSON response from a model.

    """

    def __init__(self, modelResponse, isChat, isStream):
        super().__init__(modelResponse, isChat, isStream)

    def GetResult(self):
        if self.isStream:
            raise ValueError(f"Streaming must be disabled to use {self.__class__.__name__}")

        return self.modelResponse.model_dump()

class JSONStreamResponse(Response):
    """
    Represents a JSON stream response from a model.

    """

    def __init__(self, modelResponse, isChat, isStream):
        super().__init__(modelResponse, isChat, isStream)

    def GetResult(self):
        if not self.isStream:
            raise ValueError(f"Streaming must be enabled to use {self.__class__.__name__}")

        console = Console()
        timer = Timer()
        for extraction in self.modelResponse:
            obj = extraction.model_dump()
            console.clear()
            console.print(obj)
        timer.print_time()

class EmbeddingResponse(Response):
    """
    Represents a JSON stream response from a model.

    """

    def __init__(self, modelResponse, isChat, isStream):
        super().__init__(modelResponse, isChat, isStream)

    def GetResult(self) -> list:
        if self.isStream:
            raise ValueError(f"Streaming must be disabled to use {self.__class__.__name__}")

        response = self.modelResponse['embedding']
        return response
        