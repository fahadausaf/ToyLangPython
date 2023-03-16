from grammar import *
from tokenList import *


def parseExpression(currentToken, listTokens):

    if (currentToken == len(listTokens)):
        raise Exception('Line: ' + str(listTokens[currentToken-1][1]) + ', Col: ' + str(listTokens[currentToken-1][2]) + '\nDescription: Expected expression, got EOF instead')

    parsedExpression = Expression()

    if (type(listTokens[currentToken][0]) == NumericLiteralToken):
        numLiteral = listTokens[currentToken][0]
        numericValue = NumericValue()
        numericValue.value = numLiteral.value
        parsedExpression = numericValue
        currentToken += 1

    elif (type(listTokens[currentToken][0]) == StringLiteralToken):
        strLiteral = listTokens[currentToken][0]
        strValue = StringValue()
        strValue.value = strLiteral.value;
        parsedExpression = strValue
        currentToken += 1
    
    else:
        raise Exception(
            'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: Expected string literal, int literal, or variable')

    if (currentToken == len(listTokens)):
        raise Exception('Line: ' + str(listTokens[currentToken-1][1]) + ', Col: ' + str(listTokens[currentToken-1][2]) + '\nDescription: Expected expression, got EOF instead')

    if listTokens[currentToken][0] != ExpressionTokens.TERMINATOR:
        if (listTokens[currentToken][0] == ArithmaticTokens.ADD or
                listTokens[currentToken][0] == ArithmaticTokens.SUBTRACT or
                listTokens[currentToken][0] == ArithmaticTokens.MULTIPLY or
                listTokens[currentToken][0] == ArithmaticTokens.DIVIDE):

            arithmaticExpression = ArithmaticExpression()
            arithmaticExpression.left = parsedExpression
            if listTokens[currentToken][0] == ArithmaticTokens.ADD:
                arithmaticExpression.operand = ArithmaticLogicOperands.Add
            elif listTokens[currentToken][0] == ArithmaticTokens.SUBTRACT:
                arithmaticExpression.operand = ArithmaticLogicOperands.Sub
            elif listTokens[currentToken][0] == ArithmaticTokens.MULTIPLY:
                arithmaticExpression.operand = ArithmaticLogicOperands.Mul
            elif listTokens[currentToken][0] == ArithmaticTokens.DIVIDE:
                arithmaticExpression.operand = ArithmaticLogicOperands.Div

            currentToken += 1
            (arithmaticExpression.right, currentToken) = parseExpression(
                currentToken, listTokens)
            parsedExpression = arithmaticExpression

        elif (listTokens[currentToken][0] == LogicTokens.LESS_THAN or
                listTokens[currentToken][0] == LogicTokens.LESS_THAN_EQUAL_TO or
                listTokens[currentToken][0] == LogicTokens.GREATER_THAN or
                listTokens[currentToken][0] == LogicTokens.GREATER_THAN_EQUAL_TO or
                listTokens[currentToken][0] == LogicTokens.EQUAL_TO):
            
            logicExpression = LogicExpression()
            logicExpression.left = parsedExpression
            if listTokens[currentToken][0] == LogicTokens.LESS_THAN:
                logicExpression.operand = LogicOperands.LessThan
            elif listTokens[currentToken][0] == LogicTokens.LESS_THAN_EQUAL_TO:
                logicExpression.operand = LogicOperands.LessThanEqualTo
            elif listTokens[currentToken][0] == LogicTokens.GREATER_THAN:
                logicExpression.operand = LogicOperands.GreaterThan
            elif listTokens[currentToken][0] == LogicTokens.GREATER_THAN_EQUAL_TO:
                logicExpression.operand = LogicOperands.GreaterThanEqualTo
            elif listTokens[currentToken][0] == LogicTokens.EQUAL_TO:
                logicExpression.operand = LogicOperands.EqualTo

            currentToken += 1
            (logicExpression.right, currentToken) = parseExpression(
                currentToken, listTokens)
            parsedExpression = logicExpression
            

    return (parsedExpression, currentToken)


def parseStatement(currentToken, listTokens):
    parsedStatement = Statement()

    if (currentToken == len(listTokens)):
        raise Exception('Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: Statement was expected before the end of file')

    elif listTokens[currentToken][0] == ExpressionTokens.TERMINATOR:
        parsedStatement = Terminator()

    elif listTokens[currentToken][0] == KeywordTokens.CHAR:
        currentToken += 1
        declareVariable = DeclareCharVariable()

        if (currentToken < len(listTokens) - 1 and type(listTokens[currentToken][0]) == VariableLiteralToken):
            declareVariable.identifier = listTokens[currentToken][0]
        else:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: Variable name was expected after keyword char')

        currentToken += 1

        if (currentToken == len(listTokens) or 
            (listTokens[currentToken][0] != ExpressionTokens.OPEN_BRAC and listTokens[currentToken+1] != ExpressionTokens.CLOSE_BRAC)):
            raise Exception('Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: [] sign was expected after variable name')
        
        currentToken += 2
        
        if (currentToken == len(listTokens) or listTokens[currentToken][0] != ExpressionTokens.ASSIGNMENT):
            raise Exception('Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: = sign was expected after variable name')
        
        currentToken += 1

        (declareVariable.expression, currentToken) = parseExpression(
            currentToken, listTokens)

        if listTokens[currentToken][0] == ExpressionTokens.TERMINATOR:
            declareVariable.terminator = Terminator()
        else:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: ; sign was expected after variable declaration')

        parsedStatement = declareVariable
    
    elif listTokens[currentToken][0] == KeywordTokens.INT:
        currentToken += 1
        declareIntVariable = DeclareIntVariable()

        if (currentToken < len(listTokens) - 1 and type(listTokens[currentToken][0]) == VariableLiteralToken):
            declareIntVariable.identifier = listTokens[currentToken][0]
        else:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: Variable name was expected after keyword int')

        currentToken += 1

        if (currentToken == len(listTokens) or listTokens[currentToken][0] != ExpressionTokens.ASSIGNMENT):
            raise Exception('Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: = sign was expected after variable name')

        currentToken += 1
        (declareIntVariable.expression, currentToken) = parseExpression(
            currentToken, listTokens)

        if listTokens[currentToken][0] == ExpressionTokens.TERMINATOR:
            declareIntVariable.terminator = Terminator()
        else:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: ; sign was expected after variable declaration')

        parsedStatement = declareIntVariable

    elif listTokens[currentToken][0] == KeywordTokens.PRINTF:
        currentToken += 1
        printf = Printf()
        (printf.expression, currentToken) = parseExpression(currentToken, listTokens)

        if listTokens[currentToken][0] == ExpressionTokens.TERMINATOR:
            printf.terminator = Terminator()
        else:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + '\nDescription: ; sign was expected after printf expression')

        
        parsedStatement = printf

    
    elif type(listTokens[currentToken][0]) == EOF:
        return parsedStatement
    else:
        print('Unknown Error')
        return None

    if (currentToken < len(listTokens) - 1):
        currentToken += 1
        sequence = StatementSequence()
        sequence.left = parsedStatement
        sequence.right = parseStatement(currentToken, listTokens)
        parsedStatement = sequence

    return parsedStatement
