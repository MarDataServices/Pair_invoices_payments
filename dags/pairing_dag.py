import sys
sys.path.insert(0, '/opt/airflow')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

#Import of functions in /etl
from etl.extract import extract_data
from etl.transform import compare_data
from etl.load import load_into_db, generate_report

"""
    Function that ties the project together.
    Retrieves invoice and payment data, compares data in the two datasets
    and then loads that data into a postgresql database.
    This data, aswell as other incomplete data, will be written in a report.
"""
def run_pipeline():
    invoices = extract_data('/opt/airflow/data/sample_invoices.csv')
    payments = extract_data('/opt/airflow/data/sample_payments.csv')
    
    paired, unpaired_invoices, unpaired_payments = compare_data(invoices, payments)
    load_into_db(paired, 'paired')
    generate_report(paired, unpaired_invoices, unpaired_payments)


#Run DAG and schedule operation to run once every minute.
with DAG('invoice-payment-pairing', start_date=datetime(2025,8,7), schedule_interval='*/1 * * * *', catchup=False):
    task = PythonOperator(
        task_id="etl_pipeline",
        python_callable=run_pipeline
    )

