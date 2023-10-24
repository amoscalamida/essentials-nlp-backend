from backend.model import get_model, encode_store, onehot_encode_data
from flask import Blueprint, request
import random
import numpy as np


def append_to_file(text, predicted_canton, prediction_certainty):
    with open("data/predictions.csv", "a") as file1:
        # Writing data to a file
        file1.write(
            f'"{hash(text) * -1}","{text}", "{predicted_canton}", {prediction_certainty}\n'
        )


bp = Blueprint("model", __name__, url_prefix="/model")


@bp.route("/predict", methods=("GET", "POST"))
def predict():
    if request.method == "POST":
        print(request)
        request_data = request.get_json()
        phrase = request_data["text"]
        model = get_model()
        # prediction = model.predict([phrase])

        # for development only. replace with actual model output
        # predicted_canton = random.choice(["zh", "lu", "so"])
        # prediction_certainty = str(prediction[0][0])

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

        # Load Model

        # Model Prediction
        dialects = ["LU", "BE", "ZH", "BS"]
        softmax_predictions = model.predict(X_pred)
        prediction = np.argmax(softmax_predictions)
        predicted_canton = f"{dialects[prediction]}"
        prediction_certainty = f"{softmax_predictions[0][prediction]:.2%}"
        print(f"{dialects[prediction]} ({softmax_predictions[0][prediction]:.2%})")
        result = {
            "canton": predicted_canton,
            "certainty": prediction_certainty,
        }
        # prediction = model.predict([phrase])
        append_to_file(phrase, predicted_canton, prediction_certainty)

        return result

    return "nothing to see"
