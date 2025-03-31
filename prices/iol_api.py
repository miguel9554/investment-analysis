import requests
import pandas as pd
import time
from datetime import datetime

def fetch_stock_open_close_average(symbol, exchange, from_date, to_date, resolution='D'):
    base_url = "https://iol.invertironline.com/api/cotizaciones/history"

    # Convert datetime objects to Unix timestamps
    from_timestamp = int(time.mktime(from_date.timetuple()))
    to_timestamp = int(time.mktime(to_date.timetuple()))

    # Make the request
    response = requests.get(
        base_url,
        params={
            'symbolName': symbol,
            'exchange': exchange,
            'from': from_timestamp,
            'to': to_timestamp,
            'resolution': resolution
        }
    )

    # Process response
    if response.status_code == 200:
        data = response.json()

        # Ensure 'bars' key exists
        bars = data.get('bars', [])
        if not bars:
            print("No data returned from API.")
            return None

        # Extract open, close, and timestamps
        open_prices = [bar.get('open') for bar in bars]
        close_prices = [bar.get('close') for bar in bars]
        dates = [pd.to_datetime(bar.get('time'), unit='s').date() for bar in bars]

        # Compute average prices
        avg_prices = [(o + c) / 2 for o, c in zip(open_prices, close_prices)]

        # Create DataFrame with date index
        df = pd.DataFrame({'average_price': avg_prices}, index=pd.Index(dates, name='date'))

        return df
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    from_date = datetime(2023, 2, 11)
    to_date = datetime(2023, 5, 19)

    data = fetch_stock_open_close_average('TSLA', 'BCBA', from_date, to_date)

    if data is not None:
        print(data.head())
