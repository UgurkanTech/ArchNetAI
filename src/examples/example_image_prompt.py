import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.IMAGE, model="llava")

model.setImage("image.png")


model.createModelResponse("Explain this image.")

model.getResponse(resultType=ResultType.STREAM)




