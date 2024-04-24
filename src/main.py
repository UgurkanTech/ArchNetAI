from NetNode import *
DataModel
model = NetModelFactory.createModel(ModelType.DATA, model="phi3")


options = Options(temperature=1, top_k=64, top_p=0.9, repeat_penalty=1.2, seed=-1, num_ctx=512, num_pred=64 , use_mlock=True)

model.setOptions(options)

#model.setImage("image.png")

stream = model.getModelResponse("write a short cat fact about cat colors in JSON. JSON only has one parameter. fact=")

model.printStream(stream=stream)

exit()

from typing import List
from pydantic import BaseModel

#model.setJSONBaseModel(File)







class File(BaseModel):
    name: str
    directory: str
    content: str
    type: str

class FileInfo(BaseModel):
    files: List[File]


exit()

while True:
    prompt = input("You: ")
    if prompt.lower() == "exit":
        break

    try:
        generated_text = model.generate_response(prompt)
        print("Assistant: ", generated_text)
    except Exception as e:
        print("An error occurred: ", str(e))

