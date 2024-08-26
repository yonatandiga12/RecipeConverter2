import re
from DAL.ConversionTable import *

tbspList = ['tbsp', 'tablespoon']
tspList = ['tsp', 'teaspoon']
cupsList = ['cup', 'cups']
ounceList = ['ounce', 'oz']
keywords = tspList + tbspList + cupsList + ounceList


def getUnitIndexInSentence(sentence, unit):
    searchIn = list()
    if unit == TBSP:
        searchIn = tbspList
    elif unit == TSP:
        searchIn = tspList
    elif unit == CUP:
        searchIn = cupsList
    elif unit == OZ:
        searchIn = ounceList

    for name in searchIn:
        try:
            index = sentence.index(name)
            if index != -1:
                return index
        except ValueError:
            index = -1

    return -1


def convertStringToNumber(sentence, unit):  ##
    p = '[-]?[0-9]+[,.]?[0-9]*([\\/][0-9]+[,.]?[0-9]*)*'

    unitIndex = getUnitIndexInSentence(sentence, unit)
    if unitIndex == -1:
        return -1

    numberFound = re.search(p, sentence[:unitIndex])
    if numberFound is None:
        return -1

    numberFound = numberFound.string

    removeChars = ['(', ')', 'and', '[', ']', '_', '=']    #remove interfering chars from number
    for char in removeChars:
        if char in numberFound:
            numberFound = numberFound.replace(char, " ")

    numberFound = "".join(c for c in numberFound if not c.isalpha())  #remove letters from number

    return convertToFloat(numberFound)


def gramsExists(sentence):
    if 'gram' in sentence:
        return True

    sentencedWithoutSpace = sentence.replace(" ", "")  # if there is 400 g and not 400g
    numbersFound = re.findall(r'\d+', sentence)
    for number in numbersFound:
        index = sentencedWithoutSpace.find(number) + len(number)
        if index < len(sentencedWithoutSpace):
            if sentencedWithoutSpace[index] == 'g':  # There is a number and than g, that means 400g
                return True
    return False



def findMatchWithLowestIndex(subStrings, sentence):
    if len(subStrings) == 0:
        return ""
    bestSub = subStrings[0]
    minIndex = sentence.index(bestSub)
    if len(subStrings) == 1:
        return bestSub
    else:
        for subString in subStrings:
            currIndex = sentence.index(subString)
            if currIndex < minIndex:
                minIndex = currIndex
                bestSub = subString
            #if I have another ingredient but longer, its probably better.
            #example : 1 cup of coconut milk. if by accident we have [coconut, coconut milk] the
            # coconut milk will be chosen
            if currIndex == minIndex and len(subString) > len(bestSub):
                minIndex = currIndex
                bestSub = subString
    return bestSub


def getIngredientFromSentence(sentence):
    allIngredients = getAllIngredients()

    foundList = list()  # put results to list if we have for example "flour" and "self-raising flour"
    for ingredientNames in allIngredients:
        sameCategoryList = list()
        for ingredient in ingredientNames.split(';'):
            if ingredient in sentence:
                sameCategoryList.append(ingredient)
                #foundList.append(ingredient)
        if len(sameCategoryList) > 0:
            foundList.append(sameCategoryList)

    if len(foundList) != 0:
        if len({len(i) for i in foundList}) == 1:                     #if it matches several ingredient and all of them
            flatList = [item for sublist in foundList for item in sublist]  #has the same chance to be the ingredient
            return max(flatList, key=len)

        longestList = max(foundList, key=len)

        return findMatchWithLowestIndex(longestList, sentence)

    return ""  # found nothing!


def getAmountOfIngredientInGrams(ingredient, amount, unit):
    # result should be like this : "50g flour"
    weightOfUnit = getWeightOfIngredientInUnit(ingredient, unit)
    if amount <= 0 or weightOfUnit == -1:
        return ""

    totalWeight = str(round(amount * weightOfUnit, 3))
    if totalWeight[-1] == '0' and totalWeight[-2] == '.':
        totalWeight = totalWeight[:-2]
    return totalWeight + " g " + ingredient.strip()


def convertUnitToGrams(sentence, unit):
    if gramsExists(sentence):
        return sentence

    # if there are no gram, search the number of the units we need to convert and convert it by the unit
    amount = convertStringToNumber(sentence, unit)

    ingredient = getIngredientFromSentence(sentence)

    if amount == -1 or ingredient == '':  # couldn't find number of ingredient in the sentence
        return sentence

    result = getAmountOfIngredientInGrams(ingredient, amount, unit)
    if result == "":
        return sentence

    return result


def convertToGrams(sentence: str):
    currLower = sentence.lower()
    if any(a in currLower for a in tbspList):
        return convertUnitToGrams(currLower, TBSP)
    elif any(a in currLower for a in tspList):
        return convertUnitToGrams(currLower, TSP)
    elif any(a in currLower for a in cupsList):
        return convertUnitToGrams(currLower, CUP)
    elif any(a in currLower for a in ounceList):
        return convertUnitToGrams(currLower, OZ)
    else:
        return currLower  # No need to convert this sentence to grams



# for tests!
def getNumOfUnit(unitString):
    if unitString == 'cup':
        return CUP
    elif unitString == 'tsp':
        return TSP
    elif unitString == 'tbsp':
        return TBSP
    elif unitString == 'oz':
        return OZ
    else:
        return -1


if __name__ == '__main__':
    print('Conversions')
    uploadFromCSV()

