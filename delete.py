from lex import *
from parse import *
from codeGenerator import *
from tokenList import *
from helper import *
from generateExecutionTree import *


file_ifThenElse = 'input\\symbolic.d'

tokenList = lex(file_ifThenElse)
ast, _ = parseStatement(0, tokenList)
code = generateStatement(ast)

print()
print(prettyPrint(code))
et = getExecutionTree(ast)
getExecutionSequenceDetail(et)
print()
getExpressions(et)
print()
smtExpr = getSMTExpressions(et)
printSMTExpressions(smtExpr)

"""
def getUnitTests(node):
    print('Unit Tests')

    def getUT(node):
        if node.symbols:
            print('Symbols')
            print(node.symbols)

        if node.condition:
            print('Condition')
            print(node.condition)

        if node.left:
            getUT(node.left)

        if node.right:
            getUT(node.right)

        if not node.left and not node.right:
            print('Test\n')

    getUT(node)

#getUnitTests(et)
"""


# print(ast)
# print(ast.left)
# print(ast.right)
# # function body
# fb = ast.left.functionBody
# print(fb)
# print(fb.left)
# print(fb.right)
# print(fb.right.left)
# print(fb.right.right)
# print(fb.right.right.left)
# print(fb.right.right.right)
# # first if-condition
# ifCond1 = fb.right.right.right.left 
# print(ifCond1)
# # remaining tree
# rt = fb.right.right.right.right
# print(rt)
# print()
# print(rt.left)
# print(rt.right)