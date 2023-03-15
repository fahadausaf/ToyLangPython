from lex import *
from parse import *
from codeGenerator import *

fileName = 'input\\test2.d'

tokenList = lex(fileName)
print(tokenList)


parseResult = parseStatement(0, tokenList)

code = generateStatement(parseResult)
print(code)