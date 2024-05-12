import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.EMBED, model="all-minilm")

emb = Embedder(model, vector_base=DictVectorBase(), n_ctx=512)

# Embed some text
emb.embed("UgurkanTech is a computer engineer.", InputType.TEXT)
emb.embed("ArchNetAI uses ollama API.", InputType.TEXT)
emb.embed("Hello world", InputType.TEXT)
# Embed long text
emb.embed("ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI. ArchNetAI is a python library for AI.", InputType.TEXT)
# Embed a file
emb.embed("data.txt", InputType.FILE_PATH)

# Find best matches
result = emb.find_best_matches("What is Archnet?", 3, "euclidean") # List[(Embedding, EmbeddingPart, float)]
# Print results
for match in result:
    print(f"Match: {match[0].id , match[1].index}, similarity: {match[2]:.4f}")
    print(f"Context: {emb.get_file_context_from_part(match[0], match[1])}")
    print("-----------------------------------------------------------------------")
    
#Debug virtio
emb.print_virtio()
#Debug vector base
emb.vector_base.print_db()