from ollama import Client
from openai import OpenAI

class OllamaHost():
    """
    Represents a host for the Ollama service.

    Args:
        host (str): The base URL of the Ollama service. Defaults to "http://localhost:11434/v1".

    Attributes:
        _host (str): The base URL of the Ollama service.
        _openai (OpenAI): An instance of the OpenAI class.
        _client (Client): An instance of the Client class.

    """

    def __init__(self, host="http://localhost:11434/v1"):
        self._host = host
        self._openai = None
        self._client = None

    @property
    def openai(self):
        """
        Get an instance of the OpenAI class.

        Returns:
            OpenAI: An instance of the OpenAI class.

        """
        if self._openai is None:
            self._openai = OpenAI(base_url=self._host, api_key="Ollama")
        return self._openai

    @property
    def client(self):
        """
        Get an instance of the Client class.

        Returns:
            Client: An instance of the Client class.

        """
        if self._client is None:
            self._client = Client(host=self._host)
        return self._client

class ChatMessage(tuple):
    def __new__(cls, role, content):
        return super().__new__(cls, (role, f"{content}<|eot_id|>"))
    
class Options(dict):
    """
    A dictionary subclass representing the options for a model.

    Args:
        temperature (float): The temperature value for sampling.
        top_p (float): The top-p value for nucleus sampling.
        top_k (int): The top-k value for top-k sampling.
        repeat_penalty (float): The penalty value for repeating tokens.
        seed (int): The seed value for random number generation.
        num_ctx (int): The number of context tokens.
        num_pred (int): The number of predicted tokens.
        use_mlock (bool): Whether to use mlock for memory locking.
    """

    def __init__(self, temperature, top_p, top_k, repeat_penalty, seed, num_ctx, num_pred, use_mlock):
        super().__init__()
        self['temperature'] = temperature
        self['top_p'] = top_p
        self['top_k'] = top_k
        self['repeat_penalty'] = repeat_penalty
        self['seed'] = seed
        self['num_ctx'] = num_ctx
        self['num_predict'] = num_pred
        self['use_mlock'] = use_mlock



