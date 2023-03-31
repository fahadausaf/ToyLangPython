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



def getExecutionTree(statement, symbolTable = []):
    print(symbolTable)

    # node to return after function execution
    retNode = None
    
    if (type(statement) == StatementSequence):
        left, symbolTable = getExecutionTree(statement.left, symbolTable[0:])

        if statement.right is None:
            right = None
        else:
            right, symbolTable = getExecutionTree(statement.right, symbolTable[0:])

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
                # add new symbol in symbolTable only if it does not already exist
                if not [symbol for symbol in symbolTable if symbol[0] == varName]:
                    symbolTable.append([varName, None])
                
        
        funBody = ExecutionTreeNode(None, varList, 'Function Declaration')
        # process function body
        if(functionDef.functionBody):
            funBody.right, symbolTable = getExecutionTree(functionDef.functionBody, symbolTable[0:])

        retNode = funBody
    
    elif (type(statement) == DeclareIntVariable):
        declare = DeclareIntVariable()
        declare = statement
        varName = declare.identifier.value
        
        print('DECLARING: ' + varName)
        print(generateExpression(declare.expression))
        value = getExpressionValue(declare.expression, symbolTable)
        print(value)

        # add variable to the symbol table
        if not [symbol for symbol in symbolTable if symbol[0] == varName]:
            symbolTable.append([varName, value])

        retNode = ExecutionTreeNode(None, (varName, value), 'Declare Int')
    
    elif (type(statement) == DeclareCharVariable):
        declare = DeclareCharVariable()
        declare = statement
        varName = declare.identifier.value
        value = getExpressionValue(declare.expression, symbolTable)

        # add variable to the symbol table
        if not [symbol for symbol in symbolTable if symbol[0] == varName]:
            symbolTable.append([varName, value])

        retNode = ExecutionTreeNode(None, (varName, value), 'Declare Char')

    elif (type(statement) == IfThenElse):
        ifThenElse = IfThenElse()
        ifThenElse = statement

        constraints = getExpressionValue(ifThenElse.ifCondition, symbolTable)
        
        thenBody, symbolTable = getExecutionTree(ifThenElse.thenStatement, symbolTable[0:])

        if ifThenElse.elseStatement is None:
            elseBody = None
        else:
            elseBody, symbolTable = getExecutionTree(ifThenElse.elseStatement, symbolTable[0:])
        
        trueBranch = ExecutionTreeNode(str(constraints), None, 'True-Branch')
        trueBranch.right = thenBody

        falseBranch = ExecutionTreeNode('!(' + str(constraints) + ')', None, 'False-Branch')
        falseBranch.right = elseBody
        
        ifThenNode = ExecutionTreeNode(None, None, 'If-Then-Else')
        ifThenNode.left = trueBranch
        ifThenNode.right = falseBranch

        retNode = ifThenNode

    elif (type(statement) == Printf):
        node = ExecutionTreeNode(None, None, 'Print')
        retNode = node
    
    elif (type(statement) == Assignment):
        varName = statement.identifier.value
        value = getExpressionValue(statement.expression, symbolTable)
        node = ExecutionTreeNode(None, (varName, value), 'Assignment')
        for symbol in symbolTable:
            if symbol[0] == varName:
                symbol[1] = value
        
        retNode = node
    
    elif (type(statement) == Statement):
        retNode = None
    
    elif (type(statement) == EndFile):
        retNode = None
    
    else:
        print('Unknown Statement')
        print(type(statement))
        retNode = None

    return retNode, symbolTable[0:]