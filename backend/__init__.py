import os
from flask import Flask
from backend.model import get_model
from flask_cors import CORS
import psycopg2
import os

# start with:
# flask --app backend run --debug


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(
        app,
        resources={
            r"/(model|data)/.*": {
                "origins": "https://seashell-app-xnkoa.ondigitalocean.app/"
            }
        },
    )

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

    # setup database tables if they don't exist yet
    setup_database()

    model.init_app(app)
    from . import predict
    from . import data

    app.register_blueprint(predict.bp)
    app.register_blueprint(data.bp)

    return app

def setup_database():
    try:
        conn = psycopg2.connect(database=os.environ['DB_NAME'], user=os.environ['DB_USER'], 
                                password=os.environ['DB_PWD'], host=os.environ['DB_HOST'], port=os.environ['DB_PORT'])
        cur = conn.cursor()

        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('predictions',))
        if not cur.fetchone()[0]:
            cur.execute("CREATE TABLE predictions (hash_id VARCHAR(255) PRIMARY KEY, text VARCHAR(255), canton VARCHAR(255), certainty FLOAT)")
            conn.commit()
        else:
            pass

        cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name=%s)", ('new_data',))
        if not cur.fetchone()[0]:
            cur.execute("CREATE TABLE new_data (hash_id VARCHAR(255) PRIMARY KEY, text VARCHAR(255), canton VARCHAR(255))")
            conn.commit()
        else:
            pass

        conn.close()
    except:
        print("DB connection failed")
    return
    