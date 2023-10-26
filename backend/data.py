from flask import Blueprint, request
import psycopg2
import os

def append_to_file(text, canton):
    try:
        conn = psycopg2.connect(database=os.environ['DB_NAME'], user=os.environ['DB_USER'], 
                            password=os.environ['DB_PWD'], host=os.environ['DB_HOST'], port=os.environ['DB_PORT']) 
    
        cur = conn.cursor()
        cur.execute(f"INSERT INTO new_data (hash_id, text, canton) VALUES ('{hash(text)}','{text}', '{canton}')")
        
        conn.commit()
        conn.close()
    except:
        print("DB connection failed")


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
