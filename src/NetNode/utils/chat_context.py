import math
from .chat import ChatHistory, ChatMessage, Sender
from .debugger import Debug

class ChatContext:
    """
    Represents the context of a chat conversation.

    Attributes:
        n_ctx (int): The maximum number of tokens in the context.
        n_pred (int): The number of tokens to predict.
        context (ChatHistory): The chat history context.
        data (str): The user input data.
        system (str): The system prompt.
        history (ChatHistory): The chat history.

    Methods:
        getTokenCount(historyDict): Returns the token count of a given history dictionary.
        getCurrentSize(): Returns the current token count in the context.
        getFreeSpace(): Returns the remaining free space in the context.
        getTotalSize(): Returns the total token count of the context.
        setEmpty(): Clears the chat history context.
        isFull(): Checks if the context is full.
        setData(data): Sets the user input data.
        setSystemPrompt(system): Sets the system prompt.
        setHistory(history): Sets the chat history.
        updateContext(): Updates the chat context by processing the data and history.
    """

    def __init__(self, n_ctx, n_pred):
        """
        Initializes a new instance of the ChatContext class.

        Args:
            n_ctx (int): The maximum number of tokens in the context.
            n_pred (int): The number of tokens to predict.
        """
        self.n_ctx = n_ctx
        self.n_pred = n_pred
        self.context = ChatHistory()

        self.data = ""
        self.system = ""
        self.history = None
    
    def getTokenCount(self, historyDict : dict):
        """
        Returns the token count of a given history dictionary.

        Args:
            historyDict (dict): The history dictionary.

        Returns:
            int: The token count.
        """
        count = 0
        for message in historyDict:
            count += len(message["content"].split())
        return count
    
    def getCurrentSize(self):
        """
        Returns the current token count in the context.

        Returns:
            int: The current token count.
        """
        return self.getTokenCount(self.context.getContextDict())
    
    def getFreeSpace(self):
        """
        Returns the remaining free space in the context.

        Returns:
            int: The free space.
        """
        return self.n_ctx - self.getTokenCount(self.context.getContextDict())
    
    def getTotalSize(self):
        """
        Returns the total token count of the context.

        Returns:
            int: The total token count.
        """
        return self.n_ctx

    def setEmpty(self):
        """
        Clears the chat history context.
        """
        self.context.clear()

    def isFull(self):
        """
        Checks if the context is full.

        Returns:
            bool: True if the context is full, False otherwise.
        """
        return self.getFreeSpace() == 0

    def setData(self, data : str = ""):
        """
        Sets the user input data.

        Args:
            data (str, optional): The user input data. Defaults to "".
        """
        self.data = data

    def setSystemPrompt(self, system : str):
        """
        Sets the system prompt.

        Args:
            system (str): The system prompt.
        """
        self.system = system

    def setHistory(self, history : ChatHistory):
        """
        Sets the chat history.

        Args:
            history (ChatHistory): The chat history.
        """
        self.history = history

    def updateContext(self):
        """
        Updates the chat context by processing the data and history.
        """
        Debug.print("Updating Context...")
        self.context.clear()
        space = self.getFreeSpace() - self.n_pred
        Debug.print("Initial Context Space: ", space)

        if self.system:
            system = self.system
            self.context.push_message(ChatMessage(Sender.SYSTEM, system))

        if self.history:
            if self.history.get_length() > 0:
                chat = self.history.getContextDict()

        space = self.getFreeSpace() - self.n_pred
        Debug.print("After System Context Space: ", space)

        if self.data:
            data_rate = 0.5
        else:
            data_rate = 0.0

        dataSpace = int(math.floor(space * data_rate))

        historySpace = space - dataSpace

        Debug.print("Data Space: ", dataSpace, " History Space: ", historySpace)

        data_length = len(self.data.split())
        if dataSpace > 0:
            if data_length > dataSpace:
                data_tokens = self.data.split()
                data_splitted = " ".join(data_tokens[:dataSpace])
                self.context.push_message(ChatMessage(Sender.USER, data_splitted))
                Debug.print("Data trimmed. dataSpace: ", dataSpace, " dataSize: ", len(self.data.split()))
                dataSpace = 0
            else:
                self.context.push_message(ChatMessage(Sender.USER, self.data))

            
        #Reverse loop to get last message first. then reorder.
        temp_messages = []
        for message in chat[::-1]:
            message_length = len(message["content"].split())
            if message_length > historySpace:
                message_tokens = message["content"].split()
                message_splitted = " ".join(message_tokens[:historySpace])
                temp_messages.append(ChatMessage(Sender[message["role"].upper()], message_splitted))
                Debug.print("History trimmed. historySpace: ", historySpace, " historySize: ", message_length)
                historySpace = 0
                break
            else:
                historySpace -= message_length
                temp_messages.append(ChatMessage(Sender[message["role"].upper()], message["content"]))
                if historySpace == 0:
                    Debug.print("History Space is full. Skipping the rest.")
                    break


        #Reverse the order back
        for message in temp_messages[::-1]:
            self.context.push_message(message)

        space = self.getFreeSpace() - self.n_pred
        Debug.print("End Context Space: ", space)
        Debug.print("Context Updated.")
