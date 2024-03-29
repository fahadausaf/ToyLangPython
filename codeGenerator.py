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
    elif (operand == LogicOperands.NotEqualTo):
        return ' != '
    elif (operand == LogicOperands.And):
        return ' && '
    
def generateSMTLogicOperand(operand):
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
    elif (operand == LogicOperands.NotEqualTo):
        return ' != '
    elif (operand == LogicOperands.And):
        return ', '

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
    
    elif (type(expression) == VariableExpression):
        code = code + expression.identifier

    elif (type(expression) == ArithmaticExpression):
        code = generateExpression(expression.left)
        code = code + generateArithmaticOperand(expression.operand)
        code = code + generateExpression(expression.right)

    elif (type(expression) == LogicExpression):
        code = generateExpression(expression.left)
        code = code + generateLogicOperand(expression.operand)
        code = code + generateExpression(expression.right)

    elif (type(expression) == UnaryExpression):
        unaryExp = UnaryExpression()
        unaryExp = expression

        if unaryExp.operand == UnaryOperands.Minus:
            code = code + '-'
        else:
            code = code + '!'

        code = code + generateExpression(unaryExp.expression)
    return code

def generateSMTExpression(expression):
    code = ''

    if (type(expression) == NumericValue):
        numericValue = NumericValue()
        numericValue.value = expression.value
        code = code + generateStatement(numericValue)

    elif (type(expression) == StringValue):
        strValue = StringValue()
        strValue.value = expression.value
        code = code + generateStatement(strValue)
    
    elif (type(expression) == VariableExpression):
        code = code + '(' + expression.identifier + ')'

    elif (type(expression) == ArithmaticExpression):
        code = generateSMTExpression(expression.left)
        code = code + generateArithmaticOperand(expression.operand)
        code = code + generateSMTExpression(expression.right)

    elif (type(expression) == LogicExpression):
        code = generateSMTExpression(expression.left)
        code = code + generateSMTLogicOperand(expression.operand)
        code = code + generateSMTExpression(expression.right)

    elif (type(expression) == UnaryExpression):
        unaryExp = UnaryExpression()
        unaryExp = expression

        if unaryExp.operand == UnaryOperands.Minus:
            code = code + '-'
        else:
            code = code + 'Not'

        code = code + generateSMTExpression(unaryExp.expression)
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

        code = 'char ' + generateStatement(assign) #+ generateStatement(declare.terminator)
    
    elif (type(statement) == DeclareIntVariable):
        declare = DeclareIntVariable()
        declare = statement

        assign = Assignment()
        assign.identifier = declare.identifier
        assign.expression = declare.expression

        if (type(declare.expression) == NumericValue or 
            type(declare.expression) == ArithmaticExpression or
            type(declare.expression) == LogicExpression or
            type(declare.expression) == UnaryExpression):
            code = 'int '
            code = code + generateStatement(assign)
            #code = code + generateStatement(declare.terminator)

    elif (type(statement) == FunctionDefinition):

        functionDef = FunctionDefinition()
        functionDef = statement

        # Handle Function Signature
        code = 'int ' + functionDef.identifier.value + '('
        
        if(functionDef.parameterList):
            paramSeparator = False
            for p in functionDef.parameterList:
                paramName = p[0].value
                paramType = p[1].value

                if paramSeparator:
                    code = code + ', ' + paramType + ' ' + paramName
                else:
                    code = code + paramType + ' ' + paramName
                paramSeparator = True
        
        code = code + ')\n{\n'

        # Handle Function Body
        if(functionDef.functionBody):
            code =  code + generateStatement(functionDef.functionBody)


        code = code + '\n\nreturn 0;\n}'

    elif (type(statement) == FunDefinition):

        functionDef = FunDefinition()
        functionDef = statement

        # Handle Function Signature
        code = 'int ' + functionDef.identifier.value + '('
        
        if(functionDef.parameterList):
            paramSeparator = False
            for p in functionDef.parameterList:
                if paramSeparator:
                    code = code + ', int ' + p.value
                else:
                    code = code + 'int ' + p.value
                paramSeparator = True
        
        code = code + ')\n{\n'

        # Handle Function Body
        if(functionDef.functionBody):
            code =  code + generateStatement(functionDef.functionBody)


        code = code + '\n\nreturn 0;\n}'
    
    elif (type(statement) == IfThenElse):

        ifThenElse = IfThenElse()
        ifThenElse = statement

        code = '\nif (' + generateExpression(ifThenElse.ifCondition) + ')\n{\n'
        code = code + generateStatement(ifThenElse.thenStatement) + '}\n'
        if (ifThenElse.elseStatement != None):
            code = code + 'else\n{\n' + generateStatement(ifThenElse.elseStatement) + '}\n\n'

    elif (type(statement) == Printf):
        code = 'printf(' + generateExpression(statement.expression) + ')' + generateStatement(statement.terminator)
    
    elif (type(statement) == Assignment):
        if(type(statement.expression) == StringValue):
            code = statement.identifier.value + '[] = '
        else:
            code = statement.identifier.value + ' = '
        code = code + generateExpression(statement.expression)
        code = code + generateStatement(statement.terminator)

    elif (type(statement) == NumericValue):
        code = str(statement.value)

    elif (type(statement) == StringValue):
        code = str(statement.value)

    elif (type(statement) == Terminator):
        code = ';\n'

    elif (type(statement) == EndFile):
        code = ''

    elif (type(statement) == Statement or statement == None):
        None
        
    else:
        print(statement)
        print('Unknown Token Type')
    return code
