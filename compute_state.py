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
    'Suscripción desde Balanz': fci_update,
    'Rescate Cambio de Fondo': fci_update,
    'Suscripción Cambio de Fondo': fci_update,
    'Rescate': fci_update,
    'Rescate a Balanz': fci_update,
    # NOP movements
    'Recibo de Cobro / .*': nop,
    'Liquidación de Suscripción / .* / .*': nop,
    'Comprobante de Pago / .*': nop,
    'Liquidación de Rescate / .* / .*': nop,
}

# Define your update_state function
def update_state(row: pd.DataFrame, current_state: State) -> State:
    operation_type = row['Descripcion']

    operation_function = get_operation_function(operation_functions, operation_type)
    new_state = operation_function(row, current_state)
    print(f'{row["Liquidacion"]}, State: {new_state}')

    return new_state
