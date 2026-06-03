import psycopg2
import pandas as pd

def get_connection():
    conn=psycopg2.connect(
    host="localhost",
    database="payment_reminder",
    user="postgres",
    password="Coders@2505",
    port="8586"
    )
    print("connected succsessfully")
    df=pd.read_sql("select*from customer_info",conn)
    print(df.head())
    return conn