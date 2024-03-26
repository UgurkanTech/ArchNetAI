from llama_cpp import Llama
from llama_cpp.llama_speculative import LlamaPromptLookupDecoding

class LlamaModel:
    def __init__(self, repo_id, filename, temperature, repetition_penalty):
        self.llama = Llama.from_pretrained(
            repo_id=repo_id,
            filename=filename,
            n_gpu_layers=-1,
            chat_format="chatml",
            n_ctx=1024,
            draft_model=LlamaPromptLookupDecoding(num_pred_tokens=2),
            logits_all=True,
            verbose=False,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
        )
    
    def embed(self, text):
        return self.llama.embed(text)
        
        