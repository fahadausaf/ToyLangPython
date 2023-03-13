from grammar import *

def generateOperand(operand):
    if(operand == ArithmaticOperands.Add):
        return ' + '
    elif(operand == ArithmaticOperands.Sub):
        return ' - '
    elif(operand == ArithmaticOperands.Mul):
        return ' * '
    elif(operand == ArithmaticOperands.Div):
        return ' / '

def generateExpression(expression):
    code = ''

    if(type(expression) == NumericValue):
        numericValue = NumericValue()
        numericValue.value = expression.value
        code = code + generateStatement(numericValue)

    elif(type(expression) == ArithmaticExpression):
        code = generateExpression(expression.left)
        code = code + generateOperand(expression.operand)
        code = code + generateExpression(expression.right)

    return code

def generateStatement(statement):
    code = ''
    if(type(statement) == StatementSequence):
        left = generateStatement(statement.left)
        right = generateStatement(statement.right)
        code = left + right

    elif(type(statement) == DeclareVariable):
        declare = DeclareVariable()
        declare = statement

        assign = Assignment()
        assign.identifier = declare.identifier
        assign.expression = declare.expression

        if(type(declare.expression) == NumericValue or type(declare.expression) == ArithmaticExpression):
            code = 'int '
            code = code + generateStatement(assign)
            code = code + generateStatement(declare.terminator)

    elif(type(statement) == Assignment):
        code = statement.identifier + ' = '

        code = code + generateExpression(statement.expression)

        # if(type(statement.expression) == NumericValue):
        #     numericValue = NumericValue()
        #     numericValue.value = statement.expression.value
        #     code = code + generateStatement(numericValue)
    
    elif(type(statement) == NumericValue):
        code = str(statement.value)
    
    elif(type(statement) == Terminator):
        code = ';\n'

    else:
        print('Some other type')
        print(code)
    return code