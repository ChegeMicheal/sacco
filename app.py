from flask import Flask, render_template

#create a flask instance
app = Flask(__name__)

#create route decorator
@app.route('/')
def index():
    return "hello"