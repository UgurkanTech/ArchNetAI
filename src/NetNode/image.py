from utils import File

from ollama import Client
client = Client(host='http://localhost:11434')

client.pull(model='llava')

str = File.convert_to_base64("numan.png")

stream = client.chat(
    model='llava',
    messages=[{
        'role': 'user',
        'content': 'Explain this screenshot image briefly.',
        'images': [str],
        'temperature': 0,
        }],
    stream=True,
)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)





