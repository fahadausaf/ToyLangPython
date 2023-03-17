from lex import *
from parse import *
from codeGenerator import *
from tokenList import *

file_test_01 = 'input\\test_lex\\test_01_int_01.d'
file_printf = 'input\\print.d'
file_ifThenElse = 'input\\ifthen.d'

def printTokens(tokenList):
    n = 1
    for t in tokenList:
        print('No: ' + str(n))
        print('Token: ' + str(t[0]))
        print('Line: ' + str(t[1]) + ', Col: ' + str(t[2]) + '\n')
        n += 1

tokenList = lex(file_ifThenElse)
#printTokens(tokenList)

(parseResult, currentToken) = parseStatement(0, tokenList)


code = generateStatement(parseResult)
print(code)