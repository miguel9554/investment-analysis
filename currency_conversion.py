import pandas as pd

def get_ARS_to_USD(date):

    # Define the lambda function
    parse_referencia = lambda x: float(x.replace(',', '.').split(' ')[0])

    # Read the CSV file, using the lambda function for parsing and parsing dates
    df = pd.read_csv('cotizaciones_mep.csv', parse_dates=['Fecha'], dayfirst=True, converters={'Referencia': parse_referencia})

    # Extract the date part from the 'Fecha' column and convert to Timestamp
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date

    # If no exact match found, interpolate with nearest dates
    df = df.set_index('Fecha')

    # Convert the input date to Timestamp
    date_timestamp = pd.Timestamp(date).date()

    # check if index exists
    index_date_exists = True if date_timestamp in df.index else False

    # If the row exists, extract the 'Referencia' value and convert it to a float
    if index_date_exists:
        return df.loc[date_timestamp][0]
    else:
        # If no data is found for the specified date, interpolate with nearest dates
        nearest_date_before = df.index[df.index <= date_timestamp].max()
        nearest_date_after = df.index[df.index >= date_timestamp].min()
        nearest_value_before = df.loc[nearest_date_before][0]
        nearest_value_after = df.loc[nearest_date_after][0]
        interpolated_value = (nearest_value_before+nearest_value_after)/2
        return interpolated_value
