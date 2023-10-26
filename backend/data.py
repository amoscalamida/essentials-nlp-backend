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

    filter = request.args.get('filter', "all")
    try:
        conn = psycopg2.connect(database=os.environ['DB_NAME'], user=os.environ['DB_USER'], 
                            password=os.environ['DB_PWD'], host=os.environ['DB_HOST'], port=os.environ['DB_PORT']) 
    
        cur = conn.cursor()
        html = """
                <style>
                
                    h1 {
                        font-family: arial, sans-serif;
                    }
                    
                    table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                    }

                    td, th {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                    }

                    tr:nth-child(even) {
                    background-color: #dddddd;
                    }

                    form {
                        display: flex;
                        justify-content: space-between;
                        width: 100%;
                        margin: 20px 0px;
                    }

                    input[type=submit] {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-decoration: none;
                        margin: 4px 2px;
                        cursor: pointer;
                    }
                </style>
            """

        # add buttons to switch between the two tables
        html += "<form action='/data/show' method='get'>" \
                "<input type='submit' name='filter' value='show combined data'>" \
                "<input type='submit' name='filter' value='new-data'>" \
                "<input type='submit' name='filter' value='predictions'>" \
                "</form>"

        if filter == "new-data":
            html += "<h1>Showing New Data</h1>"
            cur.execute(f"SELECT * FROM new_data")
            result = cur.fetchall()
            conn.close()

            # format the output as a html table showing the data
            html += "<table><thead><tr><th>hash_id</th><th>text</th><th>canton</th></tr></thead><tbody>"
            for row in result:
                html += "<tr>"
                for col in row:
                    html += f"<td>{col}</td>"
                html += "</tr>"
            html += "</tbody></table>"

        elif filter == "predictions":
            html += "<h1>Showing Predictions</h1>"
            cur.execute(f"SELECT * FROM predictions")
            result = cur.fetchall()
            conn.close()

            # format the output as a html table showing the data
            html += "<table><thead><tr><th>hash_id</th><th>text</th><th>canton</th><th>certainty</th></tr></thead><tbody>"
            for row in result:
                html += "<tr>"
                for col in row:
                    html += f"<td>{col}</td>"
                html += "</tr>"
            html += "</tbody></table>"

        else:
            # show all data (join on hash_id)
            html += "<h1>Showing All Data</h1>"
            cur.execute("SELECT predictions.hash_id, predictions.text, predictions.canton, predictions.certainty, new_data.canton FROM predictions LEFT JOIN new_data ON new_data.hash_id = predictions.hash_id")
            result = cur.fetchall()
            conn.close()

            # format the output as a html table showing the data
            html += ("<table><thead><tr><th>hash_id</th><th>text</th><th>predicted canton</th><th>prediction "
                     "certainty</th><th>actual canton</th></tr></thead><tbody>")
            for row in result:
                html += "<tr>"
                for col in row:
                    html += f"<td>{col}</td>"
                html += "</tr>"
            html += "</tbody></table>"
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