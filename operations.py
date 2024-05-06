import pandas as pd
from custom_types import *
from currency_conversion import *

def deposit_operation(row: pd.DataFrame, current_state: State) -> State:

    deposit_operations = (
            'Suscripción Desde Cuenta Balanz',
            )

    extract_operations = (
            'Rescate a Banco',
            'Transferencia',
            )

    operation = row['Operacion']

    amount_ARS = row['Monto']*(1 if operation in deposit_operations else -1)
    USD_price = get_ARS_to_USD(row['Fecha'])
    amount_USD = amount_ARS/USD_price
    new_amount_ARS = current_state.balance.ARS+amount_ARS
    new_amount_USD = current_state.balance.USD+amount_USD
    next_balance = Balance(ARS=new_amount_ARS, USD=new_amount_USD)
    next_state = State(balance=next_balance)

    print(f"On {row['Fecha']} USD price: {USD_price}, ARS: {amount_ARS}, USD: {amount_USD}")

    return next_state  # Placeholder, replace with your actual logic
