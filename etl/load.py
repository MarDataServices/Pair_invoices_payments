import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import csv

load_dotenv()

def load_into_db(df: pd.DataFrame, name: str) -> None:
    db_url = os.getenv('DB_URL')  # e.g., postgres://user:pass@postgres:5432/etl
    if not db_url:
        raise ValueError("DB_URL is not set in .env")
    try:
        engine = create_engine(db_url)
        pd.DataFrame(df).to_sql(name, engine, if_exists='replace', index=True)
    except Exception as e:
        print(f"Failed to load data into postgres database: {e}")

"""
    Function for generating a simple csv report.
    Highlighting data that is missing from each transaction with '-'.
    If there hasn't been a transaction that matches a certain invoice for example,
    that invoice will not yet have a 'Transaction ID' tied to it in the report
"""
def generate_report(paired:pd.DataFrame, unmatched_invoices:pd.DataFrame, unmatched_payments:pd.DataFrame):
    with open('/opt/airflow/data/report.csv', 'w', newline='') as csv_file:
        fieldnames = ['Index', 'Invoice Number', 'Transaction ID', 'Total Amount']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        #Table for correctly paid invoices
        for i, p in enumerate(paired):
            writer.writerow({'Index' : i, 'Invoice Number': p['invoice_id'], 'Transaction ID': p['payment_id'], 'Total Amount': p['amount']})
        
        #Table for invoices that have either not been paid, or paid incorrectly
        writer.writerow({})
        for i, ui in enumerate(unmatched_invoices):
            writer.writerow({'Index': i, 'Invoice Number': ui.get('Invoice Number', ''), 'Transaction ID': '-', 'Total Amount': ui.get('Total Amount', '')})

        #Table for incorrect payments
        writer.writerow({})
        for i, up in enumerate(unmatched_payments):
            writer.writerow({'Index': i, 'Invoice Number': '-', 'Transaction ID': up.get('Transaction ID', '-'), 'Total Amount': up.get('Amount', '')})
        


    