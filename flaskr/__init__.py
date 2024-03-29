import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',           # change the secret key
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register init-db with the app
    from . import db
    db.init_app(app)

    # import and register auth.py
    from . import auth
    app.register_blueprint(auth.bp)

    # import and register tracker.py
    from . import tracker
    app.register_blueprint(tracker.bp)
    app.add_url_rule('/', endpoint='index')



    return app