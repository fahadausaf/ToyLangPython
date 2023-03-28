from z3 import *
set_param('parallel.enable', True)

x = Int('x')
y = Int('y')
solve(x > 2, y < 10, x + 2*y == 7)
