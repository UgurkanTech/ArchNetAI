from .net_model import NetModel
from utils.tools import Timer
from rich.console import Console
import instructor

class InstructorModel(NetModel):
    """
    Represents an instructor model that interacts with the OpenAI API to generate responses based on user input.
    """

    def __init__(self, host, model):
        super().__init__(host, model)
        self.instructor = self._getJSONInstructor()

    def _getJSONInstructor(self):
        """
        Retrieves the JSON instructor from the OpenAI API.

        Returns:
            The JSON instructor object.
        """
        return instructor.from_openai(
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
    
    def getModelResponse(self, context):
        """
        Generates a model response based on the given context.

        Args:
            context: The input context for generating the response.

        Returns:
            The response stream from the model.
        """
        stream = self.instructor.completions.create(
            model= self.model,
            response_model=instructor.Partial[self.baseModel],
            messages=[
                {
                    "role": "user",
                    "content": f"In valid JSON format. Do not use dict for strings. {context}",
                },
            ],
            stream=False, ## make changes here
        )
        return stream
    
    def _printStream(self, stream): #fix this
        """
        Prints the model response stream.

        Args:
            stream: The response stream to print.
        """
        console = Console()
        timer = Timer()
        for extraction in stream:
            obj = extraction.model_dump()
            console.clear()
            console.print(obj)
        timer.print_time()

    def getResponseResult(self, stream):
        """
        Returns the JSON string representation of the model response.

        Args:
            stream: The response stream.

        Returns:
            The JSON string representation of the model response.
        """
        return stream.model_dump()
    
    def getResponseResultObject(self, stream):
        """
        Returns the Base Model object of the model response.

        Args:
            stream: The response stream.

        Returns:
            The Base Model object of the model response.
        """
        return stream