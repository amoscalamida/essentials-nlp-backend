from backend.model import get_model, encode_store, onehot_encode_data
from flask import Blueprint, request
import os
import psycopg2
import numpy as np


def append_to_file(text, predicted_canton, prediction_certainty):

    try:
        conn = psycopg2.connect(
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PWD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
        )

        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO predictions (hash_id, text, canton, certainty) VALUES ('{hash(text)}','{text}', '{predicted_canton}', {prediction_certainty})"
        )

        conn.commit()
        conn.close()
    except:
        print("DB connection failed")
        

bp = Blueprint("model", __name__, url_prefix="/model")


@bp.route("/predict", methods=("GET", "POST"))
def predict():
    if request.method == "POST":
        print(request)
        request_data = request.get_json()
        phrase = request_data["text"]
        model = get_model()

        INPUT_STRING = phrase
        # Encode Input String
        X_pred = encode_store(input_str=INPUT_STRING)
        vocab_size = (
            36  # X_pred.max()  # NB: 0 is not in the vocabulary, but is padding
        )
        seq_length = X_pred.shape[1]
        print("Vocabulary size, sequence length: %d, %d" % (vocab_size, seq_length))
        X_pred = onehot_encode_data(X_pred, vocab_size)
        print("Encoded Input String.")
        dialects = ["LU", "BE", "ZH", "BS"]
        softmax_predictions = model.predict(X_pred)
        prediction = np.argmax(softmax_predictions)
        predicted_canton = f"{dialects[prediction]}"
        prediction_certainty = f"{softmax_predictions[0][prediction]}"
        print(f"{dialects[prediction]} ({softmax_predictions[0][prediction]:.2%})")
        result = {
            "canton": predicted_canton,
            "certainty": prediction_certainty,
        }
        append_to_file(phrase, predicted_canton, prediction_certainty)

        return result

    return "nothing to see"
