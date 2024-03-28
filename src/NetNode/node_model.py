import os
from llama_cpp import Llama
from langchain.chains import LLMChain
from llama_cpp.llama_speculative import LlamaPromptLookupDecoding
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
import numpy as np
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

class LlamaModel:
    def __init__(self, filename="*Q4_K_M.gguf", n_ctx=1024, top_p=0.1, top_k=5, temperature=0.5, repetition_penalty=1.2, n_gpu_layers=-1, chat_format="chatml"):
        """
        Initialize the Llama model with the given parameters.
        
        Args:
            filename (str): Name of the file with the pretrained model.
            n_ctx (int): Max number of input tokens the model uses for predictions.
            top_p (float): Cumulative probability threshold for nucleus sampling (e.g., 0.1 for less diversity, 0.9 for more).
            top_k (int): Number of highest probability tokens considered for predictions (e.g., 0 for less diversity, 50 for more).
            temperature (float): Controls randomness of predictions (e.g., 0.01 for more deterministic, 1.0 for more random).
            repetition_penalty (float): Penalizes repeating tokens (e.g., 1.0 for no penalty, 2.0 for high penalty).
            n_gpu_layers (int): Number of model layers to run on the GPU (-1 for all layers).
            chat_format (str): Format of the chat data ("chatml").
            num_pred_tokens (int): Number of tokens to predict per step.
        """

        self.store = {}

        # Initialize the callback manager with a streaming stdout callback handler
        callback_manager = CallbackManager([])
        #callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        self.llama = Llama(
            model_path= os.path.join("models", filename),
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            callback_manager=callback_manager,
            verbose=False,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            f16_kv=True,
            seed=42,
            stop="[/INST]",
            chat_format="chatml",
            model_kwargs={
                'repetition_penalty': repetition_penalty,
                'do_sample': True,
            },
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "<s>[INST] You are a friendly assistant who answers brielfy. If you are wanted to do programming task, only write the code. [/INST]"),
                ("user", "<s>[INST] {input} [/INST]"),
            ]
        )
    
    def embed(self, text):
        """
        Generate an embedding for the given text.
        
        Args:
            text (str): The text to generate an embedding for.
        
        Returns:
            The embedding for the text.
        """
        if not isinstance(text, str):
            raise ValueError("Text must be a string.")
        return self.llama.embed(text)
        
    def calculate_similarity(self, text1, text2):
        """
        Calculate the cosine similarity between the embeddings of two texts.
        
        Args:
            text1 (str): The first text. Utf8 encoded.
            text2 (str): The second text. Utf8 encoded.
        
        Returns:
            The cosine similarity between the embeddings of the two texts.
        """
        embedding1 = self.embed(text1)
        embedding2 = self.embed(text2)
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    
    def generate_text(self, prompt):
        """Generate text based on the given prompt."""
        return self.llama(prompt)
    

    def generate_response(self, prompt, session_id):
        """
        Generate a response based on the given prompt and the conversation history.
        """


        llm_chain = LLMChain(prompt=self.prompt, llm=self.llama, verbose=False)

        for chunk in llm_chain.stream({"input": prompt}):
            print(chunk, end="", flush=True)


        return "Response generated."