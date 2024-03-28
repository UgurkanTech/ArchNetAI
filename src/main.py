import numpy as np
from NetNode import *




mistral= "mistral-7b-instruct-v0.2.Q4_K_M.gguf"

model = LlamaModel(
    filename= mistral
)


while True:
    prompt = input("You: ")
    if prompt.lower() == "exit":
        break

    try:
        generated_text = model.generate_response(prompt, "1")
        print("Assistant: ", generated_text)
    except Exception as e:
        print("An error occurred: ", str(e))


#instructor = NodeInstructor(model)

#instructor.extract_info(text_block)
