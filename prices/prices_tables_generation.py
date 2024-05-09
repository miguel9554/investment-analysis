import requests
import csv
from datetime import datetime
import pandas as pd

# TODO fix format of this CSV
# TODO use csv, not pandas
def generate_MEP_table():

    # Generate URL with current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://mercados.ambito.com/dolarrava/mep/historico-general/01-01-2000/{current_date}'

    # download table
    response = requests.get(url)

    # Generate CSV
    pd.DataFrame([{"Fecha": date, "Referencia": buy} for (date, buy) in response.json()[1:]]).to_csv("cotizaciones_mep.csv", index=False)

def generate_balanz_fcis_table():
    # Here, we should iterate over all FCIs and generate each table

if __name__ == "__main__":
    #generate_MEP_table()
    generate_balanz_fci_table(11)
