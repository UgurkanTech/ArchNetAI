import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.EMBED, model="all-minilm")

emb = Embedder(model)

emb.embed_text("UgurkanTech is a computer engineer.")
emb.embed_text("ArchNetAI is a python library for AI.")
emb.embed_text("ArchNetAI uses ollama API.")
emb.embed_text("Hello world")

match, sim =  emb.search_text("What is Archnet?")

print(f"With similarity: {sim:.4f}, best match:\n{match}")

match, sim =  emb.search_text("What is used by Archnet?")

print(f"With similarity: {sim:.4f}, best match:\n{match}")
