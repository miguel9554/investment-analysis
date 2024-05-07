import pandas as pd
from operations import *
from custom_types import *

# Create a dictionary mapping operation types to corresponding functions
operation_functions = {
    'Suscripción Desde Cuenta Balanz': fci_acquisition,
    'Cambio de Fondo': fci_change,
    'Rescate a Banco': fci_extraction,
    'Transferencia': nop,
}

# Define your update_state function
def update_state(row: pd.DataFrame, current_state: State) -> State:
    operation_type = row['Operacion']

    # Check if the operation type is valid
    if operation_type in operation_functions:
        # Call the corresponding function with row data and current state
        operation_function = operation_functions[operation_type]
        new_state = operation_function(row, current_state)
    else:
        raise ValueError(f"Invalid operation type: {operation_type}")

    print(f'State: {new_state}')

    return new_state
