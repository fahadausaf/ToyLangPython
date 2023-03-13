from grammar import *
from tokenList import *

def parseExpression(currentToken, listTokens):
    if(currentToken == len(listTokens)):
       raise Exception('ERROR: Expected expression, got EOF instead')
    
    parsedExpression = Expression()

    if(type(listTokens[currentToken]) == int):
        intValue = listTokens[currentToken]
        numericValue = NumericValue()
        numericValue.value = intValue
        parsedExpression = numericValue
        currentToken += 1

    elif(type(listTokens[currentToken]) == str):
        None

    else:
        raise Exception('ERROR: Expected string literal, int literal, or variable')

    if listTokens[currentToken] != Tokens.TERMINATOR:
        
        if (listTokens[currentToken] == Tokens.ADD or
            listTokens[currentToken] == Tokens.SUBTRACT or
            listTokens[currentToken] == Tokens.MULTIPLY or
            listTokens[currentToken] == Tokens.SUBTRACT):

            arithmaticExpression = ArithmaticExpression()
            arithmaticExpression.left = parsedExpression
            if listTokens[currentToken] == Tokens.ADD:
                arithmaticExpression.operand = ArithmaticOperands.Add
            elif listTokens[currentToken] == Tokens.SUBTRACT:
                arithmaticExpression.operand = ArithmaticOperands.Sub
            elif listTokens[currentToken] == Tokens.MULTIPLY:
                arithmaticExpression.operand = ArithmaticOperands.Mul
            elif listTokens[currentToken] == Tokens.DIVIDE:
                arithmaticExpression.operand = ArithmaticOperands.Div

            currentToken += 1
            (arithmaticExpression.right, currentToken) = parseExpression(currentToken, listTokens)
            parsedExpression = arithmaticExpression

    
    return (parsedExpression, currentToken)

def parseStatement(currentToken, listTokens):
    parsedStatement = Statement()
    

    if(currentToken == len(listTokens)):
        raise Exception('ERROR: Statement was expected before the end of file')

    elif listTokens[currentToken] == Tokens.TERMINATOR:
        parsedStatement = Terminator()

    elif listTokens[currentToken] == 'var':
        currentToken += 1
        declareVariable = DeclareVariable()

        if(currentToken < len(listTokens)-1 and type(listTokens[currentToken]) == str ):
            declareVariable.identifier = listTokens[currentToken]

        else:
            raise Exception('ERROR: Variable name was expected after keyword var')
        
        currentToken += 1
        if(currentToken == len(listTokens) or listTokens[currentToken] != Tokens.ASSIGNMENT):
            raise Exception('ERROR: = sign was expected after variable name')

        currentToken += 1
        (declareVariable.expression, currentToken) = parseExpression(currentToken, listTokens)
        # currentToken += 1
        if listTokens[currentToken] == Tokens.TERMINATOR:
            declareVariable.terminator = Terminator()
        else:
            raise Exception('ERROR: ; sign was expected after variable declaration')

        parsedStatement = declareVariable
    
    else:
        print('Some other token')

    if(currentToken < len(listTokens)-1):
        currentToken += 1
        sequence = StatementSequence()
        sequence.left = parsedStatement
        sequence.right = parseStatement(currentToken, listTokens)
        parsedStatement = sequence

    return parsedStatement