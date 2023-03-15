from grammar import *


def generateArithmaticOperand(operand):
    if (operand == ArithmaticLogicOperands.Add):
        return ' + '
    elif (operand == ArithmaticLogicOperands.Sub):
        return ' - '
    elif (operand == ArithmaticLogicOperands.Mul):
        return ' * '
    elif (operand == ArithmaticLogicOperands.Div):
        return ' / '
    
def generateLogicOperand(operand):
    if (operand == LogicOperands.LessThan):
        return ' < '
    elif (operand == LogicOperands.LessThanEqualTo):
        return ' <= '
    elif (operand == LogicOperands.GreaterThan):
        return ' > '
    elif (operand == LogicOperands.GreaterThanEqualTo):
        return ' >= '
    elif (operand == LogicOperands.EqualTo):
        return ' == '

def generateExpression(expression):
    code = ''

    if (type(expression) == NumericValue):
        numericValue = NumericValue()
        numericValue.value = expression.value
        code = code + generateStatement(numericValue)

    elif (type(expression) == StringValue):
        strValue = StringValue()
        strValue.value = expression.value
        code = code + generateStatement(strValue)

    elif (type(expression) == ArithmaticExpression):
        code = generateExpression(expression.left)
        code = code + generateArithmaticOperand(expression.operand)
        code = code + generateExpression(expression.right)

    elif (type(expression) == LogicExpression):
        code = generateExpression(expression.left)
        code = code + generateLogicOperand(expression.operand)
        code = code + generateExpression(expression.right)

    return code

def generateStatement(statement):
    code = ''

    if (type(statement) == StatementSequence):
        left = generateStatement(statement.left)
        right = generateStatement(statement.right)
        code = left + right

    elif (type(statement) == DeclareCharVariable):
        declare = DeclareCharVariable()
        declare = statement

        assign = Assignment()
        assign.identifier = declare.identifier
        assign.expression = declare.expression

        code = 'char ' + generateStatement(assign) + generateStatement(declare.terminator)
    
    elif (type(statement) == DeclareIntVariable):
        declare = DeclareIntVariable()
        declare = statement

        assign = Assignment()
        assign.identifier = declare.identifier
        assign.expression = declare.expression

        if (type(declare.expression) == NumericValue or 
            type(declare.expression) == ArithmaticExpression or
            type(declare.expression) == LogicExpression):
            code = 'int '
            code = code + generateStatement(assign)
            code = code + generateStatement(declare.terminator)

    elif (type(statement) == Assignment):
        if(type(statement.expression) == StringValue):
            code = statement.identifier.value + '[] = '
        else:
            code = statement.identifier.value + ' = '
        code = code + generateExpression(statement.expression)

    elif (type(statement) == NumericValue):
        code = str(statement.value)

    elif (type(statement) == StringValue):
        code = str(statement.value)

    elif (type(statement) == Terminator):
        code = ';\n'

    else:
        print('Some other type')
        print(code)
    return code
