from lex import *
from parse import *
from codeGenerator import *

fileName = 'test.d'

tokenList = lex(fileName)

parseResult = parseStatement(0, tokenList)

# print('----------')
# print(parseResult.right.left)
# print(parseResult.right.right)


# print(parseResult)
# print(parseResult.identifier)
# print(parseResult.expression)
# print(parseResult.expression.left)
# print(parseResult.expression.operand)




code = generateStatement(parseResult)
print(code)