from io import TextIOWrapper
from random import randint,uniform



__PRIMES__ = {
    "Amarillo":8000,
    "Azul":6000,
    "Blanco":10000,
    "Negro":9000,
    "Rojo":6000,
    "Verde":4000,
    "Memito":11000
}

__LOWER_P_LIMIT__ = 0
__UPPER_P_LIMIT__ = 99
__N_PRIMES__ = 7

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
    createRandomVariableAndUtility(nFinalVariables, file)
    requirementsList = []
    for i in range(nFinalVariables):
        requirementsList.append(createRequirements(requirementsList, file))
    #printList(requirementsList)
    createRestrictions(requirementsList, file)
    file.close()

def createRandomVariableAndUtility(nFinalVariables : int, file : TextIOWrapper):
    for i in range(nFinalVariables):
        name = "x"+str(i+1)
        utility = randint(10000,20000)       
        if i == nFinalVariables-1:
            file.write(str(utility)+str(name)+";\n")
        else:
            file.write(str(utility)+str(name)+"+")
    return 
    
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
            primeColor = primeColors[randint(0,__N_PRIMES__-1)]
            while primeColor in usedPrimes:
                primeColor = primeColors[randint(0,__N_PRIMES__-1)]
            usedPrimes.append(primeColor)
                   
            auxList.append([primeColor,truncate(float(percentage/100.00),2)])
    auxList.sort()
    if auxList in requirementsList:
        return createRequirements(requirementsList, file)
    else:
        return auxList
            
def createRestrictions(requirementList : list, file : TextIOWrapper):
    primeColors = list(__PRIMES__.keys())
    colorsDic = {}
    for key in primeColors:
        colorsDic.setdefault(key, "")
    
    nVariable = 1
    for requirement in requirementList:
        for color,value in requirement:
            colorsDic[color] += str(value)+"x"+str(nVariable)+"+" 
        nVariable+=1
    for key in primeColors:
        colorsDic[key] = colorsDic[key][:-1]+"<="+str(__PRIMES__[key])+";\n"
        file.write(colorsDic[key])
        


def printList(list):
    for i in list:
        print(i)
        

if '__main__' == __name__:
    createTest()
    print("Finished creating test")
    
    
