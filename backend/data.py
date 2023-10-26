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

@bp.route("/show", methods=["GET"])
def show_data():
    try:
        conn = psycopg2.connect(database=os.environ['DB_NAME'], user=os.environ['DB_USER'], 
                            password=os.environ['DB_PWD'], host=os.environ['DB_HOST'], port=os.environ['DB_PORT']) 
    
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM new_data")
        result = cur.fetchall()
        conn.close()

        
        # format the output as a html table showing the data
        html = "<table><tr><th>hash_id</th><th>text</th><th>canton</th></tr>"
        for row in result:
            html += "<tr>"
            for col in row:
                html += f"<td>{col}</td>"
            html += "</tr>"
        html += "</table>"
        return html
    except:
        print("DB connection failed")
        return "DB connection failed"
    
@bp.route("/show-predictions", methods=["GET"])
def show_predictions():
    try:
        conn = psycopg2.connect(database=os.environ['DB_NAME'], user=os.environ['DB_USER'], 
                            password=os.environ['DB_PWD'], host=os.environ['DB_HOST'], port=os.environ['DB_PORT'])
        
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM predictions")
        result = cur.fetchall()
        conn.close()


        # format the output as a html table showing the data
        html = "<table><tr><th>hash_id</th><th>text</th><th>canton</th><th>certainty</th></tr>"
        for row in result:
            html += "<tr>"
            for col in row:
                html += f"<td>{col}</td>"
            html += "</tr>"
        html += "</table>"

        return html
    except:
        print("DB connection failed")
        return "DB connection failed"