'''
lift math functions to behavious
'''
from behaviours import liftB
from events import liftET
import math
import sys
ns = globals()
for func in ['sin','cos','floor']:
    ns[func+'B'] = liftB(getattr(math, func))
for func in ['sin','cos','floor']:
    ns[func+'ET'] = liftET(getattr(math, func))
