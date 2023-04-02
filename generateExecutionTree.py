from abc import ABC
from grammar import *
from codeGenerator import *
from helper import *

class ExecutionTreeNode:
    def __init__(self, constraints, variables, expression):
        self.left = None
        self.right = None
        self.constraints = constraints
        self.variables = variables
        self.expression = expression

def insertNode(head, node):
    if head.left:
        insertNode(head.left, node)
    if head.right:
        insertNode(head.right, node)
    else:
        if node:
            newNode = ExecutionTreeNode(node.constraints, node.variables, node.expression)
            newNode.left = node.left
            newNode.right = node.right
            head.right = newNode


def getExpressionValue(expression, symbolTable=[]):
    code = ''

    if (type(expression) == NumericValue):
        numericValue = NumericValue()
        numericValue.value = expression.value
        code = code + str(expression.value)

    elif (type(expression) == StringValue):
        strValue = StringValue()
        strValue.value = expression.value
        code = code + str(expression.value)
    
    elif (type(expression) == VariableExpression):
        ident = expression.identifier
        for symbol in symbolTable:
            if symbol[0] == ident:
                if symbol[1]:
                    ident = symbol[1]
        code = code + ident

    elif (type(expression) == ArithmaticExpression):
        code = getExpressionValue(expression.left, symbolTable)
        code = code + generateArithmaticOperand(expression.operand)
        code = code + getExpressionValue(expression.right, symbolTable)

    elif (type(expression) == LogicExpression):
        code = getExpressionValue(expression.left, symbolTable)
        code = code + generateLogicOperand(expression.operand)
        code = code + getExpressionValue(expression.right, symbolTable)

    elif (type(expression) == UnaryExpression):
        unaryExp = UnaryExpression()
        unaryExp = expression

        if unaryExp.operand == UnaryOperands.Minus:
            code = code + '-'
        else:
            code = code + '!'

        code = code + getExpressionValue(unaryExp.expression, symbolTable)
    return code



def getExecutionTree(statement, symbolTable = [], iter = 0):
    # node to return after function execution
    retNode = None
    
    if (type(statement) == StatementSequence):
        left = getExecutionTree(statement.left, symbolTable[0:], iter+1)
        
        right = None
        if statement.right:
            if(type(statement.left) == IfThenElse):
                if left.left.variables:
                    right = getExecutionTree(statement.right, duplicateListOfList(left.left.variables), iter+1)
            else:
                right = getExecutionTree(statement.right, duplicateListOfList(left.variables), iter+1)

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
        
        funBody = ExecutionTreeNode(None, duplicateListOfList(varList), 'Function Declaration')
        # process function body
        if(functionDef.functionBody):
            funBody.right = getExecutionTree(functionDef.functionBody, duplicateListOfList(varList))

        retNode = funBody
    
    elif (type(statement) == DeclareIntVariable):
        declare = DeclareIntVariable()
        declare = statement
        varName = declare.identifier.value
        
        value = getExpressionValue(declare.expression, duplicateListOfList(symbolTable))

        symbolTable.append([varName, value])

        retNode = ExecutionTreeNode(None, duplicateListOfList(symbolTable), 'Declare Int')
    
    elif (type(statement) == DeclareCharVariable):
        declare = DeclareCharVariable()
        declare = statement
        varName = declare.identifier.value
        value = getExpressionValue(declare.expression, symbolTable[0:])

        symbolTable.append([varName, value])

        retNode = ExecutionTreeNode(None, symbolTable[0:], 'Declare Char')

    elif (type(statement) == IfThenElse):
        ifThenElse = IfThenElse()
        ifThenElse = statement

        constraints = getExpressionValue(ifThenElse.ifCondition, duplicateListOfList(symbolTable))
        thenBody = getExecutionTree(ifThenElse.thenStatement, duplicateListOfList(symbolTable))

        if ifThenElse.elseStatement is None:
            elseBody = None
        else:
            elseBody = getExecutionTree(ifThenElse.elseStatement, duplicateListOfList(symbolTable))
        
        trueBranch = ExecutionTreeNode(str(constraints), thenBody.variables, 'True-Branch')
        trueBranch.right = thenBody

        if elseBody:
            falseBranch = ExecutionTreeNode('!(' + str(constraints) + ')', elseBody.variables, 'False-Branch')
            falseBranch.right = elseBody
        else:
            falseBranch = ExecutionTreeNode('!(' + str(constraints) + ')', duplicateListOfList(symbolTable), 'False-Branch')
            falseBranch.right = elseBody
        
        ifThenNode = ExecutionTreeNode(None, symbolTable[0:], 'If-Then-Else')
        ifThenNode.left = trueBranch
        ifThenNode.right = falseBranch

        retNode = ifThenNode

    elif (type(statement) == Printf):
        node = ExecutionTreeNode(None, symbolTable[0:], 'Print')
        retNode = node
    
    elif (type(statement) == Assignment):
        varName = statement.identifier.value
        value = getExpressionValue(statement.expression, duplicateListOfList(symbolTable))

        symbolExist = False
        for symbol in symbolTable:
            if symbol[0] == varName:
                symbol[1] = value
                symbolExist = True
                break
        if not symbolExist:
            symbolTable.append([varName, value])

        node = ExecutionTreeNode(None, duplicateListOfList(symbolTable), 'Assignment')
        
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