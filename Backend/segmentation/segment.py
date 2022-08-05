from processing import get 

query = "SELECT create_date, name, contact_name, country_id, expected_revenue, probability FROM crm_lead"

def QUERY():
    segment_ds = get(query)
    return segment_ds

dataset = QUERY()

dataset['probability'] = dataset['probability'].fillna(dataset['probability'].mean())
dataset['contact_name'] = dataset['contact_name'].fillna("Luis Sante")
dataset['expected_revenue'] = dataset['expected_revenue'].fillna(0)

for i in range(len(dataset['expected_revenue'])):
    if(dataset['expected_revenue'][i] == 0):
        dataset['expected_revenue'][i] = dataset['expected_revenue'][i] + dataset['probability'].mean()

print(dataset.isnull().sum())

print(dataset)

