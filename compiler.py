from lex import *
from parse import *
from codeGenerator import *
from tokenList import *
from helper import *
from generateExecutionTree import *



file_test_01 = 'input\\test_lex\\test_01_int_01.d'
file_printf = 'input\\print.d'
file_ifThenElse = 'input\\ifthen3.d'
file_function = 'input\\function.d'
file_function2 = 'input\\function2.d'
file_function3 = 'input\\function3.d'
file_symbolic = 'input\\symbolic2.d'
file_assignment = 'input\\assignment.d'
file_test = 'input\\test.d'
file_unary = 'input\\unary.d'
file_logical = 'input\\logicals.d'


def insertNode(head, node):
    print(head.expression)
    if head.left:
        insertNode(head.left, node)
    if head.right:
        insertNode(head.right, node)
    else:
        newNode = ExecutionTreeNode(node.constraints, node.variables, node.expression)
        newNode.left = node.left
        newNode.right = node.right
        head.right = newNode





tokenList = lex(file_symbolic)
# printTokens(tokenList)
parseResult, _ = parseStatement(0, tokenList)
code = generateStatement(parseResult)
print()
print(prettyPrint(code))
print()



print('\nSymbolic Execution\n')
et = symbolicExecution(parseResult)
parseExecutionTree(et)






























# print(et)
# print(et.expression)
# print(et.left)
# print(et.left.expression)
# print(et.left.left)
# print(et.left.right.expression)

# print(et.left.right.left.expression)
# print(et.left.right.left.right.expression)
# print(et.left.right.left.right.left)
# print(et.left.right.left.right.right)
# print(et.left.right.left.right.right.expression)
# print(et.left.right.left.right.right.left)
# print(et.left.right.left.right.right.right)
# print(et.left.right.left.right.right.right.expression)
# print(et.left.right.left.right.right.right.left)
# print(et.left.right.left.right.right.right.right)
# print(et.left.right.left.right.right.right.right.expression)

# print(et.left.right.left.right.right.right.right.right.expression)
# print(et.left.right.left.right.right.right.right.right.right.expression)
# print(et.left.right.left.right.right.right.right.right.right.right.expression)
# print(et.left.right.left.right.right.right.right.right.right.right.right.expression)



#print(et.left.right.right.expression)


