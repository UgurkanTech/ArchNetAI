from NetNode import *
DataModel
model = NetModelFactory.createModel(ModelType.INSTRUCTOR, model="phi3")


#options = Options(temperature=1, top_k=64, top_p=0.9, repeat_penalty=1.2, seed=-1, num_ctx=512, num_pred=64 , use_mlock=True)

#model.setOptions(options)

#model.setImage("image.png")


from pydantic import BaseModel

class Cat(BaseModel):
    fact: str

    def __str__(self):
        return f"Cat(fact='{self.fact}')"
    


model.setJSONBaseModel(Cat)

stream = model.getModelResponse("write a short cat fact about cat colors. fact=")

#model.printStream(stream)

print(model.getResponseResult(stream=stream))

exit()



#model.setJSONBaseModel(File)










exit()

while True:
    prompt = input("You: ")
    if prompt.lower() == "exit":
        break

    try:
        generated_text = model.generate_response(prompt)
        print("Assistant: ", generated_text)
    except Exception as e:
        print("An error occurred: ", str(e))

