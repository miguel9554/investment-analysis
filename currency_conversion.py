import pandas as pd

def get_ARS_to_USD(date):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('cotizaciones_mep.csv', parse_dates=['Fecha'], dayfirst=True)

    # Extract the date part from the 'Fecha' column
    df['Fecha'] = df['Fecha'].dt.date

    # Filter the DataFrame based on the specified date
    filtered_row = df[df['Fecha'] == date.date()]  # Compare only day, month, and year

    # If the row exists, extract the 'Referencia' value and convert it to a float
    if not filtered_row.empty:
        referencia_str = filtered_row['Referencia'].iloc[0].replace(',', '.')
        referencia_float = float(referencia_str)
        return referencia_float
    else:
        raise Exception(f"No data found for date: {date}")
