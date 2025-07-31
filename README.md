# Example Airflow + Spark Application

This repository contains a minimal example showing how to use **Airflow**, **Python**, **SQL** and **Spark** together. The `src/airflow_app.py` file defines an Airflow DAG that:

1. Creates a SQLite table and inserts some sample records using Python/SQL.
2. Runs a small Spark job that doubles each value from the table.
3. Writes the Spark results back to SQLite.
4. Prints the contents of the new table.

## Running the example

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure the `AIRFLOW_HOME` environment variable is set. You can then initialize the Airflow database and start the webserver:
   ```bash
   export AIRFLOW_HOME=$(pwd)/airflow_home
   airflow db init
   airflow webserver &
   airflow scheduler &
   ```
3. Copy the DAG file to your Airflow `dags` folder (by default `airflow_home/dags`) and trigger it from the Airflow UI.

This is only a small demonstration, but it shows how these technologies can be used together in a data pipeline.
