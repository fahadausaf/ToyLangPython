from tokenList import *
    
def lex(fileName):
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
            tokenList.append(int(token))
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
            tokenList.append(Tokens.OPEN_PAREN)
        elif char == ')':
            tokenList.append(Tokens.CLOSE_PAREN)
        elif char == '=':
            tokenList.append(Tokens.ASSIGNMENT)
        elif char == ';':
            tokenList.append(Tokens.TERMINATOR)
        elif char == '<':
            tokenList.append(Tokens.LESS_THAN)
        elif char == '>':
            tokenList.append(Tokens.GREATER_THAN)
        elif char == ',':
            tokenList.append(Tokens.COMMA)
        elif char == '/':
            tokenList.append(Tokens.DIVIDE)
        elif char == '*':
            tokenList.append(Tokens.MULTIPLY)
        elif char == '-':
            tokenList.append(Tokens.SUBTRACT)
        elif char == '+':
            tokenList.append(Tokens.ADD)
        elif not char:
            break
    file.close()

    return tokenList
