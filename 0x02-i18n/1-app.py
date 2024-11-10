#!/usr/bin/env python3
"""
    Setup module for Babel
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration stuff here"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE ="en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/', strict_slashes=False)
def root():
    """Entry point to the flask app"""
    return render_template("1-index.html")


if __name__ == '__main__':
    app.run()
