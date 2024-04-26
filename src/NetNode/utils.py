class ChatMessage(tuple):
    def __new__(cls, role, content):
        return super().__new__(cls, (role, f"{content}<|eot_id|>"))
    




