import pandas as pd
from custom_types import *
from currency_conversion import *

def update_instruments(current_instruments, instrument_name, amount_change, date, ingress, currency):

    # Find the tuple with the given name
    found_instruments = tuple(filter(lambda instrument: instrument.name == instrument_name, current_instruments))

    # Extract the initial amount
    if len(found_instruments) == 1:
        initial_amount = found_instruments[0].amount
        initial_ingresses = found_instruments[0].ingresses
    elif len(found_instruments) == 0:
        initial_amount = 0
        initial_ingresses = tuple()
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

    if (ingress == 0):
        new_ingresses = initial_ingresses
    else:
        new_ingresses = initial_ingresses + ((date, ingress, currency),)

    updated_instrument = instrument_t(name=instrument_name, amount=new_amount, ingresses=new_ingresses)

    instruments_without_updated = tuple(filter(lambda instrument: instrument.name != instrument_name, current_instruments))

    if (new_amount > 0):
        new_instruments = instruments_without_updated + (updated_instrument,)
    else:
        new_instruments = instruments_without_updated

    return new_instruments

def instrument_n_ingress_update(row: pd.DataFrame, current_state: State) -> State:
    return instrument_update(row, current_state, is_ingress=True)

def instrument_alone_update(row: pd.DataFrame, current_state: State) -> State:
    return instrument_update(row, current_state, is_ingress=False)

def instrument_update(row: pd.DataFrame, current_state: State, is_ingress) -> State:

    price = row['Precio']
    amount_change = row['Cantidad']
    importe = row['Importe']
    name = row['Ticker']
    instrument = row['Tipo de Instrumento']
    date = row['Concertacion'].date()

    # TODO not sure if this is right
    # for buy/sell of dollars, a third op appears with price -1
    if (price == -1 and instrument == 'Bonos'):
        return current_state

    # TODO With Cedears, a second buy appears with price -1
    if (price == -1 and instrument == 'Cedears' and importe != 0):
        return current_state

    if not is_ingress:
        ingress = 0
        ingress_currency = 0
    else:
        ingress = -importe
        moneda = row['Moneda']
        if moneda == "Pesos":
            currency = "ARS"
        elif moneda == "Dólares":
            currency = "USD"
        else:
            raise Exception(f'Invalid moneda: {moneda}')
        ingress_currency = currency

    current_instruments = getattr(current_state, instrument)
    new_instruments = update_instruments(current_instruments, name, amount_change, date, ingress, ingress_currency)

    # Create a dictionary to store the new state attributes
    new_attrs = {instrument: new_instruments}

    # Replace the corresponding attribute in the state
    new_state = current_state._replace(**new_attrs)

    return new_state

def nop(row: pd.DataFrame, current_state: State) -> State:

    return current_state
