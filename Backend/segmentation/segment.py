import numpy as np
import pandas as pd
import pandas.io.sql as psql
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import database as db

def get(query):
    connection = db.connect()
    df = psql.read_sql(query, connection)
    connection.close()
    return df

# silhoutte method
def silhoutte(df, n_clusters):
    scores = []
    for k in range(2, n_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(df)
        labels = kmeans.labels_
        score = silhouette_score(df, labels)
        scores.append(score)

    max_score = max(scores)
    max_index = scores.index(max_score)
    n_clusters = max_index + 2
    return n_clusters


def cluster(df):
    n_clusters = silhoutte(df, 10)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df)
    labels = kmeans.labels_
    return labels, n_clusters


def segment():
    partners = get( "SELECT id, name, credit_limit, function, country_id FROM res_partner")

    # rename id column to partner_id
    partners.rename(columns={'id': 'partner_id'}, inplace=True)

    standard = StandardScaler()    
    partners['credit_limit'] = standard.fit_transform(partners[['credit_limit']])
    partners['country_id'] = standard.fit_transform(partners[['country_id']])
    
    # encode function to numeric
    partners['function'] = partners['function'].astype('category')
    partners['function'] = partners['function'].cat.codes



    leads = get( "SELECT priority, expected_revenue, date_open, date_closed, probability, partner_id FROM crm_lead")

    leads['priority'] = leads['priority'].fillna(leads['priority'].mode()[0])    
    leads['expected_revenue'] = leads['expected_revenue'].fillna(0)
    leads['expected_revenue'] = leads['expected_revenue'].map(lambda x: x if x != 0 else x + leads['expected_revenue'].mean())
    # new column with date_closed - date_open
    leads['date_diff'] = leads['date_closed'] - leads['date_open']
    leads['date_diff'] = leads['date_diff'].dt.days
    leads['probability'] = leads['probability'].fillna(leads['probability'].mean())

    # aggregate leads by partner_id
    leads = leads.groupby('partner_id').agg({'priority': lambda x: x.value_counts().index[0], 'expected_revenue': 'mean', 'date_diff': 'mean', 'probability': 'mean'})
    leads.reset_index(inplace=True)
    
    # rename columns to avg
    leads.rename(columns={'priority': 'priority_mode', 'expected_revenue': 'expected_revenue_avg', 'date_diff': 'date_diff_avg', 'probability': 'probability_avg'}, inplace=True)

    # merge 
    partners = pd.merge(partners, leads, on='partner_id')

    #########################
    ###      Cluster      ###
    #########################
    partners['cluster'], n_clusters = cluster(partners[['country_id', 'credit_limit', 'function']])
    partners = partners.sort_values(by="cluster")
    partners = partners.reset_index(drop=True)

    # round values
    partners['credit_limit'] = partners['credit_limit'].round(2)
    partners['expected_revenue_avg'] = partners['expected_revenue_avg'].round(2)
    partners['date_diff_avg'] = partners['date_diff_avg'].round(2)
    partners['probability_avg'] = partners['probability_avg'].round(2)
    partners['country_id'] = partners['country_id'].round(2)
    # partners['priority_avg'] = partners['priority_avg'].round(2)

    # delete partner_id column
    partners.drop(columns=['partner_id'], inplace=True)

    return partners, n_clusters

# df,c = segment()
# print(df)