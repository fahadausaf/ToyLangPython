import helper
from enum import Enum
    
def lex(fileName):
    tokens = helper.Enum(['Add', 'Subtract', 'Multiply', 'Divide', 'Terminator', 'Assignment', 'EqualTo', 'LessThan', 'GreaterThan', 'Comma', 'OpenParen', 'CloseParen', 'OpenBrac', 'CloseBrac'])
    tokenList = []
    file = open(fileName, 'r')
    
    # Read the file charcter by character to build tokens
    while 1:
        char = file.read(1)

        if char.isspace():
            None
        elif char.isalpha():
            token = ''
            while char.isalnum():
                token = token + char
                char = file.read(1)
            file.seek(file.tell()-1)
            tokenList.append(token)
        elif char.isnumeric():
            token = ''
            while char.isnumeric():
                token = token + char
                char = file.read(1)
            file.seek(file.tell()-1)
            tokenList.append(token)
        elif char == '"':
            token = char
            char = file.read(1)
            while char != '"':
                if not char:
                    print('Invalid Token')
                    break
                token = token + char
                char = file.read(1)
            token = token + char
            tokenList.append(token)

        elif char == '(':
            tokenList.append(tokens.OpenParen)
        elif char == ')':
            tokenList.append(tokens.CloseParen)
        elif char == '=':
            tokenList.append(tokens.Assignment)
        elif char == ';':
            tokenList.append(tokens.Terminator)
        elif char == '<':
            tokenList.append(tokens.LessThan)
        elif char == '>':
            tokenList.append(tokens.GreaterThan)
        elif char == ',':
            tokenList.append(tokens.Comma)
        elif char == '/':
            tokenList.append(tokens.Divide)
        elif char == '*':
            tokenList.append(tokens.Multiply)
        elif char == '-':
            tokenList.append(tokens.Subtract)
        elif char == '+':
            tokenList.append(tokens.Add)
        elif not char:
            break
    file.close()

    return tokenList
