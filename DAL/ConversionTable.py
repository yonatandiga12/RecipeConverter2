import csv
import os

ingredientsDict = dict()
TSP = 0
TBSP = 1
CUP = 2
OZ = 3

# return all the ingredients saved in the conversion table!
def getAllIngredients():
    # it checks if we pulled it already to memory for fewer I/O operations.
    if len(ingredientsDict) != 0:
        return ingredientsDict.keys()

    uploadFromCSV()

    return ingredientsDict.keys()


# return the amount in grams of this ingredient in this unit, for example: "flour", "tbsp" should return 9
def getWeightOfIngredientInUnit(ingredient, unit):
    if len(ingredientsDict) == 0:
        uploadFromCSV()

    if unit < 0:
        return -1

    keyRepresentation = getIngredientKeyRepresentation(ingredient)
    if keyRepresentation in ingredientsDict.keys():
        return ingredientsDict[keyRepresentation][unit]

    return -1

def getIngredientKeyRepresentation(ingredient):
    for currIngredient in ingredientsDict.keys():   #The ingredient has multiple names in the table
        currSplitted = currIngredient.split(';')
        if ingredient in currSplitted:            #so if one of them matches return the key
            return currIngredient
    return ""


def uploadFromCSV():
    dirPath = os.path.dirname(os.path.realpath(__file__))
    tablePath = dirPath + '/table.csv'
    with open(tablePath, 'r') as file:
        csvreader = list(csv.reader(file, delimiter=','))
        firstRow = list(csvreader.pop(0))

        tspTableIndex = firstRow.index('tsp')
        tbspTableIndex = firstRow.index('tbsp')
        cupTableIndex = firstRow.index('cup')

        for row in csvreader:
            ingredientsDict[row[0].lower()] = (convertToFloat(row[tspTableIndex]),
                                       convertToFloat(row[tbspTableIndex]),
                                       convertToFloat(row[cupTableIndex]), 28.35)



def convertToFloat(frac_str):
    if frac_str == "":
        return -1
    try:
        frac_str = frac_str.replace(",", "")
        return float(frac_str)
    except ValueError:
        try:
            num, denom = frac_str.split('/')
        except ValueError:
            return None
        try:
            leading, num = num.split(' ')
        except ValueError:
            try:
                return float(num) / float(denom)
            except ValueError:
                return -1
        if float(leading) < 0:
            sign_mult = -1
        else:
            sign_mult = 1
        return float(leading) + sign_mult * (float(num) / float(denom))





