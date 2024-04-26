import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *
from pydantic import BaseModel, Field

model = NetModelFactory.createModel(NetModelType.INSTRUCTOR, model="phi3")

class Cat(BaseModel):
    fact: str = Field(..., description="A fact about cats.")
    
model.setJSONBaseModel(Cat)

stream = model.getModelResponse("Write a short cat fact about cat colors.")

cat = model.getResponseResultObject(stream)

print(cat.fact)
