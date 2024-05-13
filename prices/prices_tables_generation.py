import requests
import csv
from datetime import datetime
from balanz_api import *

def generate_MEP_table(filepath):
    # Generate URL with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://mercados.ambito.com/dolarrava/mep/historico-general/01-01-2000/{current_date}'

    # Download table
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()

        # Extract data from response
        dates = [row[0] for row in data[1:]]
        prices = [float(row[1].replace(',', '.')) for row in data[1:]]  # Replace commas with dots and convert to floats

        # Write data to CSV file
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Price'])  # Rename columns
            writer.writerows(zip(dates, prices))
    else:
        print("Failed to retrieve data from the URL.")

def generate_balanz_fcis_table(funds_data_filepath):
    # Here, we should iterate over all FCIs and generate each table
    mapping = get_funds_id_to_ticker_mapping(funds_data_filepath)
    for fund_id in mapping:
        filepath = f'balanz_fcis/{mapping[fund_id]}_{fund_id}.csv'
        generate_balanz_fci_table(fund_id, filepath)

if __name__ == "__main__":
    generate_MEP_table("dolar/mep.csv")
    balanz_funds_table_filepath = "balanz_fcis/balanz_funds_data.json"
    generate_funds_table(balanz_funds_table_filepath)
    generate_balanz_fcis_table(balanz_funds_table_filepath)
