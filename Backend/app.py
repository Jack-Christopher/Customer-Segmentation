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
    query = "SELECT * FROM res_partner"
    df = proc.get(query)
    return df.to_json(orient='records')


if __name__ == '__main__':
   app.run(debug = True)