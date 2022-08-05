from processing import get 

query = "SELECT create_date, name, contact_name, country_id, expected_revenue, probability FROM crm_lead"

def QUERY():
    segment_ds = get(query)
    return segment_ds

print(QUERY())