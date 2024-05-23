from enum import Enum
import os
import json

class Sender(Enum):
    """
    Enum for the sender of the message.
    """
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    
    def __eq__(self, other):
        return other.value == self.value
    def __hash__(self):
        return self.value.__hash__()
    def __str__(self):
        return self.name

class ChatMessage:
    """
    Represents a chat message.

    Attributes:
        sender (Sender): The sender of the message.
        message (str): The content of the message.
        timestamp (str, optional): The timestamp of the message. Defaults to None.
    """

    def __init__(self, sender: Sender, message: str, timestamp: str = None):
        self.sender = sender
        self.message = message
        self.timestamp = timestamp

    def getDict(self):
        """
        Returns the chat message as a dictionary.

        Returns:
            dict: The chat message as a dictionary.
        """
        return {
            "role": self.sender.name.lower(),
            "content": self.message,
            "timestamp": self.timestamp
        }

    def getContextDict(self):
        """
        Returns the chat message without the timestamp as a dictionary.

        Returns:
            dict: The chat message without the timestamp as a dictionary.
        """
        return {
            "role": self.sender.name.lower(),
            "content": self.message
        }

    def __str__(self):
        """
        Returns a string representation of the chat message.

        Returns:
            str: A string representation of the chat message.
        """
        return "Time: " + str(self.timestamp) + " Sender: " + str(self.sender) + " Message: " + str(self.message)

    
class ChatHistory:

    def __init__(self):
        self.messages = []
        self.length = 0

    def push_message(self, message : ChatMessage):
        self.messages.append(message)
        self.length += 1

    
    #Pop the last message
    def pop_message(self):
        if self.length > 0:
            self.length -= 1
            return self.messages.pop()
        else:
            print("No messages to pop.")

    def get_messages(self):
        return self.messages
    
    def get_length(self):
        return self.length

    #Pop the first message
    def pop_first_message(self):
        if self.length > 0:
            self.length -= 1
            return self.messages.pop(0)
        else:
            print("No messages to pop.")
    
    def __str__(self):
        result = ""
        for message in self.messages:
            result += str(message) + "\n"
        return result
    
    def __iter__(self):
        return iter(self.messages)
    
    # For JSON serialization
    def getHistoryDict(self):
        return {
            "messages": [message.getDict() for message in self.messages],
            "length": self.length
        }
    
    # For using in the chat context
    def getContextDict(self):
        return [message.getContextDict() for message in self.messages]
    
    # For JSON deserialization
    def setHistoryDict(self, data):
        self.messages = [ChatMessage(Sender[message["role"].upper()], message["content"], message["timestamp"]) for message in data["messages"]]
        self.length = data["length"]

    def clear(self):
        self.messages = []
        self.length = 0


    def saveToFile(self, filename = "chat_history.json"):
            """
            Save the chat history to a file.

            Args:
                filename (str, optional): The name of the file to save the chat history to. Defaults to "chat_history.json".
            """

            try:
                with open(filename, 'w') as file:
                    json.dump(self.getHistoryDict(), file)
            except Exception as e:
                print("Error saving history to file.")
                print(e)
                return None
        

    def loadFromFile(self, filename="chat_history.json"):
        """
        Load chat history from a file.

        Args:
            filename (str, optional): The name of the file to load the chat history from. Defaults to "chat_history.json".

        """
        if not os.path.exists(filename):
            print("File does not exist. No history loaded.")
            return None
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.setHistoryDict(data)
        except Exception as e:
            print("Error loading history from file.")
            print(e)
            return None
        