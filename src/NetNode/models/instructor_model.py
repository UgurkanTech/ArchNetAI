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
            temperature= self.options['temperature'],
            top_p= self.options['top_p'],
            seed= self.options['seed'],
        )

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
            response_model=instructor.Partial[self.options.getBaseModel()],
            messages=[
                {
                    "role": "user",
                    "content": f"In valid JSON format. Do not use dict for strings. {context}",
                },
            ],
            stream= self.options['stream'],
        )
    