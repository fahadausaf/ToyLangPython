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
    colPos = 0
    tokenPos = 0
    
    # Read the file charcter by character to build tokens
    
    while 1:
        char = file.read(1)

        colPos += 1

        if char == '\n':
            linePos += 1
            colPos = 0
        elif char.isspace():
            #charPos += 1
            None
        elif char.isalpha():
            token = ''
            tokenPos = colPos
            while char.isalnum():
                token = token + char
                char = file.read(1)
                colPos += 1
            tokenList.append((checkKeywordToken(token), linePos, tokenPos, colPos))
            if char:
                # unread the last character
                file.seek(file.tell()-1)
                colPos -= 1
            

        elif char.isnumeric():
            token = ''
            tokenPos = colPos
            while char.isnumeric():
                token = token + char
                char = file.read(1)
                colPos += 1
            
            numLiteralToken = NumericLiteralToken()
            numLiteralToken.value = int(token)
            tokenList.append((numLiteralToken, linePos, tokenPos, colPos))
            if char:
                # unread the last character
                file.seek(file.tell()-1)
                colPos -= 1

        elif char == '"':
            token = char
            tokenPos = colPos
            char = file.read(1)
            colPos += 1
            while char != '"':
                if not char:
                    print('Invalid Token')
                    break
                token = token + char
                char = file.read(1)
                colPos += 1
            token = token + char
            strLiteralToken = StringLiteralToken()
            strLiteralToken.value = token
            tokenList.append((strLiteralToken, linePos, tokenPos, colPos))

        elif char == '(':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ExpressionTokens.OPEN_PAREN, linePos, tokenPos, colPos))
        elif char == ')':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ExpressionTokens.CLOSE_PAREN, linePos, tokenPos, colPos))
        elif char == '=':
            tokenPos = colPos
            char = file.read(1)
            colPos += 1
            if char == '=':
                tokenList.append((LogicTokens.EQUAL_TO, linePos, tokenPos, colPos))
            else:
                file.seek(file.tell()-1)
                colPos -= 1
                tokenList.append((ExpressionTokens.ASSIGNMENT, linePos, tokenPos, colPos))
        elif char == ';':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ExpressionTokens.TERMINATOR, linePos, tokenPos, colPos))
        elif char == '<':
            tokenPos = colPos
            colPos += 1
            char = file.read(1)
            colPos += 1
            if char == '=':
                tokenList.append((LogicTokens.LESS_THAN_EQUAL_TO, linePos, tokenPos, colPos))
            else:
                file.seek(file.tell()-1)
                colPos -= 1
                tokenList.append((LogicTokens.LESS_THAN, linePos, tokenPos, colPos))
        elif char == '>':
            tokenPos = colPos
            colPos += 1
            char = file.read(1)
            colPos += 1
            if char == '=':
                tokenList.append((LogicTokens.GREATER_THAN_EQUAL_TO, linePos, tokenPos, colPos))
            else:
                file.seek(file.tell()-1)
                colPos -= 1
                tokenList.append((LogicTokens.GREATER_THAN, linePos, tokenPos, colPos))
        elif char == ',':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ExpressionTokens.COMMA, linePos, tokenPos, colPos))
        elif char == '[':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ExpressionTokens.OPEN_BRAC, linePos, tokenPos, colPos))
        elif char == ']':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ExpressionTokens.CLOSE_BRAC, linePos, tokenPos, colPos))
        elif char == '/':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ArithmaticTokens.DIVIDE, linePos, tokenPos, colPos))
        elif char == '*':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ArithmaticTokens.MULTIPLY, linePos, tokenPos, colPos))
        elif char == '-':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ArithmaticTokens.SUBTRACT, linePos, tokenPos, colPos))
        elif char == '+':
            tokenPos = colPos
            colPos += 1
            tokenList.append((ArithmaticTokens.ADD, linePos, tokenPos, colPos))
        elif not char:
            tokenList.append((EOF(), linePos, tokenPos, colPos))
            break
    file.close()

    return tokenList
