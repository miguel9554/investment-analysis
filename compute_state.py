import pandas as pd
from currency_conversion import *
from collections import namedtuple

# Define the named tuple Balance with fields ARS and USD
Balance = namedtuple('Balance', ['ARS', 'USD'])

# Define the named tuple State containing a Balance tuple
State = namedtuple('State', ['balance'])

def update_state(row: pd.DataFrame, current_state: State) -> State:

    """
    Update the state based on the row data.

    Parameters:
        row (pandas.DataFrame): A row of data from the DataFrame.
        current_state (State): Current state.

    Returns:
        State: Next state.
    """
    # Implement your logic here to update the state based on the row data
    # For example:
    # if row['some_column'] > some_threshold:
    #     return 'new_state'
    # else:
    #     return current_state
    operations = (
            'Suscripción Desde Cuenta Balanz',
            'Rescate a Banco',
            )
    if (row['Operacion'] in operations):
        amount_ARS = row['Monto']*(1 if row['Operacion'] == 'Suscripción Desde Cuenta Balanz' else -1)
        USD_price = get_ARS_to_USD(row['Fecha'])
        amount_USD = amount_ARS/USD_price
        new_amount_ARS = current_state.balance.ARS+amount_ARS
        new_amount_USD = current_state.balance.USD+amount_USD
        next_balance = Balance(ARS=new_amount_ARS, USD=new_amount_USD)
        next_state = State(balance=next_balance)

        print(f"On {row['Fecha']} USD price: {USD_price}, ARS: {amount_ARS}, USD: {amount_USD}")
    else:
        next_state = current_state

    return next_state  # Placeholder, replace with your actual logic
