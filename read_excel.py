import pandas as pd

def read_excel_to_dataframe(filepath):
    # Read Excel file into DataFrame
    df = pd.read_excel(filepath)

    # Convert Concertacion and Liquidacion columns to date type
    df['Concertacion'] = pd.to_datetime(df['Concertacion'], errors='coerce')
    df['Liquidacion'] = pd.to_datetime(df['Liquidacion'], errors='coerce')

    # Convert Cantidad, Precio, and Importe columns to floats
    df['Cantidad'] = df['Cantidad'].astype(float)
    df['Precio'] = df['Precio'].astype(float)
    df['Importe'] = df['Importe'].astype(float)

    return df
