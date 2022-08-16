import numpy as np
import pandas as pd
import pandas.io.sql as psql
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from datetime import datetime
import matplotlib.pyplot as plt 
#import seaborn as sns
import database as db

def get(query):
    connection = db.connect()
    df = psql.read_sql(query, connection)
    connection.close()
    return df

# silhoutte method
def silhoutte(df, n_clusters):
    scores = []
    for k in range(2, n_clusters):
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=0).fit(df)
        labels = kmeans.labels_
        score = silhouette_score(df, labels)
        scores.append(score)

    max_score = max(scores)
    max_index = scores.index(max_score)
    n_clusters = max_index + 2
    return n_clusters


def cluster(df):
    n_clusters = silhoutte(df, 5)
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=0).fit(df)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    return labels, n_clusters, centers


def segment():
    partners = get( "SELECT id, name, credit_limit, function, country_id FROM res_partner")

    # rename id column to partner_id
    partners.rename(columns={'id': 'partner_id'}, inplace=True)
    partners['credit_limit'] = partners['credit_limit'].fillna(100000)

    standard = StandardScaler()    
    partners['credit_limit'] = standard.fit_transform(partners[['credit_limit']])
    partners['country_id'] = standard.fit_transform(partners[['country_id']])
    
    # encode function to numeric
    partners['function'] = partners['function'].astype('category')
    partners['function'] = partners['function'].cat.codes
    partners['country_id'] = partners['country_id'].fillna(100)

    #print(partners.isnull().sum())


    leads = get( "SELECT priority, expected_revenue, date_open, date_closed, probability, partner_id FROM crm_lead")

    leads['date_open'] = leads['date_open'].fillna("2015-07-14")
    leads['date_closed'] = leads['date_closed'].fillna("2015-10-10")
    leads['priority'] = leads['priority'].fillna(leads['priority'].mode()[0])    
    leads['expected_revenue'] = leads['expected_revenue'].fillna(0)

    leads['expected_revenue'] = leads['expected_revenue'].map(lambda x: x if x != 0 else x + leads['expected_revenue'].mean())
    # new column with date_closed - date_open
    diff = pd.to_datetime(leads['date_closed']) - pd.to_datetime(leads['date_open'])
    leads['date_diff'] = diff
    leads['date_diff'] = leads['date_diff'].dt.days
    leads['probability'] = leads['probability'].fillna(leads['probability'].mean())

    # aggregate leads by partner_id
    leads = leads.groupby('partner_id').agg({'priority': lambda x: x.value_counts().index[0], 'expected_revenue': 'mean', 'date_diff': 'mean', 'probability': 'mean'})
    leads.reset_index(inplace=True)
    
    # rename columns to avg
    leads.rename(columns={'priority': 'priority_mode', 'expected_revenue': 'expected_revenue_avg', 'date_diff': 'date_diff_avg', 'probability': 'probability_avg'}, inplace=True)

    # merge 
    partners = pd.merge(partners, leads, on='partner_id')

    #print(leads.isnull().sum())

    #########################
    ###      Cluster      ###
    #########################
    partners['cluster'], n_clusters, centers = cluster(partners[['country_id', 'credit_limit', 'function']])
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

    return partners, n_clusters, centers

def plot_clusters():
    
    dataframe, n_clusters, centers = segment() 
    columns_ = ['country_id', 'credit_limit', 'function']

    x = dataframe.loc[:, columns_]
    reduction = PCA(n_components=2)
    reduction_clusters = reduction.fit_transform(x) 

    ploteo = pd.DataFrame(data = reduction_clusters, 
                                columns = ['x', 'y'])
    ploteo['cluster'] = dataframe['cluster'] 
    

    '''fig, ax = plt.subplots()
    sns.scatterplot(x='x', y='y', data=ploteo.assign(cluster = ploteo['cluster']), hue='cluster', ax=ax)
    ax.set(title='K-Means Clustering');
    ax.scatter(centers[:, 0], centers[:, 1], marker='*', c='blue', s=100)'''

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('X', fontsize = 15)
    ax.set_ylabel('Y', fontsize = 15)
    ax.set_title('Customer Segmentation', fontsize = 20)
    
    targets = []
    for i in range(n_clusters):
        targets.append(i)
        
    for target in targets:
        indicesToKeep = ploteo['cluster'] == target

        ax.scatter(ploteo.loc[indicesToKeep, 'x'], 
                    ploteo.loc[indicesToKeep, 'y'], 
                    cmap = 'rainbow',
                    edgecolors = 'k',
                    s = 50)

    ax.legend(targets)
    ax.grid()

    plt.savefig("Clustering.png")


dataframe, nr_clusters , centers = segment()
plot_clusters()
print(dataframe)