import requests
import csv
from datetime import datetime
import pandas as pd
from balanz_api import *

# TODO fix format of this CSV
# TODO use csv, not pandas
def generate_MEP_table(filepath):

    # Generate URL with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://mercados.ambito.com/dolarrava/mep/historico-general/01-01-2000/{current_date}'

    # download table
    response = requests.get(url)

    # Generate CSV
    pd.DataFrame([{"Fecha": date, "Referencia": buy} for (date, buy) in response.json()[1:]]).to_csv(filepath, index=False)

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
