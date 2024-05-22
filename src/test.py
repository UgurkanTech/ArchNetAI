from NetNode import *


Debug.setDebug(True)

mngr = ChatContext(512, 128)

mngr.setData("His name is John. You should ask him about his job. And don't forget to ask him about his family. Also, ask him about his hobbies.")

mngr.setSystemPrompt("You are a helpful ai assistant. Answer the following questions.")

history = ChatHistory()
msg = ChatMessage(Sender.USER, "Hello, how are you?", "2021-09-01 12:00:00")
msg2 = ChatMessage(Sender.ASSISTANT, "I am fine.", "2021-09-01 12:00:01")
msg3 = ChatMessage(Sender.USER, "What is your name? I wonder.", "2021-09-01 12:00:02")
history.push_message(msg)
history.push_message(msg2)
history.push_message(msg3)
mngr.setHistory(history=history)

mngr.updateContext()

#mngr.context.saveToFile("context.json")

