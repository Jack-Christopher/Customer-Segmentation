import json
import random
import pandas as pd
import database as db
from datetime import datetime, timedelta


def delete_all():
    connection = db.connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM crm_lead")
    cursor.execute("DELETE FROM res_partner")
    cursor.execute("ALTER SEQUENCE crm_lead_id_seq RESTART WITH 1")
    cursor.execute("ALTER SEQUENCE res_partner_id_seq RESTART WITH 1")
    connection.commit()
    connection.close()


def insert_random_data(n_partners, n_leads):
    connection = db.connect()
    cursor = connection.cursor()

    ##############################################
    ####         Partner Generation           ####
    ##############################################

    contacts = pd.read_csv('https://raw.githubusercontent.com/LuisSante/Datasets/main/names.csv')
    # email = list(contacts['Email Address'])
    names = list(contacts['FirstName LastName'])
    job_positions = ['Sales', 'Marketing', 'Accounting', 'IT', 'Production', 'Logistics', 'Customer Service']
    country_ids = range(1, 251)

    data_partners = {}

    # insert partners
    for i in range(1, n_partners + 1):
        name = random.choice(names)
        credit_limit = random.randint(0, 1000000)
        function = random.choice(job_positions)
        country_id = random.choice(country_ids)
        cursor.execute("INSERT INTO res_partner (name, credit_limit, function, country_id) VALUES (%s, %s, %s, %s)", 
            (name, credit_limit, function, country_id))
        data_partners[i] = {'name': name, 'credit_limit': credit_limit, 'function': function, 'country_id': country_id}

    connection.commit()


    ##############################################
    ####            Lead Generation           ####
    ##############################################

    priorities = range(0, 3)
    stage_id = range(1, 4)
    partner_ids = range(1, n_partners+1)

    data_leads = {}

    # insert leads
    for i in range(1, n_leads + 1):
        partner_id = random.choice(partner_ids)
        partner_name = data_partners[partner_id]['name']
        lead_name = "Oportunidad - " + str(i)

        priority = str(random.choice(priorities))
        stage_id = str(random.choice(stage_id))
        expected_revenue = str(random.randint(500,50000)/10)
        probability = str(random.randint(300,980)/10)

        country_id = data_partners[partner_id]['country_id']

        date_open = datetime(random.randint(2015, 2021), random.randint(1, 12), random.randint(1, 28)).strftime('%Y-%m-%d')
        date_closed = datetime.strptime(date_open, '%Y-%m-%d') + timedelta(days=random.randint(0, 30), weeks=random.randint(0, 28))
        date_closed = date_closed.strftime('%Y-%m-%d')
        
        cursor.execute("INSERT INTO crm_lead (name, partner_id, priority, stage_id, expected_revenue, type, probability, country_id, date_open, date_closed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (lead_name, partner_id, priority, stage_id, expected_revenue, 'oportunity' , probability, country_id, date_open, date_closed))
        
        data_leads[i] = {'name': lead_name, 'partner_id': partner_id, 'priority': priority, 'stage_id': stage_id, 'expected_revenue': expected_revenue, 'probability': probability, 'country_id': country_id, 'date_open': date_open, 'date_closed': date_closed}

    connection.commit()

    # dump to json files
    with open('data_partners.json', 'w') as outfile:
        json.dump(data_partners, outfile, indent=4)
    with open('data_leads.json', 'w') as outfile:
        json.dump(data_leads, outfile, indent=4)


delete_all()
insert_random_data(50, 5000)
