from lex import *
from parse import *
from codeGenerator import *

def printTokens(tokenList):
    n = 1
    for t in tokenList:
        print('No: ' + str(n))
        print('Token: ' + str(t[2]))
        print('Line: ' + str(t[0]) + ', Char: ' + str(t[1]) + '\n')
        n += 1

fileName = 'input\\test2.d'
tokenList = lex(fileName)
#printTokens(tokenList)

parseResult = parseStatement(0, tokenList)

code = generateStatement(parseResult)
print(code)