from lex import *
from parse import *
from codeGenerator import *

fileName = 'input\stringLiteral.d'
tokenList = lex(fileName)


parseResult = parseStatement(0, tokenList)

code = generateStatement(parseResult)
print(code)