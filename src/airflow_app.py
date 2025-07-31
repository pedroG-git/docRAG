from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sqlite3
import pandas as pd
from pyspark.sql import SparkSession

DB_PATH = '/tmp/example.db'

def create_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS numbers (num INTEGER)')
    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect(DB_PATH)
    for i in range(5):
        conn.execute('INSERT INTO numbers (num) VALUES (?)', (i,))
    conn.commit()
    conn.close()


def run_spark_job():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM numbers', conn)
    spark = SparkSession.builder.appName('ExampleSparkJob').getOrCreate()
    sdf = spark.createDataFrame(df)
    sdf = sdf.withColumn('double', sdf.num * 2)
    result = sdf.toPandas()
    result.to_sql('numbers_double', conn, if_exists='replace', index=False)
    conn.close()
    spark.stop()


def show_results():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM numbers_double', conn)
    print(df)
    conn.close()

with DAG(
    dag_id='example_python_sql_spark',
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id='create_table', python_callable=create_table)
    t2 = PythonOperator(task_id='insert_data', python_callable=insert_data)
    t3 = PythonOperator(task_id='run_spark_job', python_callable=run_spark_job)
    t4 = PythonOperator(task_id='show_results', python_callable=show_results)

    t1 >> t2 >> t3 >> t4
