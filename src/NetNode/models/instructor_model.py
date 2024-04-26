from .net_model import NetModel
from utils.tools import Timer
from rich.console import Console
import instructor

class InstructorModel(NetModel):

    def __init__(self, host, model):
        super().__init__(host, model)
        self.instructor = self._getJSONInstructor()

    def _getJSONInstructor(self):
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
        self.baseModel = baseModel
    
    def getModelResponse(self, context):
        stream = self.instructor.completions.create(
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
        return stream
    
    def printStream(self, stream):
        console = Console()
        timer = Timer()
        for extraction in stream:
            obj = extraction.model_dump()
            console.clear()
            console.print(obj)
        timer.print_time()

    """Returns JSON string."""
    def getResponseResult(self, stream):
        return stream.model_dump()
    
    """Returns JSON Base Model object."""
    def getResponseResultObject(self, stream):
        return stream