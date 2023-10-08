import keras
from flask import g
import click
import tensorflow as tf
import re
import string

# model from
# https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/keras/text_classification.ipynb#scrollTo=FWXsMvryuZuq


@keras.saving.register_keras_serializable()
def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    stripped_html = tf.strings.regex_replace(lowercase, "<br />", " ")
    return tf.strings.regex_replace(
        stripped_html, "[%s]" % re.escape(string.punctuation), ""
    )


def get_model():
    if "model" not in g:
        g.model = keras.models.load_model("./test.keras")
    return g.model


def init_db():
    db = get_model()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()


def init_app(app):
    app.cli.add_command(init_db_command)
