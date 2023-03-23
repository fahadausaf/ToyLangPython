from lex import *
from parse import *
from codeGenerator import *
from tokenList import *
from helper import *
from symbolic import *



file_test_01 = 'input\\test_lex\\test_01_int_01.d'
file_printf = 'input\\print.d'
file_ifThenElse = 'input\\ifthen3.d'
file_function = 'input\\function.d'
file_function2 = 'input\\function2.d'
file_function3 = 'input\\function3.d'
file_symbolic = 'input\\symbolic.d'
file_assignment = 'input\\assignment.d'
file_test = 'input\\test.d'
file_unary = 'input\\unary.d'
file_logical = 'input\\logicals.d'



tokenList = lex(file_ifThenElse)
parseResult, _ = parseStatement(0, tokenList)
code = generateStatement(parseResult)
print()
print(prettyPrint(code))
print()
print(parseResult)
print(parseResult.left)
print(parseResult.right)
print()
print(parseResult.right.left)
print(parseResult.right.right)
print()
# if-then-else
print(parseResult.right.right.left)
print(parseResult.right.right.right)
print()
# print(parseResult.right.right.right.left)
# print(parseResult.right.right.right.right)



print('\nSymbolic Execution\n')
et = symbolicExecution(parseResult)

print(et)
print(et.expression)
print('Left: ' + str(et.left))
print('Right: ' + str(et.right))
print()
print(et.right.variables)
print(et.right.expression)
print('Left: ' + str(et.right.left))
print('Right: ' + str(et.right.right))


# printf "Test Program";
# int a = 0;
# if 10 > 9 then
# 	a = 2;
# else
# 	printf "Smaller";
# endif;

# printf "End of program";