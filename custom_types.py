from collections import namedtuple

instrument_t = namedtuple('instrument_t', ['name', 'amount', 'ingresses'])

# Define the named tuple State containing a Balance tuple
State = namedtuple('State', ['Fondos', 'Cedears', 'Bonos', 'Corporativos'])
