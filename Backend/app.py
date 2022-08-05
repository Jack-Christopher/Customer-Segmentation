from flask import Flask, request, jsonify, send_file
import utils.database as db
import utils.processing as proc

app = Flask(__name__)
app.secret_key = 'very-secret-key'


@app.route('/')
def index():
    response = {'message': 'Hello World!'}
    return jsonify(response)


@app.route('/partners', methods=['GET'])
def query():
    query = "SELECT create_date, name, contact_name, country_id, expected_revenue, probability FROM crm_lead"

    df = proc.get(query)
    print(df)
    return df.to_json(orient='records')


if __name__ == '__main__':
   app.run(debug = True)
