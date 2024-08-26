from Business.Conversions import convertToGrams
from Business.convertToText import readPicture


def startFunc():
    result = list()
    ingredients = readPicture('recipe6.jpg')
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        result.append(curr)

    for curr in result:
        print(curr)




if __name__ == '__main__':
    startFunc()



