import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.IMAGE, model="llava")

model.options.setImage("image.png")
model.options.setStreaming(True)

model.createModelResponse("Explain this image.")

model.getResponse(resultType=ResultType.STREAM)




