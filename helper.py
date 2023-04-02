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
def parseExecutionTree(node, exprlst = ''):
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
        parseExecutionTree(node.left, exprlst)
    if node.right:
        parseExecutionTree(node.right, exprlst)


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