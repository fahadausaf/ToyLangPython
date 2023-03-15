from grammar import *
from tokenList import *


def parseExpression(currentToken, listTokens):
    if (currentToken == len(listTokens)):
        raise Exception('ERROR: Expected expression, got EOF instead')

    parsedExpression = Expression()

    if (type(listTokens[currentToken]) == NumericLiteralToken):
        numLiteral = listTokens[currentToken]
        numericValue = NumericValue()
        numericValue.value = numLiteral.value
        parsedExpression = numericValue
        currentToken += 1

    elif (type(listTokens[currentToken]) == StringLiteralToken):
        strLiteral = listTokens[currentToken]
        strValue = StringValue()
        strValue.value = strLiteral.value;
        parsedExpression = strValue
        currentToken += 1
    
    else:
        raise Exception(
            'ERROR: Expected string literal, int literal, or variable')

    if listTokens[currentToken] != ExpressionTokens.TERMINATOR:
        if (listTokens[currentToken] == ArithmaticTokens.ADD or
                listTokens[currentToken] == ArithmaticTokens.SUBTRACT or
                listTokens[currentToken] == ArithmaticTokens.MULTIPLY or
                listTokens[currentToken] == ArithmaticTokens.DIVIDE):

            arithmaticExpression = ArithmaticExpression()
            arithmaticExpression.left = parsedExpression
            if listTokens[currentToken] == ArithmaticTokens.ADD:
                arithmaticExpression.operand = ArithmaticLogicOperands.Add
            elif listTokens[currentToken] == ArithmaticTokens.SUBTRACT:
                arithmaticExpression.operand = ArithmaticLogicOperands.Sub
            elif listTokens[currentToken] == ArithmaticTokens.MULTIPLY:
                arithmaticExpression.operand = ArithmaticLogicOperands.Mul
            elif listTokens[currentToken] == ArithmaticTokens.DIVIDE:
                arithmaticExpression.operand = ArithmaticLogicOperands.Div

            currentToken += 1
            (arithmaticExpression.right, currentToken) = parseExpression(
                currentToken, listTokens)
            parsedExpression = arithmaticExpression

        elif (listTokens[currentToken] == LogicTokens.LESS_THAN or
                listTokens[currentToken] == LogicTokens.LESS_THAN_EQUAL_TO or
                listTokens[currentToken] == LogicTokens.GREATER_THAN or
                listTokens[currentToken] == LogicTokens.GREATER_THAN_EQUAL_TO or
                listTokens[currentToken] == LogicTokens.EQUAL_TO):
            
            logicExpression = LogicExpression()
            logicExpression.left = parsedExpression
            if listTokens[currentToken] == LogicTokens.LESS_THAN:
                logicExpression.operand = LogicOperands.LessThan
            elif listTokens[currentToken] == LogicTokens.LESS_THAN_EQUAL_TO:
                logicExpression.operand = LogicOperands.LessThanEqualTo
            elif listTokens[currentToken] == LogicTokens.GREATER_THAN:
                logicExpression.operand = LogicOperands.GreaterThan
            elif listTokens[currentToken] == LogicTokens.GREATER_THAN_EQUAL_TO:
                logicExpression.operand = LogicOperands.GreaterThanEqualTo
            elif listTokens[currentToken] == LogicTokens.EQUAL_TO:
                logicExpression.operand = LogicOperands.EqualTo

            currentToken += 1
            (logicExpression.right, currentToken) = parseExpression(
                currentToken, listTokens)
            parsedExpression = logicExpression
            

    return (parsedExpression, currentToken)


def parseStatement(currentToken, listTokens):
    parsedStatement = Statement()

    if (currentToken == len(listTokens)):
        raise Exception('ERROR: Statement was expected before the end of file')

    elif listTokens[currentToken] == ExpressionTokens.TERMINATOR:
        parsedStatement = Terminator()

    elif listTokens[currentToken] == KeywordTokens.CHAR:
        currentToken += 1
        declareVariable = DeclareCharVariable()

        if (currentToken < len(listTokens) - 1 and type(listTokens[currentToken]) == VariableLiteralToken):
            declareVariable.identifier = listTokens[currentToken]
        else:
            raise Exception(
                'ERROR: Variable name was expected after keyword char')

        currentToken += 1

        if (currentToken == len(listTokens) or 
            (listTokens[currentToken] != ExpressionTokens.OPEN_BRAC and listTokens[currentToken+1] != ExpressionTokens.CLOSE_BRAC)):
            raise Exception('ERROR: [] sign was expected after variable name')
        
        currentToken += 2
        
        if (currentToken == len(listTokens) or listTokens[currentToken] != ExpressionTokens.ASSIGNMENT):
            raise Exception('ERROR: = sign was expected after variable name')
        
        currentToken += 1

        (declareVariable.expression, currentToken) = parseExpression(
            currentToken, listTokens)

        if listTokens[currentToken] == ExpressionTokens.TERMINATOR:
            declareVariable.terminator = Terminator()
        else:
            raise Exception(
                'ERROR: ; sign was expected after variable declaration')

        parsedStatement = declareVariable
    
    elif listTokens[currentToken] == KeywordTokens.INT:
        currentToken += 1
        declareIntVariable = DeclareIntVariable()

        if (currentToken < len(listTokens) - 1 and type(listTokens[currentToken]) == VariableLiteralToken):
            declareIntVariable.identifier = listTokens[currentToken]
        else:
            raise Exception(
                'ERROR: Variable name was expected after keyword int')

        currentToken += 1

        if (currentToken == len(listTokens) or listTokens[currentToken] != ExpressionTokens.ASSIGNMENT):
            raise Exception('ERROR: = sign was expected after variable name')

        currentToken += 1
        (declareIntVariable.expression, currentToken) = parseExpression(
            currentToken, listTokens)

        if listTokens[currentToken] == ExpressionTokens.TERMINATOR:
            declareIntVariable.terminator = Terminator()
        else:
            raise Exception(
                'ERROR: ; sign was expected after variable declaration')

        parsedStatement = declareIntVariable

    else:
        print('Some other token')

    if (currentToken < len(listTokens) - 1):
        currentToken += 1
        sequence = StatementSequence()
        sequence.left = parsedStatement
        sequence.right = parseStatement(currentToken, listTokens)
        parsedStatement = sequence

    return parsedStatement
