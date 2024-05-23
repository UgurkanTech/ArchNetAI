from typing import override
from .net_model import NetModel
from utils.tools import *
from utils.model import *
from utils.response import *
from utils.chat_context import *

class ChatModel(NetModel):
    """
    Represents a chat model that interacts with a host and generates responses using a specified model.

    Args:
        host (Host): The host object representing the connection to the model server.
        model (str): The name or ID of the model to use for generating responses.

    Attributes:
        client (Client): The client object representing the connection to the model server.
        options (dict): The options to be used for generating responses.

    Methods:
        setOptions: Sets the options for generating responses.
        getModelResponse: Generates a response from the model given a context.
        ChatInteractive: Starts an interactive chat session with the model.
        printStream: Prints the generated response stream.

    """
    @override
    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client

        self.resultMask.addType(ResultType.STRING)
        self.resultMask.addType(ResultType.STREAM)
        self.resultMask.addType(ResultType.INTERACTIVE)
        

    @override
    def createModelResponse(self, context):
        """
        Generates a response from the model given a context.

        Args:
            context (str): The context or prompt for generating the response.

        """
        self.modelResponse = self.client.chat(
            model=self.model,
            messages= context,
            stream= self.options['stream'],
            options= {
                'temperature': self.options['temperature'],
                'top_k': self.options['top_k'],
                'top_p': self.options['top_p'],
                'repeat_penalty': self.options['repeat_penalty'],
                'seed': self.options['seed'],
                'num_ctx': self.options['num_ctx'],
                'num_predict': self.options['num_predict'],
                'use_mlock': self.options['use_mlock'],
            },
            keep_alive= self.options['keep_alive'],
        )
        self.isChat = True

    @override
    def getResponse(self, resultType):
        """
        Returns the result based on the specified type.

        """
        res = ResponseFactory(mask=self.resultMask)

        if resultType == ResultType.INTERACTIVE:
            return self._chatInteractive()
        else:
            return res.GenerateResponse(self.modelResponse, self.isChat, self.options.isStream(), resultType)

    def _chatInteractive(self):
        """
        Starts an interactive chat session with the model.

        The user can input prompts and receive responses from the model until they enter "exit".

        """
        if not self.options.isStream():
            print("Interactive chat is only available with stream enabled.")
            return
        
        context = ChatContext(self.options['num_ctx'], self.options['num_predict'])
        context.setSystemPrompt(self.options['system_prompt'])

        history = ChatHistory()
        while True:
            prompt = input("You: ")
            if prompt.lower() == "exit":
                break
            try:
                print("AI: ", end='')
                history.push_message(ChatMessage(Sender.USER, prompt))
                
                context.setHistory(history)
                context.updateContext()
                Debug.print("Context: ", context.context.getContextDict())
                self.createModelResponse(context.context.getContextDict())
                result = StreamResponse(self.modelResponse, self.isChat, self.options.isStream()).GetResult()
                history.push_message(ChatMessage(Sender.ASSISTANT, result))
            except Exception as e:
                print("An error occurred: ", str(e))