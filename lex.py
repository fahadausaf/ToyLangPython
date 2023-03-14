from tokenList import *

def checkKeywordToken(token):
    try:
        return KeywordTokens(token)
    except:
        varLiteralToken = VariableLiteralToken()
        varLiteralToken.value = token
        return varLiteralToken

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
            tokenList.append(checkKeywordToken(token))

        elif char.isnumeric():
            token = ''
            while char.isnumeric():
                token = token + char
                char = file.read(1)
            file.seek(file.tell()-1)
            numLiteralToken = NumericLiteralToken()
            numLiteralToken.value = int(token)
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
            strLiteralToken = StringLiteralToken()
            strLiteralToken.value = token
            tokenList.append(strLiteralToken)

        elif char == '(':
            tokenList.append(ExpressionTokens.OPEN_PAREN)
        elif char == ')':
            tokenList.append(ExpressionTokens.CLOSE_PAREN)
        elif char == '=':
            char = file.read(1)
            if char == '=':
                tokenList.append(LogicTokens.EQUAL_TO)
            else:
                file.seek(file.tell()-1)
                tokenList.append(ExpressionTokens.ASSIGNMENT)
        elif char == ';':
            tokenList.append(ExpressionTokens.TERMINATOR)
        elif char == '<':
            char = file.read(1)
            if char == '=':
                tokenList.append(LogicTokens.LESS_THAN_EQUAL_TO)
            else:
                file.seek(file.tell()-1)
                tokenList.append(LogicTokens.LESS_THAN)
        elif char == '>':
            char = file.read(1)
            if char == '=':
                tokenList.append(LogicTokens.GREATER_THAN_EQUAL_TO)
            else:
                file.seek(file.tell()-1)
                tokenList.append(LogicTokens.GREATER_THAN)
        elif char == ',':
            tokenList.append(ExpressionTokens.COMMA)
        elif char == '[':
            tokenList.append(ExpressionTokens.OPEN_BRAC)
        elif char == ']':
            tokenList.append(ExpressionTokens.CLOSE_BRAC)
        elif char == '/':
            tokenList.append(ArithmaticTokens.DIVIDE)
        elif char == '*':
            tokenList.append(ArithmaticTokens.MULTIPLY)
        elif char == '-':
            tokenList.append(ArithmaticTokens.SUBTRACT)
        elif char == '+':
            tokenList.append(ArithmaticTokens.ADD)
        elif not char:
            break
    file.close()

    return tokenList
