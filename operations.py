import pandas as pd
from custom_types import *
from currency_conversion import *

def update_fci_quota(current_fcis, fci_name, quotas_change):

    # Find the tuple with the given name
    found_fcis = tuple(filter(lambda FCI: FCI.name == fci_name, current_fcis))

    # Extract the initial quotas
    if len(found_fcis) == 1:
        initial_quotas = found_fcis[0].quotas
    elif len(found_fcis) == 0:
        initial_quotas = 0
    else:
        raise Exception(f'More than 1 FCI with name {fci_name}: {found_fcis}')

    new_quotas = initial_quotas + quotas_change
    if (new_quotas < 0):
        if (abs(new_quotas) > .5):
            raise Exception(f'FCI {fci_name} quotas can not be negative: {initial_quotas}+{quotas_change}={new_quotas}')
        else:
            new_quotas = 0

    new_fci = FCI(name=fci_name, quotas=new_quotas)

    FCIs_without_changed = tuple(filter(lambda FCI: FCI.name != fci_name, current_fcis))

    if (new_quotas > 0):
        new_FCIs = FCIs_without_changed + (new_fci,)
    else:
        new_FCIs = FCIs_without_changed

    return new_FCIs

def fci_update(row: pd.DataFrame, current_state: State) -> State:

    quotas_acquired = row['Cantidad']
    fci_name = row['Ticker']

    new_FCIs = update_fci_quota(current_state.FCIs, fci_name, quotas_acquired)

    new_state = State(FCIs=new_FCIs)

    return new_state

def nop(row: pd.DataFrame, current_state: State) -> State:

    return current_state
