#!/usr/bin/env python3
"""
    Infer timezone
"""
from flask import Flask, g, render_template, request
from flask_babel import Babel, gettext as _, format_datetime
from typing import Dict
from datetime import datetime
import pytz

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
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Inferes the correct timeozone"""
    requested_timezone = request.args.get('timezone', '').strip()
    if not requested_timezone and g.user:
        requested_timezone = g.user.get('timezone')
    try:
        return pytz.timezone(requested_timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', strict_slashes=False)
def root():
    """Entry point to the flask app"""
    user = None
    if g.user:
        user = g.user

    current_timezone = get_timezone()
    current_time = datetime.now(pytz.timezone(current_timezone))

    formatted_time = format_datetime(current_time)

    return render_template("index.html",
                           home_title=_("home_title"),
                           home_header=_("home_header"),
                           c_time=_("current_time_is",
                                    current_time=formatted_time),
                           user=user)


@app.before_request
def before_request():
    """Runs before request"""
    id_from_request = request.args.get('login_as', type=int)
    g.user = get_user(login_as=id_from_request)


if __name__ == '__main__':
    app.run()
