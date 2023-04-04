from datetime import datetime
from grammar import *
from codeGenerator import *

class Enumm(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

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

negation = False
def getSMTExpressionValue(expression, symbolTable=[]):
    global negation
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
        if negation:
            code = code + '(' + ident + ')'
            negation = False
        else:
            code = code + ident

    elif (type(expression) == ArithmaticExpression):
        code = getSMTExpressionValue(expression.left, symbolTable)
        code = code + generateArithmaticOperand(expression.operand)
        code = code + getSMTExpressionValue(expression.right, symbolTable)

    elif (type(expression) == LogicExpression):
        code = getSMTExpressionValue(expression.left, symbolTable)
        code = code + generateSMTLogicOperand(expression.operand)
        code = code + getSMTExpressionValue(expression.right, symbolTable)

    elif (type(expression) == UnaryExpression):
        unaryExp = UnaryExpression()
        unaryExp = expression

        if unaryExp.operand == UnaryOperands.Minus:
            code = code + '-'
        else:
            code = code + 'Not'
            negation = True

        code = code + getSMTExpressionValue(unaryExp.expression, symbolTable)
    return code

def printTokens(tokenList):
    n = 1
    for t in tokenList:
        print('No: ' + str(n))
        print('Token: ' + str(t[0]))
        print('Line: ' + str(t[1]) + ', Col: ' + str(t[2]) + '\n')
        n += 1

def prettyPrint(code):
    newCode = '\n'
    noOfBrac = 0
    tab = False
    for line in code.splitlines():
        tmpTab = ''
        newLine = ''
        
        if(line == '}'):
            noOfBrac -= 1
            if noOfBrac == 0:
                tab = False   
        
        if tab:
            for x in range(noOfBrac):
                tmpTab = tmpTab + '\t'
        newLine = tmpTab + line + '\n'
        
        
        if(line == '{'):
            noOfBrac += 1
            tab = True
        

        newCode = newCode + newLine

    return newCode

def getConstraints(node):
    case_no = 0
    def getCons(node, constlst = ''):
        if node.constraints:
            if(constlst == ''):
                constlst = node.constraints
            else:
                constlst = constlst + ', ' + node.constraints
            
        if (not node.left and not node.right):
            case_no += 1
            print('Case ' + str(case_no) + ': ' + constlst)
        if node.left:
            getCons(node.left, constlst)
        if node.right:
            getCons(node.right, constlst)

def getSymbols(node):
    global case_no
    case_no = 0
    def getSym(node, symlst = []):
        global case_no
        if node.symbols:
            if isinstance(node.symbols, list):
                for s in node.symbols:
                    print()
                    ident = s[0]
                    val = s[1]
                    symlst.append([ident, val])
            else:
                ident = node.symbols[0]
                val = node.symbols[1]
                symlst.append([ident, val])
        
        if not node.left and not node.right:
            case_no += 1
            print('\nCase: ' + str(case_no))
            for sym in symlst:
                print(sym)
        if node.left:
            getSym(node.left, cloneListOfList(symlst))
        if node.right:
            getSym(node.right, cloneListOfList(symlst))

    getSym(node)

seq_no = 0
def getVariables(node, constlst=[]):
    global seq_no
    if node.variables:
        constlst.append(node.variables)
        
    if (not node.left and not node.right):
        seq_no += 1
        print('Case ' + str(seq_no) + ': ')
        for c in constlst:
            print(c)
        print()
    if node.left:
        getVariables(node.left, constlst)
    if node.right:
        getVariables(node.right, constlst)

def generateFileName(fileName=''):
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    if(fileName==''):
        return dt_string
    else:
        return fileName + '_' + dt_string
    
def cloneListOfList(listOfList):
    tmpList = []
    for lst in listOfList:
        tmpList.append(lst[0:])
    return tmpList

def getExpressions(node):
    global case_no
    case_no = 0
    def getExpr(node, exprlst = ''):
        global case_no
        
        if node.condition:
            if exprlst == '':
                exprlst = node.condition[0]
            else:
                exprlst = exprlst + ' && ' + node.condition[0]
        
        if node.left:
            getExpr(node.left, exprlst)

        if node.right:
            getExpr(node.right, exprlst)

        if not node.left and not node.right:
            case_no += 1
            print('Case ' + str(case_no) + ': ' + exprlst)

    getExpr(node)

def getExecutionSequenceDetail(node):
    global case_no
    case_no = 0
    def parseET(node, exprlst = ''):
        global case_no
        symbol = '-'
        condition = '-'
        if node.symbols:
            symbol = str(node.symbols)
        if node.condition:
            condition = str(node.condition[0])
        if(exprlst == ''):
            exprlst = node.expression.ljust(25, ' ') + '\t' + symbol.ljust(40, ' ') + '\t' + condition
        else:
            exprlst = exprlst + '\n' + node.expression.ljust(25, ' ') + '\t' + symbol.ljust(40, ' ') + '\t' + condition
            
        if (not node.left and not node.right):
            case_no += 1
            print('\nCase: ' + str(case_no))
            print('Action'.ljust(25, ' ') + '\tSymbol(s)'.ljust(40, ' ') + '\t\tCondition(s)')
            print('-'.ljust(100, '-'))
            print(exprlst)
        if node.left:
            parseET(node.left, exprlst)
        if node.right:
            parseET(node.right, exprlst)
    
    parseET(node)

def getExpressionsWithValue_old(node):
    global case_no
    case_no = 0
    def getExpr(node, exprlst = '', varList = []):
        global case_no
        
        if node.symbols:
            if isinstance(node.symbols, list):
                None
            else:
                varExist = False
                for var in varList:
                    if var[0] == node.symbols[0]:
                        var[1] = node.symbols[1]
                        varExist = True
                        break
                if not varExist:
                    varList.append([node.symbols[0], node.symbols[1]])

        if node.condition:
            exprVal = '(' + str(getExpressionValue(node.condition[1], varList)) + ')'
            if not node.condition[2]:
                exprVal = 'Not' + exprVal
            
            if exprlst == '':
                exprlst = exprVal
            else:
                exprlst = exprlst + ', ' + str(exprVal)
        
        if node.left:
            getExpr(node.left, exprlst, cloneListOfList(varList))

        if node.right:
            getExpr(node.right, exprlst, cloneListOfList(varList))

        if not node.left and not node.right:
            case_no += 1
            print('Case ' + str(case_no) + ': ' + exprlst)

    getExpr(node)

def getSMTExpressions(node):
    global exprList
    exprList = []
    
    global case_no
    case_no = 0
    
    def getExpr(node, expr = '', varList = []):
        global case_no
        global exprList 
        
        if node.symbols:
            if isinstance(node.symbols, list):
                None
            else:
                varExist = False
                for var in varList:
                    if var[0] == node.symbols[0]:
                        var[1] = node.symbols[1]
                        varExist = True
                        break
                if not varExist:
                    varList.append([node.symbols[0], node.symbols[1]])

        if node.condition:
            #print(node.condition[0])
            exprVal = str(getSMTExpressionValue(node.condition[1], varList))
            if not node.condition[2]:
                exprVal = 'Not(' + exprVal + ')'
            
            if expr == '':
                expr = exprVal
            else:
                expr = expr + ', ' + str(exprVal)
        
        if node.left:
            getExpr(node.left, expr, cloneListOfList(varList))

        if node.right:
            getExpr(node.right, expr, cloneListOfList(varList))

        if not node.left and not node.right:
            case_no += 1
            #print('print("Case " + "' + str(case_no) + '")\nsolve(' + exprlst + ')')
            exprList.append(expr)
    getExpr(node)
    return exprList

def printSMTExpressions(exprList):
    case_no = 1
    for expr in exprList:
        print('Case ' + str(case_no) + ': ' + str(expr))
        case_no += 1

