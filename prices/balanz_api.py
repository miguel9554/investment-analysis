import requests
import csv
import json
from datetime import datetime

def write_balanz_fci_api_response(response, filename):
    # Define the CSV fieldnames
    fieldnames = ['Date', 'Price']

    json_list = response.json()

    # Write the JSON data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data
        for obj in json_list:
            # Convert datetime string to datetime object
            date_time_obj = datetime.strptime(obj['Fecha'], '%Y-%m-%dT%H:%M:%S')
            # Extract only the date portion
            date_only = date_time_obj.date()
            # Write to CSV
            writer.writerow({'Date': date_only, 'Price': obj['ValorCuotaparte']})

def generate_balanz_fci_table(fci_id, filepath):
    url = 'https://balanz.com/api-web/v1/funds/history'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
    }
    data = f'{{"id":{fci_id}}}'

    response = requests.post(url, headers=headers, data=data)

    write_balanz_fci_api_response(response, filepath)

def get_funds_data():
    url = 'https://balanz.com/api-web/v1/funds/funds_data'

    headers = {
        'accept': 'application/json, text/plain, */*',
    }

    response = requests.get(url, headers=headers)

    return response.json()

def generate_funds_table(filepath):
    funds_data = get_funds_data()
    dump_json(funds_data, filepath)

def dump_json(json_data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def read_json(file_path):
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
    return json_data


def get_funds_id_to_ticker_mapping(filepath):
    funds_data = read_json(filepath)
    return extract_funds_id_to_ticker_mapping(funds_data)

def extract_funds_id_to_ticker_mapping(json_list):
    id_to_ticker_mapping = {}

    for fund in json_list:
        fund_id = fund.get("CodFondo")
        ticker = fund.get("NombreAbreviado")

        if fund_id is not None and ticker is not None:
            id_to_ticker_mapping[fund_id] = ticker

    return id_to_ticker_mapping
