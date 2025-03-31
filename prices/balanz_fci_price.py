import os
import re
from datetime import datetime
import csv
from pathlib import Path
import pandas as pd
from prices.iol_api import *

def get_this_file_dir():
    # Get the path of the current script
    script_path = Path(__file__).resolve()

    # Get the directory containing the script
    script_dir = script_path.parent

    return script_dir

def get_fci_price(ticker, date):
    mapping = get_ticker_to_filepath_mapping(get_this_file_dir() / 'balanz_fcis')
    try:
        filepath = mapping[ticker]
    except KeyError:
        raise Exception(f'Prices table for ticker {ticker} not found')
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
            dates_before = tuple(date for date in dates if date < target_date)
            if (len(dates_before) == 0):
                # If there are no dates before, we are on a date older than data
                # There is no price, so return 0
                return 0
            closest_date_before = max(dates_before)

            dates_after = tuple(date for date in dates if date > target_date)
            # If there no dates after, we are on a date newer than data
            # Just return the newest available data
            if (len(dates_after) == 0):
                return prices[closest_date_before]
            closest_date_after = min(dates_after)

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

def interpolate_csv(filepath, date_index):
    # Ensure date_index is a DatetimeIndex
    date_index = pd.to_datetime(date_index)

    # Load CSV file into DataFrame
    df = pd.read_csv(filepath, parse_dates=['Date'], index_col='Date', dayfirst=True)

    return interpolate_df(df, date_index)

def interpolate_df(df, date_index):
    # Convert DataFrame index to DatetimeIndex
    df.index = pd.to_datetime(df.index)

    # Ensure the DataFrame has only one column
    if df.shape[1] != 1:
        raise ValueError("DataFrame must have only one column")

    column_name = df.columns[0]  # Get the single column name

    # Reindex DataFrame with provided date_index, ensuring it's a DatetimeIndex
    date_index = pd.to_datetime(date_index)
    df = df.reindex(date_index)

    # Interpolate missing values
    df[column_name] = df[column_name].interpolate(method='time')

    # Fill NaN values before the first data point with 0
    df[column_name] = df[column_name].fillna(0)

    # Fill NaN values after the last data point with the last value
    df[column_name] = df[column_name].ffill()

    # Convert index to date only
    df.index = df.index.date

    return df

def get_fci_price_df(ticker, dates):
    mapping = get_ticker_to_filepath_mapping(get_this_file_dir() / 'balanz_fcis')
    try:
        filepath = mapping[ticker[:-1]]
    except KeyError:
        raise Exception(f'Prices table for ticker {ticker} not found')
    df = interpolate_csv(filepath, dates)
    # Rename the column to ticker
    df.columns = [ticker]
    return df

def get_cedear_price_df(ticker, dates):

    # Get the first and last dates from the list
    start_date = min(dates)
    end_date = max(dates)

    # Fetch data for the entire range at once
    price_df = fetch_stock_open_close_average(
        symbol=f'{ticker}D',
        exchange='BCBA',  # Argentine exchange for CEDEARs
        from_date=start_date,
        to_date=end_date
    )

    price_df = interpolate_df(price_df, dates)
    price_df.columns = [ticker]
    return price_df

def get_cedears_price_df(tickers, dates):
    dfs = ()
    for ticker in tickers:
        dfs = dfs + (get_cedear_price_df(ticker, dates),)
    return pd.concat(dfs, axis=1)

def get_fcis_price_df(tickers, dates):
    dfs = ()
    for ticker in tickers:
        dfs = dfs + (get_fci_price_df(ticker, dates),)
    return pd.concat(dfs, axis=1)

def get_dolar_price_df(dates):
    filepath = get_this_file_dir() / 'dolar' / 'mep.csv'
    df = interpolate_csv(filepath, dates)
    # Rename the column to ticker
    df.columns = ['Dolar MEP']
    return df
