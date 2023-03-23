from abc import ABC
from grammar import *
from codeGenerator import *

class ExecutionTreeNode:
    def __init__(self, constraints, variables, expression):
        self.left = None
        self.right = None
        self.constraints = constraints
        self.variables = variables
        self.expression = expression
    
    def insert(self, left, right):
        if self.left is None:
            self.left = left
        else:
            self.left.insert(left, right)

        if self.right is None:
            self.right = right
        else:
            self.right.insert(left, right)

def symbolicExecution(statement, exTree = None):

    if (type(statement) == StatementSequence):
        
        left = symbolicExecution(statement.left)
        right = symbolicExecution(statement.right)

        if(type(statement.left) == IfThenElse):
            left.left.right = right
            left.right.right = right
        else:
            left.right = right

        return left
    
    elif (type(statement) == FunctionDefinition):

        functionDef = FunctionDefinition()
        functionDef = statement


        # process function body
        if(functionDef.functionBody):
            _ = symbolicExecution(functionDef.functionBody, exTree)
    
    elif (type(statement) == DeclareIntVariable):
        declare = DeclareIntVariable()
        declare = statement
        value = generateExpression(declare.expression)
        return ExecutionTreeNode(None, (declare.identifier.value, value), 'declare int')

    elif (type(statement) == IfThenElse):
        constraints = generateExpression(statement.ifCondition)
        
        trueBranch = ExecutionTreeNode(str(constraints), None, 'True-Branch')
        #trueBranch.right = symbolicExecution(statement.thenStatement)

        falseBranch = ExecutionTreeNode('!(' + str(constraints) + ')', None, 'False-Branch')
        #falseBranch.right = symbolicExecution(statement.elseStatement)
        
        ifThenNode = ExecutionTreeNode(None, None, 'If-Then-Else')
        ifThenNode.left = trueBranch
        ifThenNode.right = falseBranch

        return ifThenNode


    elif (type(statement) == Printf):
        node = ExecutionTreeNode(None, None, 'printf')
        return node
    
    elif (type(statement) == Statement):
        return None
    elif (type(statement) == EndFile):
        if exTree is None:
            return None
        else:
            return exTree
    else:
        print('Unknown Statement')
        print(type(statement))


    return None