from NetNode import *


mistral= "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
tiny= "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"

llama_model = LlamaModel(
    repo_id = mistral,
    filename="*Q4_K_M.gguf",
    temperature=0.5,
    repetition_penalty=1.2,
)

instructor = NodeInstructor(llama_model)
text_block = """
Sure, here's a simple example of a web server in Python using the Flask framework. We'll create two files: app.py for the server logic and index.html for the HTML content.

app.py:

'''
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
'''
In this file, we create a Flask web server that serves the index.html file when the home route (/) is accessed.

templates/index.html:
'''
<!DOCTYPE html>
<html>
<head>
    <title>My Web Server</title>
    <style>
        body {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    <h1>Welcome to my web server!</h1>
</body>
</html>

In this file, we define the HTML content that will be served by the web server. We also include some CSS to style the page.

To run the server, you would navigate to the directory containing app.py in your terminal and run the command python app.py. Then, you can access the web server by navigating to http://localhost:5000 in your web browser.

'''



"""
instructor.extract_info(text_block)
