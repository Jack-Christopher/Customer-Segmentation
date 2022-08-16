import sys
sys.path.insert(0, 'segmentation')

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
import database as db
import segment as seg
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'very-secret-key'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    response = {'message': 'Hello World!'}
    return jsonify(response)


@app.route('/partners', methods=['GET'])
def partners():
    query = "SELECT name, function, credit_limit, country_id FROM res_partner"
    df = seg.get(query)
    return df.to_json(orient='records')

@app.route('/leads', methods=['GET'])
def leads():
    query = "SELECT name, priority, country_id, expected_revenue, probability, date_open, date_closed FROM crm_lead"
    df = seg.get(query)
    
    df['date_open'] = df['date_open'].astype(str)
    df['date_closed'] = df['date_closed'].astype(str)

    return df.to_json(orient='records')

@app.route('/metrics', methods=['GET'])
def metrics():
    leads = "SELECT name, priority, country_id, expected_revenue, probability, date_open, date_closed FROM crm_lead"
    df_leads = seg.get(leads)

    # get metrics from dataframe
    prob_avg = round(df_leads['probability'].mean(), 2)
    exp_avg = df_leads['expected_revenue'].mean()
    exp_total = round(df_leads['expected_revenue'].sum(), 2)
    

    partners = "SELECT name, function, credit_limit, country_id FROM res_partner"
    df_partners = seg.get(partners)

    # get metrics from dataframe
    credit_avg = df_partners['credit_limit'].mean()
    function_mode = df_partners['function'].mode()[0]
    
    data = {
        'prob_avg': prob_avg,
        'exp_avg': exp_avg,
        'exp_total': exp_total,
        'credit_avg': credit_avg,
        'function_mode': function_mode
    }

    return jsonify(data)

@app.route('/history', methods=['GET'])
@cross_origin()
def history():
    query = "SELECT date_open FROM crm_lead"
    df = seg.get(query)
    # get the last 6 years of data
    df = df[df['date_open'] > datetime(datetime.now().year - 6, 1, 1)]
    # add year column
    df['year'] = df['date_open'].dt.year
    # get the number of leads per year and rename it to 'n_leads'
    df = df.groupby(['year']).count()
    # add id column
    df['year'] = df.index
    return df.to_json(orient='records')

@app.route('/last_year', methods=['GET'])
@cross_origin()
def last_year():
    query = "SELECT expected_revenue, date_open FROM crm_lead"
    df = seg.get(query)
    # get the last year of data
    df = df[df['date_open'] > datetime(datetime.now().year - 1, 1, 1)]
    print(df)
    # get the expected revenue, group by month 
    df = df.groupby([df['date_open'].dt.month]).sum()
    # add id column
    df['month'] = df.index
    return df.to_json(orient='records')
    


@app.route('/segmentation', methods=['GET'])
def segmentation():
    df, k, centers = seg.segment()
    data = df.to_json(orient='records')
    total = {'n_clusters': k, 'centers': centers, 'data': data}
    # convert to json
    return str(total)


@app.route('/plot', methods=['GET'])
def plot():
    seg.plot_clusters()
    return send_file('static/img/Clustering.png', mimetype='image/png')

if __name__ == '__main__':
   app.run(debug = True)
