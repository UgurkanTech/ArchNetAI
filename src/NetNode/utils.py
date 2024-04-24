class ChatMessage(tuple):
    def __new__(cls, role, content):
        return super().__new__(cls, (role, f"{content}<|eot_id|>"))
    
import base64

class File():
    def convert_to_base64(file):
        with open(file, "rb") as image_file:
            str = base64.b64encode(image_file.read())
        return str
    
class Options(dict):
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

