import pandas as pd
from datetime import datetime

def extract_instrument_from_state(states_over_time, instrument):
    instrument_over_time = {key: getattr(value, instrument) for key, value in states_over_time.items()}
    return instrument_over_time

def dict_to_dataframe(original_dict):
    # Create a list of dictionaries to construct the DataFrame
    data = []
    for key, value in original_dict.items():
        row = {'Date': pd.to_datetime(key)}  # Convert key to datetime
        for instrument_tuple in value:
            row[instrument_tuple.name] = instrument_tuple.amount
        data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)

    # If for a certain date there is not existence of an instrument,
    # we'll have NaN. We actually want 0.
    df.fillna(0, inplace=True)

    return df

def fill_missing_days(df):
    # Get today's date
    today = pd.to_datetime(datetime.today().date())

    # Ensure the DataFrame is indexed by dates
    df.index = pd.to_datetime(df.index)

    # Reindex with a date range up to today and forward fill missing values
    df_filled = df.reindex(pd.date_range(start=df.index.min(), end=today, freq='D')).ffill()

    return df_filled

def apply_price(df, get_price):
    """
    Applies the get_price function to each value in the DataFrame.

    Args:
    - df (pd.DataFrame): The DataFrame to be modified.
    - get_price (function): A function that takes a ticker (column name) and a date as arguments
                            and returns the price.

    Returns:
    - pd.DataFrame: The modified DataFrame with each value multiplied by the corresponding price.
    """
    # Make a copy of the DataFrame to avoid modifying the original DataFrame
    df_modified = df.copy()

    # Iterate over each date in the DataFrame's index
    for date in df_modified.index:
        # Call get_price for each column and date, and multiply the corresponding value
        for col in df_modified.columns:
            df_modified.at[date, col] *= get_price(col[:-1], date)

    return df_modified
