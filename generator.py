from io import TextIOWrapper
from random import randint,uniform



__PRIMES__ = {
    "Amarillo":800,
    "Azul":600,
    "Blanco":1000,
    "Negro":900,
    "Rojo":600
}

__LOWER_P_LIMIT__ = 0
__UPPER_P_LIMIT__ = 99
__N_PRIMES__ = 5

def truncate(num,n):
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return float(temp[:x+n+1])
            except:
                return float(temp)      
    return float(temp)

def createTest():
    nFinalVariables = int(input("Cantidad de Variables: "))
    file = open("muestra.lp", "w")
    file.write("max: ")
    variableList = createRandomVariableAndUtility(nFinalVariables, file)
    requirementsList = []
    for i in range(nFinalVariables):
        requirementsList.append(createRequirements(requirementsList, file))
    printList(requirementsList)
    createRestrictions(requirementsList, nFinalVariables, file)
    file.close()

def createRandomVariableAndUtility(nFinalVariables : int, file : TextIOWrapper):
    variablesList = []
    for i in range(nFinalVariables):
        name = "x"+str(i+1)
        utility = randint(10000,20000)
        variablesList.append([name,utility])
        
        if i == nFinalVariables-1:
            file.write(str(utility)+str(name)+";\n")
        else:
            file.write(str(utility)+str(name)+"+")
    return variablesList
    
def createRequirements(requirementsList : list, file : TextIOWrapper):
    usedPrimes = []
    auxList = []
    cuantityOfPrimes = randint(2, __N_PRIMES__)
    totalRequirement = 100
    primeColors = list(__PRIMES__.keys())

    for i in range(cuantityOfPrimes):
        if(totalRequirement == 0):
            break

        percentage = randint(__LOWER_P_LIMIT__, __UPPER_P_LIMIT__)
        if percentage > totalRequirement or i == cuantityOfPrimes-1:
            percentage = totalRequirement
        totalRequirement -= percentage

        if percentage != 0:
            # Repeated colors verifier
            primeColor = primeColors[randint(0,4)]
            while primeColor in usedPrimes:
                primeColor = primeColors[randint(0,4)]
            usedPrimes.append(primeColor)
                   
            auxList.append([primeColor,truncate(float(percentage/100.00),2)])
    auxList.sort()
    if auxList in requirementsList:
        return createRequirements(requirementsList, file)
    else:
        return auxList
            
def createRestrictions(requirementList : list, nFinalVariables : int, file : TextIOWrapper):
    primeColors = list(__PRIMES__.keys())
    for i in range(__N_PRIMES__):
        restrictionString = ""
        selectedColor = primeColors[i]
        print(selectedColor)
        nVariable = 1
        for requirement in requirementList:
            for color,value in requirement:
                if selectedColor == color:
                    restrictionString += str(value)+"x"+str(nVariable)+"+"
            nVariable+=1
        restrictionString = restrictionString[:-1]+"<="+str(__PRIMES__[selectedColor])+";\n"
        file.write(restrictionString)
        


def printList(list):
    for i in list:
        print(i)
        

if '__main__' == __name__:
    createTest()
    print("Finished creating test")
    
    
