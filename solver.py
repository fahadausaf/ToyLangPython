from z3 import *
set_param('parallel.enable', True)


a = Bool('a')
b = Int('b')
c = Bool('c')


# solve(a, b > 5, Not(a), c, -2 + 1 + 2 != 3)                 # no Solution
# solve(a, b > 5, Not(a), c, Not(-2 + 1 + 2 != 3))            # no Solution
# solve(a, b > 5, Not(Not(a), c), -2 + 0 + 2 != 3)            # [b = 6, a = True]
# solve(a, b > 5, Not(Not(a), c), Not(-2 + 0 + 2 != 3))       # no Solution
# solve(a, Not(b > 5), -2 + 0 + 0 != 3)                       # [b = 5, a = True]
# solve(a, Not(b > 5), Not(-2 + 0 + 0 != 3))                  # no Solution
# solve(Not(a), b > 5, Not(a), c, 0 + 1 + 2 != 3)             # no Solution
# solve(Not(a), b > 5, Not(a), c, Not(0 + 1 + 2 != 3))        # [b = 6, a = False, c = True]
# solve(Not(a), b > 5, Not(Not(a), c), 0 + 0 + 2 != 3)        # no Solution
# solve(Not(a), b > 5, Not(Not(a), c), Not(0 + 0 + 2 != 3))   # no Solution
# solve(Not(a), Not(b > 5), 0 + 0 + 0 != 3)                   # [b = 5, a = False]
# solve(Not(a), Not(b > 5), Not(0 + 0 + 0 != 3))              # no Solution


# lstCons = [('a', 'Bool'), ('b', 'Int'), ('c', 'Bool')]

# for con in lstCons:
#     print(con)

# print('constraints added')


print('====================')
a1 = solve(Bool('a'), Not(Int('b') > 5), -2 + 0 + 0 != 3)                       # [b = 5, a = True]
a2 = solve(Not(Bool('a')), Int('b') > 5, Not(Bool('a')), Bool('c'))
a3 = solve(Not(a), b > 5, Not(a), c)  

s = Solver()
s.add(Bool('a'))
s.add(Not(Int('b') > 5))

test = s.check()
print(test)
print('==========')
m = s.model()
print(m)
print(m[Bool('a')])
print(m[Int('b')])

