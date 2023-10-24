import os
from flask import Flask
from backend.model import get_model
from flask_cors import CORS

# start with:
# flask --app backend run --debug




def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/(model|data)/.*": {"origins": "https://laughing-guacamole-jr5gwqg7x5q3p74g-3000.app.github.dev"}})

    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import model

    model.init_app(app)
    from . import predict
    from . import data

    app.register_blueprint(predict.bp)
    app.register_blueprint(data.bp)

    return app