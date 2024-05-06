import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *
from pydantic import BaseModel, Field

model = NetModelFactory.createModel(NetModelType.INSTRUCTOR, model="phi3")

class Cat(BaseModel):
    fact: str = Field(..., description="A fact about cats.")

model.setJSONBaseModel(Cat)

model.createModelResponse("Write a short cat fact about cat colors.")

print(model.getResponse(resultType=ResultType.JSON_RESPONSE))
