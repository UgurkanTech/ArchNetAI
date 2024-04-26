import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *
from pydantic import BaseModel, Field

model = NetModelFactory.createModel(NetModelType.INSTRUCTOR, model="phi3")

class Cat(BaseModel):
    fact: str = Field(..., description="A fact about cats.")

model.setJSONBaseModel(Cat)

stream = model.getModelResponse("write a short cat fact about cat colors.")

#model.printStream(stream)

print(model.getResponseResult(stream))
