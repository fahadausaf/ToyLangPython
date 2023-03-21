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
    newCode = ''
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