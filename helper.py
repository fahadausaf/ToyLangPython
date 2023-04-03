from datetime import datetime

class Enumm(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

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


path_no = 0
def parseExecutionTree_old(node, exprlst = ''):
    global path_no
    if(exprlst == ''):
        exprlst = node.expression + '\t' + str(node.variables)
    else:
        exprlst = exprlst + '\n' + node.expression + '\t' + str(node.variables)
        
    if (not node.left and not node.right):
        path_no += 1
        path = '\nCase ' + str(path_no) + ': \n\n'+ exprlst
        print(path)
    if node.left:
        parseExecutionTree_old(node.left, exprlst)
    if node.right:
        parseExecutionTree_old(node.right, exprlst)


def parseExecutionTree(node):
    global case_no
    case_no = 0
    def parseET(node, exprlst = ''):
        global case_no
        symbol = '-'
        constraint = '-'
        if node.symbols:
            symbol = str(node.symbols)
        if node.constraints:
            constraint = str(node.constraints)
        if(exprlst == ''):
            exprlst = node.expression.ljust(25, ' ') + '\t' + symbol.ljust(40, ' ') + '\t' + constraint
        else:
            exprlst = exprlst + '\n' + node.expression.ljust(25, ' ') + '\t' + symbol.ljust(40, ' ') + '\t' + constraint
            
        if (not node.left and not node.right):
            case_no += 1
            print('\nCase: ' + str(case_no))
            print('Action'.ljust(25, ' ') + '\tSymbol(s)'.ljust(40, ' ') + '\t\tConditions')
            print('-'.ljust(100, '-'))
            print(exprlst)
        if node.left:
            parseET(node.left, exprlst)
        if node.right:
            parseET(node.right, exprlst)
    
    parseET(node)


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
            getSym(node.left, duplicateListOfList(symlst))
        if node.right:
            getSym(node.right, duplicateListOfList(symlst))

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
    
def duplicateListOfList(listOfList):
    tmpList = []
    for lst in listOfList:
        tmpList.append(lst[0:])
    return tmpList