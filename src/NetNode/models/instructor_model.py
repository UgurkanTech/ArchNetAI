from .net_model import NetModel
from utils.tools import Timer
from rich.console import Console
import instructor
from utils.model import *

class InstructorModel(NetModel):
    """
    Represents an instructor model that interacts with the OpenAI API to generate responses based on user input.
    """
    @override
    def __init__(self, host, model):
        super().__init__(host, model)
        self._setInstructor()

        self.resultMask.addType(ResultType.OBJECT)
        self.resultMask.addType(ResultType.JSON_RESPONSE)
        self.resultMask.addType(ResultType.JSON_STREAM_RESPONSE)

    def _setInstructor(self):
        """
        Retrieves the JSON instructor from the OpenAI API.

        Returns:
            The JSON instructor object.
        """
        self.instructor = instructor.from_openai(
            self.host.openai,
            mode=instructor.Mode.JSON,
            temperature=0,
            top_p=0.99,
            seed=42,            
            max_tokens=256,
            #make changes here
        )
    
    def setJSONBaseModel(self, baseModel):
        """
        Sets the JSON base model for the instructor.

        Args:
            baseModel: The JSON base model to set.
        """
        self.baseModel = baseModel

    @override
    def createModelResponse(self, context):
        """
        Generates a model response based on the given context.

        Args:
            context: The input context for generating the response.

        Returns:
            The response stream from the model.
        """
        self.modelResponse = self.instructor.completions.create(
            model= self.model,
            response_model=instructor.Partial[self.baseModel],
            messages=[
                {
                    "role": "user",
                    "content": f"In valid JSON format. Do not use dict for strings. {context}",
                },
            ],
            stream=True, ## make changes here
        )
    