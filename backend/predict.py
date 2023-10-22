from backend.model import get_model
from flask import Blueprint, request
import random

def append_to_file(text):
    with open("data/new_data.txt", "a") as file1:
        # Writing data to a file
        file1.write(text + ";\n")


bp = Blueprint("model", __name__, url_prefix="/model")


@bp.route("/predict", methods=("GET", "POST"))
def predict():
    if request.method == "POST":
        print(request)
        request_data = request.get_json()
        phrase = request_data["text"]
        # append_to_file(phrase)
        model = get_model()
        prediction = model.predict([phrase])
        
        result = {
            "canton": random.choice(["zh", "lu", "so"]), # for development. replace with actual model output
            "certainty": str(prediction[0][0])
        }
        return result 

    return "nothing to see"
