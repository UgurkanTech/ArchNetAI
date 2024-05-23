# ArchNetAI

ArchNetAI is a Python library that leverages the Ollama API for generating AI-powered content.

Created by [UgurkanTech](https://github.com/UgurkanTech)

## Setup

To install the NetNode module, Install [Ollama](https://ollama.com/) then navigate to the `setup.py` containing directory and run the following command:

```bash
pip3 install .
```

## Features

- **ChatModel:** A module for generating AI-powered chat responses. This module can be used to create a conversational AI assistant that can respond to user queries and engage in natural language conversations. ChatModel supports chat history and data input.

- **DataModel:** A module for generating random data. This module provides functions to generate random data such as names, addresses, phone numbers, and more. It can be useful for testing and generating sample data for applications.

- **ImageModel:** An image analysis module for explaining images and classifying them. This module uses LLAVA models to analyze images and provide explanations for the content of the images. It can also classify images into different categories or labels.

- **InstructorModel:** A utility for populating JSON and object templates with data. This module provides functions to fill JSON and object templates with data, making it easier to generate dynamic JSON files and create instances of objects with predefined properties and values.

These modules provide powerful functionality for AI-powered content generation, data manipulation, image analysis, and template filling. They can be used individually or in combination to build sophisticated AI applications.

# Examples

Here are some examples of how to use ArchNetAI:

**ChatModel Example**
```python
from NetNode import *
#Initialize model
model = NetModelFactory.createModel(NetModelType.CHAT, model="phi3")
#Set options
options = Options(temperature=1, top_k=64, top_p=0.9, repeat_penalty=1.2, stream=True)
model.setOptions(options)
#Start interactive mode
model.getResponse(resultType=ResultType.INTERACTIVE)
```

**ImageModel Example**
```python
from NetNode import *
#Initialize model
model = NetModelFactory.createModel(NetModelType.IMAGE, model="llava")
#Set options
model.options.setImage("image.png")
model.options.setStreaming(True)
#Create model response
model.createModelResponse("Explain this image.")
#Print results
model.getResponse(resultType=ResultType.STREAM)
```

**InstructorModel Object Fill Example**

```python
from NetNode import *
from pydantic import BaseModel, Field
#Initialize model
model = NetModelFactory.createModel(NetModelType.INSTRUCTOR, model="phi3")
#Define BaseModel
class Cat(BaseModel):
    fact: str = Field(..., description="A fact about cats.")
#Set BaseModel
model.options.setBaseModel(Cat)
#Create model response
model.createModelResponse("Write a short cat fact about cat colors.")
#Get result object
cat = model.getResponse(resultType=ResultType.OBJECT)
#Print object's variable
print(cat.fact)
```


**DataModel Example**
```python
from NetNode import *
#Initialize model
model = NetModelFactory.createModel(NetModelType.DATA, model="phi3")
#Create model response
model.createModelResponse("write one sentence cat fact about cat breeds.")
#Print results
print(model.getResponse(resultType=ResultType.STRING))
```


**Embedding Usage**
```python
from NetNode import *
#Initialize model
model = NetModelFactory.createModel(NetModelType.CHAT, model="phi3")
#Embed data
model_embed = NetModelFactory.createModel(NetModelType.EMBED, model="all-minilm")
emb = Embedder(model_embed, vector_base=SQLiteVectorBase(), n_ctx=512)
# Embed some text
emb.embed("Hello world", InputType.TEXT)
emb.embed("ArchNet uses ollama API.", InputType.TEXT)
# Embed a file
emb.embed("data.txt", InputType.FILE_PATH)

# Find best matches
result = emb.find_best_matches(prompt, 3)
data = ""
for match in result:
    data += emb.get_file_context_from_part(match[0], match[1]) + "\n"

ctx = ChatContext(512, 128)
ctx.setData(data)
ctx.setSystemPrompt("Using context, Answer the user's question.")
prompt = "What is ArchNet? Briefly."
ctx.history.push_message(ChatMessage(Sender.USER, prompt))
ctx.updateContext()
#Create model response
model.createModelResponse(ctx.context.getContextDict())
#Print results
print(model.getResponse(resultType=ResultType.STRING) + "\n")
```