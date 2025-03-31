import pandas as pd
import re
from operations import *
from custom_types import *

def get_operation_function(operation_functions, operation_type):
    matching_functions = []

    # Find matching functions
    for operation_pattern, func in operation_functions.items():
        if re.fullmatch(operation_pattern, operation_type):
            matching_functions.append(func)

    if not matching_functions:
        raise Exception("No matching function found for operation type:", operation_type)
    elif len(matching_functions) > 1:
        raise Exception("More than one function matched for operation type:", operation_type)
    else:
        return matching_functions[0]

# Create a dictionary mapping operation types to corresponding functions
operation_functions = {
    # FCI movements
    r'Suscripción desde Balanz': instrument_update,
    r'Rescate Cambio de Fondo': instrument_update,
    r'Suscripción Cambio de Fondo': instrument_update,
    r'Rescate': instrument_update,
    r'Rescate a Balanz': instrument_update,
    # NOP movements
    r'Recibo de Cobro / \d+': nop,
    r'Recibo de Cobro / \d+': nop,
    r'Liquidación de Suscripción / \d+ / [\w|\s]+': nop,
    r'Comprobante de Pago / \d+': nop,
    r'Liquidación de Rescate / \d+ / [\w|\s]+': nop,
    # CEDEAR/bonos/corporativos
    r'Boleto / \d+ / (COMPRA|VENTA|Licitación MAE) / \d+ / \w+ / (\$|usd)': instrument_update,
    # Dividends
    # TODO should do something with this
    r'Dividendo en efectivo / \w+': nop,
    r'Renta / [\d|\w]+': nop,
    r'Renta y Amortización / (TX26|RCCJO|AL30|IRCGO)': nop,
    # CEDEAR split
    r'Dividendo en acciones / \w+': instrument_update, # This is actually a CEDEAR split
    r'Split / \w+': instrument_update, # This is actually a CEDEAR split
    r'Acreditación cambio de ratio / \w+': instrument_update,
    # Misc
    r'^Movimiento Manual \/ Conversión CV 7\.000 a CV 10\.000 \(dólar (MEP|mep)\)$': nop,
    r'^Movimiento Manual / Gastos por cambio de ratio - NVDA$': nop,
    r'Cargo por Descubierto del \d\d/\d\d/\d\d\d\d': nop,
    r'Cargo por Descubierto del \d\d/\d/\d\d\d\d': nop,
}

# Define your update_state function
def update_state(row: pd.DataFrame, current_state: State) -> State:
    operation_type = row['Descripcion']

    operation_function = get_operation_function(operation_functions, operation_type)
    new_state = operation_function(row, current_state)
    #print(f'{row["Liquidacion"]}, State: {new_state}')

    return new_state
