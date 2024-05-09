import requests
import csv

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

def generate_balanz_fci_table(fci_id):
    url = 'https://balanz.com/api-web/v1/funds/history'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
    }
    data = f'{{"id":{fci_id}}}'

    response = requests.post(url, headers=headers, data=data)

    fci_ticker = balanz_fci_code_to_ticker[fci_id]
    csv_filename = f'{fci_ticker}_{fci_id}.csv'

    write_balanz_fci_api_response(response, csv_filename)
