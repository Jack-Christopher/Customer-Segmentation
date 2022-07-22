import os 
import sys
from flask import Flask, jsonify


app = Flask(__name__)
app.secret_key = 'very-secret-key'


@app.route('/')
def index():
    response = {'message': 'Hello World!'}
    return jsonify(response)


if __name__ == '__main__':
   app.run(debug = True)