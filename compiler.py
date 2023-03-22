from lex import *
from parse import *
from codeGenerator import *
from tokenList import *
from helper import *
from symbolic import *



file_test_01 = 'input\\test_lex\\test_01_int_01.d'
file_printf = 'input\\print.d'
file_ifThenElse = 'input\\ifthen.d'
file_function = 'input\\function.d'
file_function2 = 'input\\function2.d'
file_function3 = 'input\\function3.d'
file_symbolic = 'input\\symbolic.d'
file_assignment = 'input\\assignment.d'
file_test = 'input\\test.d'
file_unary = 'input\\unary.d'
file_logical = 'input\\logicals.d'



tokenList = lex(file_symbolic)
parseResult, currentToken = parseStatement(0, tokenList)
code = generateStatement(parseResult)
print()
print(prettyPrint(code))

# print(parseResult)
# print(parseResult.left)
# print(parseResult.left.parameterList)
# funBody = parseResult.left.functionBody
# print('Function Body')
# print(funBody)
# print(funBody.left)
# print(funBody.left.identifier.value)
# print(funBody.left.expression)

# print(funBody.right)
# print(funBody.right.left)
# print(funBody.right.right)
# print(funBody.right.right.left)
# print(funBody.right.right.right)
# print('FIRST: If-Then-Else')
# print(funBody.right.right.right.left)

# print('Remaining Statement')
# print(funBody.right.right.right.right)
# print('SECOND: If-Then-Else')
# print(funBody.right.right.right.right.left)
# print(funBody.right.right.right.right.right)
# print('THIRD: If-Then-Else')
# print(funBody.right.right.right.right.right.left)
# print(funBody.right.right.right.right.right.right)
# print("**********")


paramList, varList, executionTree = symbolicExecution(parseResult)

# print('Input parameters:\t' + str(paramList))
# print('Internal variables:\t' + str(varList))
# print('Dependent variables:\t' + str(dependencyList))

print('********************')
print(executionTree)
print(executionTree.constraints)
print(executionTree.variables)


left = ExecutionTree('Z', 'xyz')
right = ExecutionTree('!(Z)', 'xyz')

executionTree.insert(left, right)

print(executionTree.left.constraints)
print(executionTree.left.variables)
print(executionTree.right.constraints)
print(executionTree.right.variables)

