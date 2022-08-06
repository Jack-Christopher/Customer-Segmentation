import numpy as np
import pandas as pd
import pandas.io.sql as psql
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import segmentation.database as db


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


def leads():
    dataset = get( "SELECT create_date, name, contact_name, country_id, expected_revenue, probability FROM crm_lead")
    # dataset = get( "SELECT country_id, expected_revenue, probability FROM crm_lead")

    dataset['probability'] = dataset['probability'].fillna(dataset['probability'].mean())
    dataset['contact_name'] = dataset['contact_name'].fillna("Luis Sante")
    dataset['expected_revenue'] = dataset['expected_revenue'].fillna(0)
    # using for loop
    # for i in range(len(dataset['expected_revenue'])):
    #     if(dataset['expected_revenue'][i] == 0):
    #         dataset['expected_revenue'][i] = dataset['expected_revenue'][i] + dataset['probability'].mean()

    # using map to replace 0 with mean of probability
    dataset['expected_revenue'] = dataset['expected_revenue'].map(lambda x: x if x != 0 else x + dataset['probability'].mean())

    dataset['cluster'], n_clusters = cluster(dataset[['country_id', 'expected_revenue', 'probability']])

    return dataset, n_clusters



