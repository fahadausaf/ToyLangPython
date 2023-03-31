from z3 import *
set_param('parallel.enable', True)

a = Bool('a')
b = Int('b')
solve( a, (b > 5))

