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

def insertNode(head, node):
    if head.left and head.right:
        insertNode(head.left, node)
        insertNode(head.right, node)
    elif not head.left and head.right:
        insertNode(head.right, node)
    elif not head.left and not head.right:
        head.right = node

def symbolicExecution(statement, exTree = None):

    if (type(statement) == StatementSequence):
        left = symbolicExecution(statement.left)
        if statement.right is None:
            right = None
        else:
            right = symbolicExecution(statement.right)

        if(type(statement.left) == IfThenElse):
            insertNode(left, right)
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
        return ExecutionTreeNode(None, (declare.identifier.value, value), 'Declare Int')
    
    elif (type(statement) == DeclareCharVariable):
        declare = DeclareCharVariable()
        declare = statement
        value = generateExpression(declare.expression)
        return ExecutionTreeNode(None, (declare.identifier.value, value), 'Declare Char')

    elif (type(statement) == IfThenElse):
        ifThenElse = IfThenElse()
        ifThenElse = statement

        constraints = generateExpression(ifThenElse.ifCondition)
        
        thenBody = symbolicExecution(ifThenElse.thenStatement)

        if ifThenElse.elseStatement is None:
            elseBody = None
        else:
            elseBody = symbolicExecution(ifThenElse.elseStatement)
        
        trueBranch = ExecutionTreeNode(str(constraints), None, 'True-Branch')
        trueBranch.right = thenBody

        falseBranch = ExecutionTreeNode('!(' + str(constraints) + ')', None, 'False-Branch')
        falseBranch.right = elseBody
        
        ifThenNode = ExecutionTreeNode(None, None, 'If-Then-Else')
        ifThenNode.left = trueBranch
        ifThenNode.right = falseBranch

        return ifThenNode


    elif (type(statement) == Printf):
        node = ExecutionTreeNode(None, None, 'Print')
        return node
    
    elif (type(statement) == Assignment):
        node = ExecutionTreeNode(None, None, 'Assignment')
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


    return None