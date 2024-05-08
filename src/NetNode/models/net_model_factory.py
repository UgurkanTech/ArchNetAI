from enum import Enum
from .image_model import ImageModel
from .data_model import DataModel
from .instructor_model import InstructorModel
from .chat_model import ChatModel
from .embed_model import EmbedModel

from enum import Enum

class NetModelType(Enum):
    """
    Enum representing the types of network models.

    Attributes:
        IMAGE (int): Represents an image model.
        DATA (int): Represents a data model.
        INSTRUCTOR (int): Represents an instructor model.
        CHAT (int): Represents a chat model.
    """
    IMAGE = 1
    DATA = 2
    INSTRUCTOR = 3
    CHAT = 4
    EMBED = 5

class NetModelFactory:
    """
    Factory class for creating different types of network models.
    """

    @staticmethod
    def createModel(modelType, host="http://localhost:11434/v1", model="phi3"):
        """
        Creates and returns an instance of the specified model type.

        Parameters:
        - modelType (NetModelType): The type of model to create.
        - host (str): The host URL for the model server. Default is "http://localhost:11434/v1".
        - model (str): The name of the model. Default is "phi3".

        Returns:
        - model (NetModel): An instance of the specified model type.

        Raises:
        - ValueError: If an invalid model type is provided.
        """
        match modelType:
            case NetModelType.IMAGE:
                return ImageModel(host, model)
            case NetModelType.DATA:
                return DataModel(host, model)
            case NetModelType.INSTRUCTOR:
                return InstructorModel(host, model)
            case NetModelType.CHAT:
                return ChatModel(host, model)
            case NetModelType.EMBED:
                return EmbedModel(host, model)
            case _:
                raise ValueError("Invalid model type")