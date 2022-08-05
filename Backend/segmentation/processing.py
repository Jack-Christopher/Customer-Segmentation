import database as db
import pandas.io.sql as psql

def get(query):
    connection = db.connect()
    df = psql.read_sql(query, connection)
    connection.close()
    return df
