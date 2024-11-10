#!/usr/bin/env python3
"""
    Different locale based on params or user settings
"""
from flask import Flask, g, render_template, request
from flask_babel import Babel, gettext as _
from typing import Dict

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(login_as: int) -> Dict:
    if not login_as or login_as not in users:
        return None
    user = users.get(login_as)
    return user


class Config:
    """Configuration stuff here"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Retrives best matcg lingo from request"""
    requested_locale = request.args.get("locale")
    if requested_locale in app.config['LANGUAGES']:
        return requested_locale

    if g.get('user') and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def root():
    """Entry point to the flask app"""
    user = None
    if g.user:
        user = g.user
    return render_template("5-index.html",
                           home_title=_("home_title"),
                           home_header=_("home_header"),
                           user=user)


@app.before_request
def before_request():
    """Runs before request"""
    id_from_request = request.args.get('login_as', type=int)
    g.user = get_user(login_as=id_from_request)


if __name__ == '__main__':
    app.run()
