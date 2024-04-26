from .net_model import NetModel
from utils.tools import *

class ChatModel(NetModel):
    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client

    def setOptions(self, options):
        self.options = options

    def getModelResponse(self, context):
        stream = self.client.generate(
            model=self.model,
            prompt= context,
            images=[],
            stream=True,
            options=self.options,
            keep_alive='1m'
        )
        return stream

    def ChatInteractive(self):
        while True:
            prompt = input("You: ")
            if prompt.lower() == "exit":
                break
            try:
                print("AI: ", end='')
                self.printStream(self.getModelResponse(prompt))
            except Exception as e:
                print("An error occurred: ", str(e))

    def printStream(self, stream):
        timer = Timer()
        for chunk in stream:
            print(chunk['response'], end='', flush=True)
            if 'usage' in chunk:
                print(f"\nTokens used: {chunk['usage']['total_tokens']}")
        print()
        timer.print_time()