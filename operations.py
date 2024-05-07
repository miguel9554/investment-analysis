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
    if (new_amount < 0):
        if (abs(new_amount) > .5):
            raise Exception(f'Instrument {instrument_name} amount can not be negative: {initial_amount}+{amount_change}={new_amount}')
        else:
            new_amount = 0

    updated_instrument = instrument_t(name=instrument_name, amount=new_amount)

    instruments_without_updated = tuple(filter(lambda instrument: instrument.name != instrument_name, current_instruments))

    if (new_amount > 0):
        new_instruments = instruments_without_updated + (updated_instrument,)
    else:
        new_instruments = instruments_without_updated

    return new_instruments

def instrument_update(row: pd.DataFrame, current_state: State) -> State:

    amount_change = row['Cantidad']
    name = row['Ticker']
    instrument = row['Tipo de Instrumento']

    current_instruments = getattr(current_state, instrument)
    new_instruments = update_instruments(current_instruments, name, amount_change)

    if (instrument == 'Fondos'):
        new_state = current_state._replace(Fondos=new_instruments)
    elif (instrument == 'Cedears'):
        new_state = current_state._replace(Cedears=new_instruments)
    elif (instrument == 'Bonos'):
        new_state = current_state._replace(Bonos=new_instruments)
    elif (instrument == 'Corporativos'):
        new_state = current_state._replace(Corporativos=new_instruments)

    return new_state

def nop(row: pd.DataFrame, current_state: State) -> State:

    return current_state
