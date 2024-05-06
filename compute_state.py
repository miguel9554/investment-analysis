import pandas as pd
from currency_conversion import *
from collections import namedtuple

# Define the named tuple Balance with fields ARS and USD
Balance = namedtuple('Balance', ['ARS', 'USD'])

# Define the named tuple State containing a Balance tuple
State = namedtuple('State', ['balance'])

def update_state(row: pd.DataFrame, current_state: State) -> State:

    deposit_operations = (
            'Suscripción Desde Cuenta Balanz',
            )

    extract_operations = (
            'Rescate a Banco',
            'Transferencia',
            )

    operations = deposit_operations + extract_operations

    operation = row['Operacion']

    if (operation in operations):
        amount_ARS = row['Monto']*(1 if operation in deposit_operations else -1)
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
