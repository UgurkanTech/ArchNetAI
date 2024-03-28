from typing import List
import instructor
from pydantic import BaseModel
from rich.console import Console
import time

class NodeInstructor:
    def __init__(self, llama_model):
        self.llama_model = llama_model
        self.create = instructor.patch(
            create=self.llama_model.llama.create_chat_completion_openai_v1,
            mode=instructor.Mode.JSON_SCHEMA,
        )


    def extract_info(self, text_block):


        class File(BaseModel):
            name: str
            directory: str
            content: str
            type: str

        class FileInfo(BaseModel):
            files: List[File]


        extraction_stream = self.create(
            response_model=instructor.Partial[FileInfo],
            messages=[
                {
                    "role": "user",
                    "content": f"Get the information about files and raw file content. Make sure to catch all files. Type is one of Write, Delete or Execute. Write directory of file with base / symbol.  Write file count. {text_block}",
                },
            ],
            stream=True,
        )

        console = Console()

        start_time = time.time()

        for extraction in extraction_stream:
            obj = extraction.model_dump()
            console.clear()
            console.print(obj)

        end_time = time.time()
        exec_time = end_time - start_time

        print(f"Total execution time: {exec_time:.4f} seconds")