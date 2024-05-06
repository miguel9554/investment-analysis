import pandas as pd

def read_excel_to_dataframe(file_path):
    """
    Reads data from an Excel file into a pandas DataFrame.

    Parameters:
        file_path (str): Path to the Excel file.

    Returns:
        pandas.DataFrame: DataFrame containing the data from the Excel file.
    """
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    return df

def merge_date_time_columns(df):
    """
    Merges 'Fecha' and 'Hora' columns into a single column 'Fecha' of type datetime.

    Parameters:
        df (pandas.DataFrame): DataFrame containing the data.

    Returns:
        pandas.DataFrame: DataFrame with 'Fecha' column merged.
    """
    # Merge 'Fecha' and 'Hora' columns into a single column 'Fecha' of type datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'] + ' ' + df['Hora'], dayfirst=True)

    # Drop the 'Hora' column
    df.drop(columns=['Hora'], inplace=True)

    return df
