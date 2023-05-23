from flask import Flask
app = Flask(__name__)
import bot

@app.route('/')
def hello_world():
    return 'Hello, World!'