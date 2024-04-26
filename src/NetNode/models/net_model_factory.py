from enum import Enum
from .image_model import ImageModel
from .data_model import DataModel
from .instructor_model import InstructorModel
from .chat_model import ChatModel

class NetModelType(Enum):
    IMAGE = 1
    DATA = 2
    INSTRUCTOR = 3
    CHAT = 4

class NetModelFactory:
    @staticmethod
    def createModel(modelType, host = "http://localhost:11434/v1", model = "phi3"):
        if modelType == NetModelType.IMAGE:
            return ImageModel(host, model)
        elif modelType == NetModelType.DATA:
            return DataModel(host, model)
        elif modelType == NetModelType.INSTRUCTOR:
            return InstructorModel(host, model)
        elif modelType == NetModelType.CHAT:
            return ChatModel(host, model)
        else:
            raise ValueError("Invalid model type")