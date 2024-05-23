import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.CHAT, model="phi3")

#Before embedding data.
prompt = "What is ArchNet? Briefly."
print("\nPrompt: " + prompt + "\n")
history = ChatHistory()
history.push_message(ChatMessage(Sender.USER, prompt))
model.createModelResponse(history.getContextDict())
print('\x1b[5;30;41m' + '=========== Before Embedding Data ===========' + '\x1b[0m')
print(model.getResponse(resultType=ResultType.STRING) + "\n")

#Embed data
model_embed = NetModelFactory.createModel(NetModelType.EMBED, model="all-minilm")
emb = Embedder(model_embed, vector_base=SQLiteVectorBase(), n_ctx=512)

# Embed some text
emb.embed("UgurkanTech is a computer engineer.", InputType.TEXT)
emb.embed("ArchNet uses ollama API.", InputType.TEXT)
emb.embed("Hello world", InputType.TEXT)
emb.embed("ArchNet is a python library for AI", InputType.TEXT)
emb.embed("Cooking some food in the kitchen.", InputType.TEXT)
emb.embed("I like to play basketball.", InputType.TEXT)
emb.embed("My name is Ugurkan.", InputType.TEXT)
# Embed a file
emb.embed("data.txt", InputType.FILE_PATH)

# Find best matches
result = emb.find_best_matches(prompt, 4) # List[(Embedding, EmbeddingPart, float)]
# Print results
data = ""
for match in result:
    print(f"Match: {match[0].id , match[1].index}, similarity: {match[2]:.4f}")
    data += emb.get_file_context_from_part(match[0], match[1]) + "\n"

ctx = ChatContext(512, 128)
ctx.setData(data)
ctx.setSystemPrompt("Using context, Answer the user's question.")
ctx.history.push_message(ChatMessage(Sender.USER, prompt))
ctx.updateContext()

model.createModelResponse(ctx.context.getContextDict())
print('\x1b[5;30;42m' + '=========== After Embedding Data ===========' + '\x1b[0m')
print(model.getResponse(resultType=ResultType.STRING) + "\n")
