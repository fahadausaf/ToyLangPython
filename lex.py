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
    
    # variables to track the position of the token in the file
    linePos = 1
    charPos = 0
    tokenPos = 0
    
    # Read the file charcter by character to build tokens
    
    while 1:
        char = file.read(1)

        charPos += 1

        if char == '\n':
            linePos += 1
            #charPos = 1
        elif char.isspace():
            #charPos += 1
            None
        elif char.isalpha():
            token = ''
            tokenPos = charPos
            while char.isalnum():
                token = token + char
                char = file.read(1)
                charPos += 1
            file.seek(file.tell()-1)
            charPos -= 1
            tokenList.append((linePos, tokenPos, checkKeywordToken(token)))

        elif char.isnumeric():
            token = ''
            tokenPos = charPos
            while char.isnumeric():
                token = token + char
                char = file.read(1)
                charPos += 1
            
            numLiteralToken = NumericLiteralToken()
            numLiteralToken.value = int(token)
            tokenList.append((linePos, tokenPos, numLiteralToken))
            if not char:
                break
            file.seek(file.tell()-1)
            charPos -= 1

        elif char == '"':
            token = char
            tokenPos = charPos
            char = file.read(1)
            charPos += 1
            while char != '"':
                if not char:
                    print('Invalid Token')
                    break
                token = token + char
                char = file.read(1)
                charPos += 1
            token = token + char
            strLiteralToken = StringLiteralToken()
            strLiteralToken.value = token
            tokenList.append((linePos, tokenPos, strLiteralToken))

        elif char == '(':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ExpressionTokens.OPEN_PAREN))
        elif char == ')':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ExpressionTokens.CLOSE_PAREN))
        elif char == '=':
            tokenPos = charPos
            char = file.read(1)
            charPos += 1
            if char == '=':
                tokenList.append((linePos, tokenPos, LogicTokens.EQUAL_TO))
            else:
                file.seek(file.tell()-1)
                charPos -= 1
                tokenList.append((linePos, tokenPos, ExpressionTokens.ASSIGNMENT))
        elif char == ';':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ExpressionTokens.TERMINATOR))
        elif char == '<':
            tokenPos = charPos
            charPos += 1
            char = file.read(1)
            charPos += 1
            if char == '=':
                tokenList.append((linePos, tokenPos, LogicTokens.LESS_THAN_EQUAL_TO))
            else:
                file.seek(file.tell()-1)
                charPos -= 1
                tokenList.append((linePos, tokenPos, LogicTokens.LESS_THAN))
        elif char == '>':
            tokenPos = charPos
            charPos += 1
            char = file.read(1)
            charPos += 1
            if char == '=':
                tokenList.append((linePos, tokenPos, LogicTokens.GREATER_THAN_EQUAL_TO))
            else:
                file.seek(file.tell()-1)
                charPos -= 1
                tokenList.append((linePos, tokenPos, LogicTokens.GREATER_THAN))
        elif char == ',':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ExpressionTokens.COMMA))
        elif char == '[':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ExpressionTokens.OPEN_BRAC))
        elif char == ']':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ExpressionTokens.CLOSE_BRAC))
        elif char == '/':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ArithmaticTokens.DIVIDE))
        elif char == '*':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ArithmaticTokens.MULTIPLY))
        elif char == '-':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ArithmaticTokens.SUBTRACT))
        elif char == '+':
            tokenPos = charPos
            charPos += 1
            tokenList.append((linePos, tokenPos, ArithmaticTokens.ADD))
        elif not char:
            break
    file.close()

    return tokenList
