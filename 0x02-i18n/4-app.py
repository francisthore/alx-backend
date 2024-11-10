#!/usr/bin/env python3
"""
    Setup module for Babel paremetize
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext as _


class Config:
    """Configuration stuff here"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Retrives best matcg lingo from request"""
    requested_locale = request.args.get("locale")
    if requested_locale in app.config['LANGUAGES']:
        return requested_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def root() -> str:
    """Entry point to the flask app"""
    return render_template("4-index.html",
                           home_title=_("home_title"),
                           home_header=_("home_header"))


if __name__ == '__main__':
    app.run()
