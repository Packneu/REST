import os

from flask import Flask
from . import db
from . import auth
from . import auction
from . import paypal
from . import user


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join('sovaa/db.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(auction.bp)
    app.register_blueprint(paypal.bp)
    app.register_blueprint(user.bp)
    app.add_url_rule('/', endpoint='index')

    return app