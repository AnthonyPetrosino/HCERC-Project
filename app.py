from flask import Flask, render_template

app = Flask(__name__)

# Homepage 
@app.route("/")
def index():
    return("Hello World")