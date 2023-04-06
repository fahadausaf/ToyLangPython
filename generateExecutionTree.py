from abc import ABC
from grammar import *
from codeGenerator import *
from helper import *

class ExecutionTreeNode:
    def __init__(self, constraints, expression, symbols, condition):
        self.left = None
        self.right = None
        self.constraints = constraints
        self.expression = expression
        self.symbols = symbols
        self.condition = condition

def insertNode(head, node):
    if head.left:
        insertNode(head.left, node)
    if head.right:
        insertNode(head.right, node)
    else:
        if node:
            newNode = ExecutionTreeNode(node.constraints, node.expression, node.symbols, node.condition)
            newNode.left = node.left
            newNode.right = node.right
            head.right = newNode




def getExecutionTree(statement, symbolTable = [], iter = 0):
    # node to return after function execution
    retNode = None

    if (type(statement) == StatementSequence):
        left = getExecutionTree(statement.left, symbolTable[0:])
        right = getExecutionTree(statement.right)
        
        if(type(statement.left) == IfThenElse):
            insertNode(left, right)
        else:
            if left.right is None:
                left.right = right
               
        retNode = left

    
    elif (type(statement) == FunctionDefinition):
        functionDef = FunctionDefinition()
        functionDef = statement

        # get function parameters list
        symList = []
        conList = []
        if(functionDef.parameterList):
            for p in functionDef.parameterList:
                paramName = p[0].value
                paramType = p[1].value
                symList.append((paramName, None))
                conList.append((paramName, paramType))

        
        funBody = ExecutionTreeNode(conList, 'Function Declaration', symList, None)
        # process function body
        if(functionDef.functionBody):
            funBody.right = getExecutionTree(functionDef.functionBody)

        retNode = funBody

    elif (type(statement) == FunDefinition):
        functionDef = FunDefinition()
        functionDef = statement

        # get function parameters list
        symList = []
        if(functionDef.parameterList):
            for p in functionDef.parameterList:
                varName = p.value
                symList.append((varName, None))

        
        funBody = ExecutionTreeNode(None, 'Function Declaration', symList, None)
        # process function body
        if(functionDef.functionBody):
            funBody.right = getExecutionTree(functionDef.functionBody)

        retNode = funBody
    
    elif (type(statement) == DeclareIntVariable):
        declare = DeclareIntVariable()
        declare = statement
        varName = declare.identifier.value
        value = getExpressionValue(declare.expression)

        retNode = ExecutionTreeNode(None, 'Declare Int', (varName, value), None)
    
    elif (type(statement) == DeclareCharVariable):
        declare = DeclareCharVariable()
        declare = statement
        varName = declare.identifier.value
        value = getExpressionValue(declare.expression)

        retNode = ExecutionTreeNode(None, 'Declare Char', (varName, value), None)

    elif (type(statement) == IfThenElse):
        ifThenElse = IfThenElse()
        ifThenElse = statement

        constraints = getExpressionValue(ifThenElse.ifCondition, cloneListOfList(symbolTable))
        thenBody = getExecutionTree(ifThenElse.thenStatement)

        condition = str(generateSMTExpression(ifThenElse.ifCondition))
        notCondition = 'Not(' + condition + ')'

        if ifThenElse.elseStatement is None:
            elseBody = None
        else:
            elseBody = getExecutionTree(ifThenElse.elseStatement)
        
        trueBranch = ExecutionTreeNode(str(constraints), 'True-Branch', None, (condition, ifThenElse.ifCondition, True))
        trueBranch.right = thenBody

        if elseBody:
            falseBranch = ExecutionTreeNode('Not(' + str(constraints) + ')', 'False-Branch', None, (notCondition, ifThenElse.ifCondition, False))
            falseBranch.right = elseBody
        else:
            falseBranch = ExecutionTreeNode('Not(' + str(constraints) + ')', 'False-Branch', None, (notCondition,ifThenElse.ifCondition, False))
            falseBranch.right = elseBody
        
        ifThenNode = ExecutionTreeNode(None, 'If-Then-Else', None, None)
        ifThenNode.left = trueBranch
        ifThenNode.right = falseBranch

        retNode = ifThenNode

    elif (type(statement) == Printf):
        node = ExecutionTreeNode(None, 'Print', None, None)
        retNode = node
    
    elif (type(statement) == Assignment):
        varName = statement.identifier.value
        value = getExpressionValue(statement.expression)

        node = ExecutionTreeNode(None, 'Assignment', (varName, value), None)
        
        retNode = node
    
    elif (type(statement) == Statement):
        retNode = None
    
    elif (type(statement) == EndFile):
        retNode = None
    
    else:
        print('Unknown Statement')
        print(type(statement))
        retNode = None
    
    return retNode