import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.INSTRUCTOR, model="phi3")

from pydantic import BaseModel

class Cat(BaseModel):
    fact: str
    def __str__(self):
        return f"Cat(fact='{self.fact}')"
    

model.setJSONBaseModel(Cat)

stream = model.getModelResponse("write a short cat fact about cat colors. fact=")

#model.printStream(stream)

print(model.getResponseResult(stream=stream))
