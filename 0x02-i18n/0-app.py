#!/usr/bin/env python3
"""
    Flask app entry point module
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    """Entry pooiint to the flask app"""
    return render_template("0-index.html")


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
