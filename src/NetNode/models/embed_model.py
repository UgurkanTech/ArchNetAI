from typing import override
from .net_model import NetModel
from utils.tools import *
from utils.model import *
from utils.response import *

class EmbedModel(NetModel):
    @override
    def __init__(self, host, model):
        super().__init__(host, model)
        self.client = self.host.client
        self.resultMask.addType(ResultType.EMBEDDING)

    @override
    def createModelResponse(self, context):
        self.modelResponse = self.client.embeddings(
            model=self.model, 
            prompt=context,
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
            keep_alive= self.options['keep_alive']
        )
        self.isChat = False
