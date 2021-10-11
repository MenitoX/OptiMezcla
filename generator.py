from io import TextIOWrapper
from random import randint

# Variables Globales

__PRIMES__ = {}
__N_PRIMES__ = 0

# Constantes

    # Cambiables #
__LOWER_AVAILABILITY__ = 5000
__UPPER_AVAILABILITY__ = 10000
__LOWER_UTILITY__ = 10000
__UPPER_UTILITY__ = 20000

    # No tocar #
__LOWER_P_LIMIT__ = 0
__UPPER_P_LIMIT__ = 99


# Función para truncar Floats
def truncate(num : float , n : int):
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return float(temp[:x+n+1])
            except:
                return float(temp)      
    return float(temp)

# Función main
def createTest():
    global __N_PRIMES__
    nFinalVariables = int(input("Cantidad de Variables: "))
    __N_PRIMES__ = int(input("Cantidad de materias primas: "))
    file = open("muestra.lp", "w")
    file.write("max: ")
    createPrimes()
    createRandomVariableAndUtility(nFinalVariables, file)
    requirementsList = []
    for i in range(nFinalVariables):
        requirementsList.append(createRequirements(requirementsList, file))
    createRestrictions(requirementsList, file)
    file.close()

# Crea las materias primas
def createPrimes():
    global __PRIMES__
    for i in range(__N_PRIMES__):
        key = "color"+str(i+1)
        __PRIMES__[key] = randint(__LOWER_AVAILABILITY__, __UPPER_AVAILABILITY__)

# Crea variables junto a su utilidad en un rango específico,
# y forma la función objetivo
def createRandomVariableAndUtility(nFinalVariables : int, file : TextIOWrapper):
    for i in range(nFinalVariables):
        name = "x"+str(i+1)
        utility = randint(__LOWER_UTILITY__,__UPPER_UTILITY__)       
        if i == nFinalVariables-1:
            file.write(str(utility)+str(name)+";\n")
        else:
            file.write(str(utility)+str(name)+"+")
    return 

# Crea los requerimientos de cada variable, o sea el porcentaje de materias
# primas por variable    
def createRequirements(requirementsList : list, file : TextIOWrapper):
    usedPrimes = []
    auxList = []
    if __N_PRIMES__ != 2:
        cuantityOfPrimes = randint(2, __N_PRIMES__)
    else:
        cuantityOfPrimes = 2
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
    
    # Este sort permite que las materias primas siempre estén en el mismo orden para
    # poder comparar si ya existen en la lista de requerimientos 
    auxList.sort()

    if auxList in requirementsList or len(auxList) == 1:
        return createRequirements(requirementsList, file)
    else:
        return auxList

# Crea las restricciones de cada materia prima respecto a la lista de requerimientos
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
        if colorsDic[key] != "":
            colorsDic[key] = colorsDic[key][:-1]+"<="+str(__PRIMES__[key])+";\n"
            file.write(colorsDic[key])
        
if '__main__' == __name__:
    createTest()
    print("Finished creating test")
