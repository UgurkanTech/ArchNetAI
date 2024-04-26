import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.IMAGE, model="llava")

model.setImage("image.png")


stream = model.getModelResponse("Explain this image.")

#model.printStream(stream)

print(model.getResponseResult(stream))



