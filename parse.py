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
    
    elif(listTokens[currentToken][0] == ArithmaticTokens.SUBTRACT or listTokens[currentToken][0] == LogicTokens.NOT):
        unaryExp = UnaryExpression()
        if listTokens[currentToken][0] == ArithmaticTokens.SUBTRACT:
            unaryExp.operand = UnaryOperands.Minus
        else:
            unaryExp.operand = UnaryOperands.Not

        currentToken += 1
        (unaryExp.expression, currentToken) = parseExpression(currentToken, listTokens)
        parsedExpression = unaryExp
    
    else:
        raise Exception(
            'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
            '\nDescription: Expected string literal, int literal, or variable')

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

    elif type(listTokens[currentToken][0]) == VariableLiteralToken:
        assign = Assignment()
        assign.identifier = listTokens[currentToken][0]
        currentToken += 1

        if listTokens[currentToken][0] != ExpressionTokens.ASSIGNMENT:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: = sign was expected after variable name')
        
        currentToken += 1
        
        (assign.expression, currentToken) = parseExpression(currentToken, listTokens)

        if listTokens[currentToken][0] != ExpressionTokens.TERMINATOR:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: ; sign was expected after value assignment')
        
        parsedStatement = assign

    
    elif listTokens[currentToken][0] == KeywordTokens.FUNCTION:
        currentToken += 1
        functionDef = FunctionDefinition()
        
        # handle function signature
        if type(listTokens[currentToken][0]) != VariableLiteralToken:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: function name was expected after keyword function')
        
        functionDef.identifier = listTokens[currentToken][0]
        currentToken += 1
        
        if listTokens[currentToken][0] != ExpressionTokens.OPEN_PAREN:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: ( was expected after the function name')
        
        currentToken += 1

        # handle function parameters
        if listTokens[currentToken][0] != ExpressionTokens.CLOSE_PAREN:
            paramList = []
            while(listTokens[currentToken][0] != ExpressionTokens.CLOSE_PAREN):
                if (listTokens[currentToken][0] == ExpressionTokens.COMMA and type(listTokens[currentToken+1][0]) != VariableLiteralToken):
                    raise Exception(
                        'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                        '\nDescription: Input parameter name was expected after ,')
                
                elif (type(listTokens[currentToken][0]) == EOF):
                    raise Exception(
                        'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                        '\nDescription: ) was expected after function_name(')
                
                if (listTokens[currentToken][0] != ExpressionTokens.COMMA):
                    paramList.append(listTokens[currentToken][0])
                
                currentToken += 1
            functionDef.parameterList = paramList
        
        currentToken += 1

        # handle function body
        if listTokens[currentToken][0] != ExpressionTokens.ASSIGNMENT or listTokens[currentToken+1][0] != ExpressionTokens.OPEN_CURLY_BRAC:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: ={ was expected after the function signature')
        
        currentToken += 2

        if(listTokens[currentToken][0] != ExpressionTokens.CLOSE_CURLY_BRAC):
            (functionDef.functionBody, currentToken)  = parseStatement(currentToken, listTokens)
        else:
            functionDef.functionBody = None
            currentToken += 1

        
        parsedStatement = functionDef
    
    elif listTokens[currentToken][0] == KeywordTokens.PRINTF:
        currentToken += 1
        printf = Printf()
        (printf.expression, currentToken) = parseExpression(currentToken, listTokens)
        
        if listTokens[currentToken][0] == ExpressionTokens.TERMINATOR:
            printf.terminator = Terminator()
        else:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: ; sign was expected after printf expression')

        parsedStatement = printf

    elif listTokens[currentToken][0] == KeywordTokens.IF:

        currentToken += 1
        ifThenElse = IfThenElse()
        (ifThenElse.ifCondition, currentToken) = parseExpression(currentToken, listTokens)

        if listTokens[currentToken][0] != KeywordTokens.THEN:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: then keyword was expected after if-condition')
        
        currentToken += 1
        (ifThenElse.thenStatement, currentToken)  = parseStatement(currentToken, listTokens)

        # set the statement.right to None if there is no code
        if(type(ifThenElse.thenStatement.right) == Statement):
            ifThenElse.thenStatement.right = None

        # if current token is not ENDIF then this is an ELSE block
        if listTokens[currentToken][0] != KeywordTokens.ENDIF:
            currentToken += 1
            (ifThenElse.elseStatement, currentToken)  = parseStatement(currentToken, listTokens)

        if listTokens[currentToken][0] != KeywordTokens.ENDIF:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: endif keyword was expected after then/else expression')
        
        currentToken += 1
        if listTokens[currentToken][0] != ExpressionTokens.TERMINATOR:
            raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: ; sign was expected after printf expression')
        
        currentToken += 1
        parsedStatement = ifThenElse

    elif type(listTokens[currentToken][0]) == EOF:
        eof = EndFile()
        parsedStatement = eof
    
    elif listTokens[currentToken][0] == KeywordTokens.ELSE:
        return (parsedStatement, currentToken)

    elif listTokens[currentToken][0] == KeywordTokens.ENDIF:
        return (parsedStatement, currentToken)
    
    elif listTokens[currentToken][0] == ExpressionTokens.CLOSE_CURLY_BRAC:
        return (parsedStatement, currentToken)

    else:
        raise Exception(
                'Line: ' + str(listTokens[currentToken][1]) + ', Col: ' + str(listTokens[currentToken][2]) + 
                '\nDescription: Unrecognised Token/Syntax')

    if (currentToken < len(listTokens) - 1):
        currentToken += 1
        sequence = StatementSequence()
        sequence.left = parsedStatement
        (sequence.right, currentToken) = parseStatement(currentToken, listTokens)
        parsedStatement = sequence

    return (parsedStatement, currentToken)
