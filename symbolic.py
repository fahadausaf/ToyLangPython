from abc import ABC
from grammar import *
from codeGenerator import *

class ExecutionTree:
    def __init__(self, constraints, variables):
        self.left = None
        self.right = None
        self.constraints = constraints
        self.variables = variables
    
    def insert(self, left, right):
        if self.left is None:
            self.left = left
        else:
            self.left.insert(left, right)

        if self.right is None:
            self.right = right
        else:
            self.right.insert(left, right)

executionTree = None

def symbolicExecution(statement, paramList = [], varList = []):
    global executionTree

    if executionTree is None:
            executionTree = ExecutionTree(None, None)

    if (type(statement) == StatementSequence):
        paramList, varList, leftSubTree = symbolicExecution(statement.left, paramList, varList)

        # if leftSubTree:
        #     if(executionTree == None):
        #         executionTree = leftSubTree
        
        paramList, varList, rightSubTree = symbolicExecution(statement.right, paramList, varList)

        # if rightSubTree:
        #     if(executionTree == None):
        #         executionTree = rightSubTree
    
    elif (type(statement) == FunctionDefinition):

        functionDef = FunctionDefinition()
        functionDef = statement

        # get all the input parameters from the function signature
        for p in functionDef.parameterList:
            paramList.append(p.value)

        # process function body
        if(functionDef.functionBody):
            paramList, varList, _ = symbolicExecution(functionDef.functionBody, paramList, varList)
    
    elif (type(statement) == DeclareIntVariable):

        declare = DeclareIntVariable()
        declare = statement
        value = generateExpression(declare.expression)
        varList.append((declare.identifier.value, value))

        # check variable dependency

    elif (type(statement) == IfThenElse):
        print('If-Block')
        ifThenElse = statement
        constraints = generateExpression(ifThenElse.ifCondition)
        print(constraints)
        print(ifThenElse.thenStatement)
        print(ifThenElse.elseStatement)

        print('Input parameters:\t' + str(paramList))
        print('Internal variables:\t' + str(varList))
        print('--------------------')


        left = ExecutionTree(str(constraints), str(varList))
        right = ExecutionTree(str('!(' + constraints + ')'), str(varList))
        
        if executionTree == None:
            executionTree = ExecutionTree(None, None)
            executionTree.left = left
            executionTree.right = right
        else:
            print('\nExecution tree exist. Append node to all terminals')
            
            executionTree.insert(left, right)
            print('Done Insertion')

    
    elif (type(statement) == Statement):
        None
    elif (type(statement) == EndFile):
        None
    else:
        print('Unknown Statement')
        print(type(statement))


    return paramList, varList, executionTree