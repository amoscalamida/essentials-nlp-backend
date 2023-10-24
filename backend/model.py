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


import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences
from collections import defaultdict, Counter
import numpy as np
import os

#
# helper functions
#
char_replacement = {
    "é": "e1",
    "è": "e2",
    "ẽ": "e3",
    "ò": "o2",
    "õ": "o2",
    "ú": "u1",
    "ù": "u2",
    "à": "a2",
    "ã": "a3",
    "ǜ": "ü2",
    "ì": "i2",
}


def replace_ngraphs(s):
    for old, new in [("sch", "8"), ("ch", "9")]:
        s = s.replace(old, new)
    return s


def replaced(s):
    return "".join(char_replacement.get(c, c) for c in replace_ngraphs(s))


#
# data encoding
#
padding = "pre"
truncating = "post"


def encode_data(
    X,
    encoder,
    maxlen,
    fit=False,
    padding=padding,
    truncating=truncating,
    padding_value=0,
):
    # `fit=True` for training, `fit=False` otherwise
    # for production: better intelligently replace chars not in encoder
    return pad_sequences(
        (
            [[encoder[c] for c in s] for s in X]
            if fit
            else
            # in dev and test, if char not in encoder, ignore it
            [[encoder[c] for c in s if c in encoder] for s in X]
        ),
        maxlen=maxlen,
        dtype="int32",
        padding=padding,
        truncating=truncating,
        value=padding_value,
    )


def decoder(enc):
    return dict((v, k) for k, v in enc.items())


def encode_store(input_str, maxlen=70, model_dir=False):
    # one hot encode characters
    encoder = defaultdict()
    encoder.default_factory = encoder.__len__
    padding_value = encoder["#"]
    assert padding_value == 0

    # encoder data
    # prepend with a padding value, truncate long sequences at the end
    encoder = dict(
        {
            "#": 0,
            "u": 1,
            "2": 2,
            "n": 3,
            "d": 4,
            " ": 5,
            "e": 6,
            "t": 7,
            "h": 8,
            "m": 9,
            "g": 10,
            "\u00e4": 11,
            "l": 12,
            "r": 13,
            "i": 14,
            "o": 15,
            "9": 16,
            "b": 17,
            "8": 18,
            "s": 19,
            "a": 20,
            "\u00f6": 21,
            "v": 22,
            "w": 23,
            "p": 24,
            "z": 25,
            "f": 26,
            "\u00fc": 27,
            "k": 28,
            "j": 29,
            "1": 30,
            "\u0303": 31,
            "\u0300": 32,
            "3": 33,
            "x": 34,
            "q": 35,
            "c": 36,
        }
    )
    print("# chars %d" % len(encoder))

    # replace special chars of input string
    replaced_string = replaced(input_str)

    # encode input string
    X_pred = encode_data([replaced(replaced_string)], encoder, maxlen)

    return X_pred


# one-hot encode data as dense vectors
def onehot_encode_data(X, vocab_size):
    num_samples, num_timesteps = X.shape
    X_enc = np.zeros((num_samples, num_timesteps, vocab_size), dtype=np.int8)
    # how to do it with numpy indexing?
    for i in (
        (s, t, f - 1) for s in range(num_samples) for t, f in enumerate(X[s]) if f != 0
    ):
        X_enc[i] = 1
    return X_enc


#
# Main Script
#


def get_model():
    if "model" not in g:
        g.model = tf.keras.models.load_model("./my_model.keras")
    return g.model


def init_db():
    db = get_model()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()


def init_app(app):
    app.cli.add_command(init_db_command)
