import os
import re
from datetime import datetime
import csv

def get_fci_price(ticker, date):
    mapping = get_ticker_to_filepath_mapping('balanz_fcis')
    try:
        filepath = mapping[ticker]
    except KeyError:
        print(f'Prices table for ticker {ticker} not found')
    price = get_price_for_date(filepath, date.date())
    return price

def get_price_for_date(csv_file, target_date):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        prices = {}  # Dictionary to store dates and corresponding prices
        for row in reader:
            row_date = datetime.strptime(row['Date'], '%Y-%m-%d').date()
            prices[row_date] = float(row['Price'])  # Convert price to float
        dates = sorted(prices.keys())  # Sort dates
        if target_date in prices:
            return prices[target_date]
        else:
            # Find the closest dates before and after the target date
            closest_date_before = max(date for date in dates if date < target_date)
            closest_date_after = min(date for date in dates if date > target_date)

            # Get the prices for the closest dates
            price_before = prices[closest_date_before]
            price_after = prices[closest_date_after]

            # Linear interpolation
            # Linear interpolation
            time_interval = (closest_date_after - closest_date_before).days
            next_weight = (closest_date_after - target_date).days / time_interval
            prev_weight = 1 - next_weight
            interpolated_price = price_before * next_weight + price_after * prev_weight
            return interpolated_price

def get_ticker_to_filepath_mapping(directory):
    pattern = re.compile(r'^([a-zA-Z]+)_\d+\.csv$')
    ticker_filepath_map = {}

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            ticker = match.group(1)
            filepath = os.path.join(directory, filename)
            if ticker not in ticker_filepath_map:
                ticker_filepath_map[ticker] = filepath

    return ticker_filepath_map
