import pandas as pd
from custom_types import *
from currency_conversion import *

def increment_balance_ARS(balance, ars, date):
    usd_price = get_ARS_to_USD(date)
    usd = ars/usd_price
    new_amount_ARS = balance.ARS+ars
    new_amount_USD = balance.USD+usd
    next_balance = Balance(ARS=new_amount_ARS, USD=new_amount_USD)

    print(f"On {date} USD price: {usd_price}, ARS: {ars}, USD: {usd}")

    return next_balance


def deposit_operation(row: pd.DataFrame, current_state: State) -> State:

    deposit_operations = (
            'Suscripción Desde Cuenta Balanz',
            )

    extract_operations = (
            'Rescate a Banco',
            'Transferencia',
            )

    operation = row['Operacion']

    next_balance = increment_balance_ARS(current_state.balance, row['Monto'], row['Fecha'])
    next_state = State(balance=next_balance)

    return next_state  # Placeholder, replace with your actual logic
