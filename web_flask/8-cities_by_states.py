#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


@app.route("/cities_by_states")
def cities_by_states():
    """
    Display a HTML page with a list of states and cities
    """
    states = storage.all("State").values()
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(err):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
