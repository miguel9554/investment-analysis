import pandas as pd
from custom_types import *
from currency_conversion import *

def update_instruments(current_instruments, instrument_name, amount_change):

    # Find the tuple with the given name
    found_instruments = tuple(filter(lambda instrument: instrument.name == instrument_name, current_instruments))

    # Extract the initial amount
    if len(found_instruments) == 1:
        initial_amount = found_instruments[0].amount
    elif len(found_instruments) == 0:
        initial_amount = 0
    else:
        raise Exception(f'More than 1 instrument with name {instrument_name}: {found_instruments}')

    new_amount = initial_amount + amount_change
    # TODO we admit negative accounts, since in some buy/sell, the sell appears first,
    # is then cancelled by the buy, so is negative for some iterations.
    # Somewhere a check should be done that no amounts are negative.
    """
    if (new_amount < 0):
        if (abs(new_amount) > .5):
            raise Exception(f'Instrument {instrument_name} amount can not be negative: {initial_amount}+{amount_change}={new_amount}')
        else:
            new_amount = 0
    """
    # Round to zero if amount is small, we'll consider it a round error
    if (abs(new_amount) < 1e-3):
        new_amount = 0

    updated_instrument = instrument_t(name=instrument_name, amount=new_amount)

    instruments_without_updated = tuple(filter(lambda instrument: instrument.name != instrument_name, current_instruments))

    if (new_amount > 0):
        new_instruments = instruments_without_updated + (updated_instrument,)
    else:
        new_instruments = instruments_without_updated

    return new_instruments

def instrument_update(row: pd.DataFrame, current_state: State) -> State:

    price = row['Precio']
    amount_change = row['Cantidad']
    name = row['Ticker']
    instrument = row['Tipo de Instrumento']

    # TODO not sure if this is right
    # for buy/sell of dollars, a third op appears with price -1
    if (price == -1 and instrument == 'Bonos'):
        return current_state

    current_instruments = getattr(current_state, instrument)
    new_instruments = update_instruments(current_instruments, name, amount_change)

    # Create a dictionary to store the new state attributes
    new_attrs = {instrument: new_instruments}

    # Replace the corresponding attribute in the state
    new_state = current_state._replace(**new_attrs)

    return new_state

def nop(row: pd.DataFrame, current_state: State) -> State:

    return current_state
