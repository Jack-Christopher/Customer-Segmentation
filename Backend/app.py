from flask import Flask, request, jsonify, send_file
import segmentation.database as db
import segmentation.segment as seg
import json

app = Flask(__name__)
app.secret_key = 'very-secret-key'


@app.route('/')
def index():
    response = {'message': 'Hello World!'}
    return jsonify(response)


@app.route('/partners', methods=['GET'])
def query():
    query = "SELECT create_date, name, contact_name, country_id, expected_revenue, probability FROM crm_lead"
    df = seg.get(query)
    return df.to_json(orient='records')


@app.route('/segmentation', methods=['GET'])
def segmentation():
    df, k = seg.leads()
    data = df.to_json(orient='records')
    total = {'n_clusters': k, 'data': data}
    # convert to json
    return str(total)


if __name__ == '__main__':
   app.run(debug = True)
