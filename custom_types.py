from collections import namedtuple

# Define the named tuple Balance with fields ARS and USD
Balance = namedtuple('Balance', ['ARS', 'USD'])

FCI = namedtuple('FCI', ['name', 'quotas'])

# Define the named tuple State containing a Balance tuple
State = namedtuple('State', ['FCIs'])
