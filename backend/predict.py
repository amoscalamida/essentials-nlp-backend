from backend.model import get_model
from flask import Blueprint, request
import random


def append_to_file(text, predicted_canton, prediction_certainty):
    with open("data/predictions.csv", "a") as file1:
        # Writing data to a file
        file1.write(f'"{hash(text) * -1}","{text}", "{predicted_canton}", {prediction_certainty}\n')


bp = Blueprint("model", __name__, url_prefix="/model")


@bp.route("/predict", methods=("GET", "POST"))
def predict():
    if request.method == "POST":
        print(request)
        request_data = request.get_json()
        phrase = request_data["text"]
        model = get_model()
        prediction = model.predict([phrase])

        # for development only. replace with actual model output
        predicted_canton = random.choice(["zh", "lu", "so"])
        prediction_certainty = str(prediction[0][0])

        result = {
            "canton": predicted_canton,
            "certainty": prediction_certainty
        }
        append_to_file(phrase, predicted_canton, prediction_certainty)

        return result

    return "nothing to see"
