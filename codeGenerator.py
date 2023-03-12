from grammar import *

def generateStatement(statement):
    code = ''
    if(type(statement) == DeclareVariable):
        declare = DeclareVariable()
        declare = statement

        assign = Assignment()
        assign.identifier = declare.identifier
        assign.expression = declare.expression
        if(type(declare.expression) == NumericValue):
            code = 'int '
            code = code + generateStatement(assign)

    elif(type(statement) == Assignment):
        code = statement.identifier + ' = '
        if(type(statement.expression) == NumericValue):
            numericValue = NumericValue()
            numericValue.value = statement.expression.value
            code = code + generateStatement(numericValue)
    
    elif(type(statement) == NumericValue):
        code = str(statement.value) + ';'
        print(code)
    
    else:
        print('Some other type')
    return code