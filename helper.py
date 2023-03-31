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
        exprlst = node.expression
    else:
        exprlst = exprlst + ', ' + node.expression
        
    if (not node.left and not node.right):
        path_no += 1
        path = 'Case ' + str(path_no) + ': '+ exprlst
        if len(path) > 180:
            print(path[:180] + '.....(cont.)')
        else:
            print(path)
    if node.left:
        parseExecutionTree(node.left, exprlst)
    if node.right:
        parseExecutionTree(node.right, exprlst)

case_no = 0
def getConstraints(node, constlst = ''):
    global case_no
    if node.constraints:
        if(constlst == ''):
            constlst = node.constraints
        else:
            constlst = constlst + ', ' + node.constraints
        
    if (not node.left and not node.right):
        case_no += 1
        print('Case ' + str(case_no) + ': ' + constlst)
    if node.left:
        getConstraints(node.left, constlst)
    if node.right:
        getConstraints(node.right, constlst)

def generateFileName(fileName=''):
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y_%H%M%S")
    if(fileName==''):
        return dt_string
    else:
        return fileName + '_' + dt_string