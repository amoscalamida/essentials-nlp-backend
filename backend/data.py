from flask import Blueprint, request


def append_to_file(text, canton):
    with open("data/new_data.csv", "a") as file1:
        # Writing data to a file
        file1.write(f'"{hash(text) * -1}", "{text}", "{canton}"\n')


bp = Blueprint("data", __name__, url_prefix="/data")


@bp.route("/save", methods=("GET", "POST"))
def predict():
    if request.method == "POST":
        print(request)
        request_data = request.get_json()
        phrase = request_data["text"]
        canton = request_data["canton"]
        append_to_file(phrase, canton)
        return "saved"

    return "nothing to see"
