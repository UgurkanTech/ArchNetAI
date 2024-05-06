import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.DATA, model="phi3")

model.createModelResponse("write one sentence cat fact about cats. fact=")

print(model.getResponse(resultType=ResultType.STRING))
