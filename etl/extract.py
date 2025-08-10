import pandas as pd 

#Simple function that extracts data from a .csv(excel comma-delimited) file
def extract_data(csv_file):
    return pd.read_csv(csv_file)