#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    return "C " + text.replace("_", " ")


@app.route("/python", strict_slashes=False)
def python():
    return "Python is cool"


@app.route("/python/<text>", strict_slashes=False)
def Python_text(text):
    return "Python " + text.replace("_", " ")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
