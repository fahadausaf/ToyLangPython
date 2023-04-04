from abc import ABC
from grammar import *
from codeGenerator import *
from helper import *

class ExecutionTreeNode:
    def __init__(self, constraints, variables, expression, symbols, condition):
        self.left = None
        self.right = None
        self.constraints = constraints
        self.variables = variables
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
            newNode = ExecutionTreeNode(node.constraints, node.variables, node.expression, node.symbols, node.condition)
            newNode.left = node.left
            newNode.right = node.right
            head.right = newNode




def getExecutionTree(statement, symbolTable = [], iter = 0):
    # node to return after function execution
    retNode = None

    if (type(statement) == StatementSequence):
        left = getExecutionTree(statement.left, symbolTable[0:], iter+1)
        
        right = None
        if statement.right:
            if(type(statement.left) == IfThenElse):
                if left.left.variables:
                    right = getExecutionTree(statement.right, cloneListOfList(left.left.variables), iter+1)
            else:
                right = getExecutionTree(statement.right, cloneListOfList(left.variables), iter+1)

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
        varList = []
        if(functionDef.parameterList):
            for p in functionDef.parameterList:
                varName = p.value
                varList.append([varName, None])

        symList = []
        if(functionDef.parameterList):
            for p in functionDef.parameterList:
                varName = p.value
                symList.append((varName, None))

        
        funBody = ExecutionTreeNode(None, cloneListOfList(varList), 'Function Declaration', symList, None)
        # process function body
        if(functionDef.functionBody):
            funBody.right = getExecutionTree(functionDef.functionBody, cloneListOfList(varList))

        retNode = funBody
    
    elif (type(statement) == DeclareIntVariable):
        declare = DeclareIntVariable()
        declare = statement
        varName = declare.identifier.value
        
        value = getExpressionValue(declare.expression, cloneListOfList(symbolTable))

        symbolTable.append([varName, value])

        retNode = ExecutionTreeNode(None, cloneListOfList(symbolTable), 'Declare Int', (varName, value), None)
    
    elif (type(statement) == DeclareCharVariable):
        declare = DeclareCharVariable()
        declare = statement
        varName = declare.identifier.value
        value = getExpressionValue(declare.expression, symbolTable[0:])

        symbolTable.append([varName, value])

        retNode = ExecutionTreeNode(None, symbolTable[0:], 'Declare Char', (varName, value), None)

    elif (type(statement) == IfThenElse):
        ifThenElse = IfThenElse()
        ifThenElse = statement

        constraints = getExpressionValue(ifThenElse.ifCondition, cloneListOfList(symbolTable))
        thenBody = getExecutionTree(ifThenElse.thenStatement, cloneListOfList(symbolTable))

        condition = str(generateSMTExpression(ifThenElse.ifCondition))
        notCondition = 'Not(' + condition + ')'

        if ifThenElse.elseStatement is None:
            elseBody = None
        else:
            elseBody = getExecutionTree(ifThenElse.elseStatement, cloneListOfList(symbolTable))
        
        trueBranch = ExecutionTreeNode(str(constraints), thenBody.variables, 'True-Branch', None, (condition, ifThenElse.ifCondition, True))
        trueBranch.right = thenBody

        if elseBody:
            falseBranch = ExecutionTreeNode('Not(' + str(constraints) + ')', elseBody.variables, 'False-Branch', None, (notCondition, ifThenElse.ifCondition, False))
            falseBranch.right = elseBody
        else:
            falseBranch = ExecutionTreeNode('Not(' + str(constraints) + ')', cloneListOfList(symbolTable), 'False-Branch', None, (notCondition,ifThenElse.ifCondition, False))
            falseBranch.right = elseBody
        
        ifThenNode = ExecutionTreeNode(None, cloneListOfList(symbolTable), 'If-Then-Else', None, None)
        ifThenNode.left = trueBranch
        ifThenNode.right = falseBranch

        retNode = ifThenNode

    elif (type(statement) == Printf):
        node = ExecutionTreeNode(None, cloneListOfList(symbolTable), 'Print', None, None)
        retNode = node
    
    elif (type(statement) == Assignment):
        varName = statement.identifier.value
        value = getExpressionValue(statement.expression, cloneListOfList(symbolTable))

        symbolExist = False
        for symbol in symbolTable:
            if symbol[0] == varName:
                symbol[1] = value
                symbolExist = True
                break
        if not symbolExist:
            symbolTable.append([varName, value])

        node = ExecutionTreeNode(None, cloneListOfList(symbolTable), 'Assignment', (varName, value), None)
        
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