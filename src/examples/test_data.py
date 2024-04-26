import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.DATA, model="phi3")

options = Options(temperature=1, top_k=64, top_p=0.9, repeat_penalty=1.2, seed=-1, num_ctx=512, num_pred=64 , use_mlock=True)

model.setOptions(options)

stream = model.getModelResponse("write a short cat fact about cat colors. fact=")

print(model.getResponseResult(stream=stream))
