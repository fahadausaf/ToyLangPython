from grammar import *

def symbolicExecution(statement, paramList = [], varList = [], dependencyList = []):
    if (type(statement) == StatementSequence):
        paramList, varList, dependencyList = symbolicExecution(statement.left, paramList, varList, dependencyList)
        paramList, varList, dependencyList = symbolicExecution(statement.right, paramList, varList, dependencyList)
    
    elif (type(statement) == FunctionDefinition):
        print('Function Type found')

        functionDef = FunctionDefinition()
        functionDef = statement

        # get all the input parameters from the function signature
        for p in functionDef.parameterList:
            paramList.append(p.value)

        # process function body
        if(functionDef.functionBody):
            paramList, varList, dependencyList = symbolicExecution(functionDef.functionBody, paramList, varList, dependencyList)
    
    elif (type(statement) == DeclareIntVariable):
        print('Declare Variable Found')

        declare = DeclareIntVariable()
        declare = statement
        varList.append(declare.identifier.value)

        # check variable dependency
    
    else:
        print('Unknown Statement')

    return paramList, varList, dependencyList