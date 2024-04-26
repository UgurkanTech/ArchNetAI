# ArchNetAI

ArchNetAI is a Python library that leverages the Ollama API for generating AI-powered content.

Created by [UgurkanTech](https://github.com/UgurkanTech)

## Features

- ChatModel: A module for generating AI-powered chat responses. This module can be used to create a conversational AI assistant that can respond to user queries and engage in natural language conversations.

- DataModel: A module for generating random data. This module provides functions to generate random data such as names, addresses, phone numbers, and more. It can be useful for testing and generating sample data for applications.

- ImageModel: An image analysis module for explaining images and classifying them. This module uses LLAVA models to analyze images and provide explanations for the content of the images. It can also classify images into different categories or labels.

- InstructorModel: A utility for populating JSON and object templates with data. This module provides functions to fill JSON and object templates with data, making it easier to generate dynamic JSON files and create instances of objects with predefined properties and values.

These modules provide powerful functionality for AI-powered content generation, data manipulation, image analysis, and template filling. They can be used individually or in combination to build sophisticated AI applications.

# Examples

Here are some examples of how to use ArchNetAI:

**ChatModel Example**
```python
from NetNode import *

model = NetModelFactory.createModel(NetModelType.CHAT, model="phi3")
options = Options(temperature=1, top_k=64, top_p=0.9, repeat_penalty=1.2, seed=-1, num_ctx=512, num_pred=256, use_mlock=True)
model.setOptions(options)

model.ChatInteractive()
```

**ImageModel Example**
```python
from NetNode import *

model = NetModelFactory.createModel(NetModelType.IMAGE, model="llava")
model.setImage("image.png")
stream = model.getModelResponse("Explain this image.")

print(model.getResponseResult(stream))
```

**InstructorModel Object Fill Example**

```python
from NetNode import *
from pydantic import BaseModel, Field

model = NetModelFactory.createModel(NetModelType.INSTRUCTOR, model="phi3")

class Cat(BaseModel):
    fact: str = Field(..., description="A fact about cats.")
    
model.setJSONBaseModel(Cat)
stream = model.getModelResponse("write a short cat fact about cat colors. JSON.")
cat = model.getResponseResultObject(stream)

print(cat.fact)
```