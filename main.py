from Business.Conversions import convertToGrams
from Business.convertToText import readPicture
from Presenation.app_ui import RecipeConverterUI


def startFunc():
    result = list()
    ingredients = readPicture('recipe6.jpg')
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        result.append(curr)

    for curr in result:
        print(curr)




if __name__ == '__main__':
    #startFunc()
    app = RecipeConverterUI()
    app.run()



