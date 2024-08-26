import unittest
from unittest import TestCase
from Business.Conversions import *


class TestConversions(TestCase):


    def test_convertStringToNumber_Valid(self):
        result = convertStringToNumber("1 1/2 cup milk", getNumOfUnit('cup'))
        self.assertEqual(result, 1.5)

        result = convertStringToNumber("5/2 tbsp milk", getNumOfUnit('tbsp'))
        self.assertEqual(result, 2.5)

        result = convertStringToNumber("1 cup milk", getNumOfUnit('cup'))
        self.assertEqual(result, 1)

        result = convertStringToNumber("1.5 cup milk", getNumOfUnit('cup'))
        self.assertEqual(result, 1.5)

        result = convertStringToNumber("0.5 cup milk", getNumOfUnit('cup'))
        self.assertEqual(result, 0.5)


        result = convertStringToNumber("1/3 cup milk", getNumOfUnit('cup'))
        self.assertEqual(result, 1/3)

        result = convertStringToNumber("10 tablespoons (145 grams) unsalted butter", getNumOfUnit('tbsp'))
        self.assertEqual(result, 10)

    def test_convertStringToNumber_ShouldFail(self):

        result = convertStringToNumber("1 large egg", getNumOfUnit('cup'))
        self.assertEqual(result, -1)

        result = convertStringToNumber("1 tbsp flour", getNumOfUnit('cup'))
        self.assertEqual(result, -1)

        result = convertStringToNumber("1 cup flour", getNumOfUnit('tsp'))
        self.assertEqual(result, -1)

        result = convertStringToNumber("1 tsp flour", getNumOfUnit('tbsp'))
        self.assertEqual(result, -1)

        result = convertStringToNumber("85g plain flour", getNumOfUnit('tbsp'))
        self.assertEqual(result, -1)

    def test_gramsExists_Valid(self):
        self.assertTrue(gramsExists("400g flour"))
        self.assertTrue(gramsExists("400 g flour"))
        self.assertTrue(gramsExists("400 gram flour"))
        self.assertTrue(gramsExists("400 grams flour"))
        self.assertTrue(gramsExists("1.5g flour"))
        self.assertTrue(gramsExists("1.5 grams grams flour"))
        self.assertTrue(gramsExists("1 1/2g flour"))
        self.assertTrue(gramsExists("1 1/2 grams flour"))
        self.assertTrue(gramsExists("3/2 grams flour"))
        self.assertTrue(gramsExists("1 cup (140g) flour"))
        self.assertTrue(gramsExists("1 cup (140 g) flour"))

    def test_gramsExists_Fail(self):
        self.assertFalse(gramsExists("1 cup flour"))
        self.assertFalse(gramsExists("1 cup granola"))
        self.assertFalse(gramsExists("1 tsp flour"))
        self.assertFalse(gramsExists("1 tsp flour"))

    def test_getIngredientFromSentence(self):
        result = getIngredientFromSentence("1 cup flour")
        self.assertEqual(result, "flour")

        result = getIngredientFromSentence("1 cup whole wheat flour")
        self.assertEqual(result, "whole wheat flour")

        result = getIngredientFromSentence("1 cup butter")
        self.assertEqual(result, " butter")

        result = getIngredientFromSentence("2 tsp coconut")
        self.assertEqual(result, "coconut")

        result = getIngredientFromSentence("2 tsp sugar")
        self.assertEqual(result, "sugar")

        result = getIngredientFromSentence("2 tsp powdered sugar")
        self.assertEqual(result, "powdered sugar")

        result = getIngredientFromSentence("2 tsp water")
        self.assertEqual(result, "water")

        result = getIngredientFromSentence("2 tsp cornstarch")
        self.assertEqual(result, "cornstarch")

    def test_getUnitIndexInSentence_Valid(self):
        result = getUnitIndexInSentence("1 cup flour", getNumOfUnit('cup'))
        self.assertEqual(result, 2)

        result = getUnitIndexInSentence("1 tablespoon flour", getNumOfUnit('tbsp'))
        self.assertEqual(result, 2)

        result = getUnitIndexInSentence("1  tablespoon flour", getNumOfUnit('tbsp'))
        self.assertEqual(result, 3)

        result = getUnitIndexInSentence("1  tsp flour", getNumOfUnit('tsp'))
        self.assertEqual(result, 3)

        result = getUnitIndexInSentence("4444 teaspoons flour", getNumOfUnit('tsp'))
        self.assertEqual(result, 5)

    def test_getUnitIndexInSentence_Fail(self):
        result = getUnitIndexInSentence("1 cup flour", getNumOfUnit('tsp'))
        self.assertEqual(result, -1)

        result = getUnitIndexInSentence("1 tablespoon flour", getNumOfUnit('tsp'))
        self.assertEqual(result, -1)

        result = getUnitIndexInSentence("1  tablespoon flour", getNumOfUnit('cup'))
        self.assertEqual(result, -1)

    def test_getAmountOfIngredientInGrams_Valid(self):
        result = getAmountOfIngredientInGrams('flour', 3, getNumOfUnit('cup'))
        self.assertEqual(result, '420 g flour')

        result = getAmountOfIngredientInGrams('flour', 3, getNumOfUnit('tbsp'))
        self.assertEqual(result, '23.4 g flour')

        result = getAmountOfIngredientInGrams('flour', 3, getNumOfUnit('tsp'))
        self.assertEqual(result, '7.5 g flour')

        result = getAmountOfIngredientInGrams('flour', 3, getNumOfUnit('oz'))
        self.assertEqual(result, '85.05 g flour')

        result = getAmountOfIngredientInGrams('sugar', 10, getNumOfUnit('cup'))
        self.assertEqual(result, '2000 g sugar')

        result = getAmountOfIngredientInGrams('sugar', 10, getNumOfUnit('tsp'))
        self.assertEqual(result, '42 g sugar')

        result = getAmountOfIngredientInGrams('sugar', 10, getNumOfUnit('tbsp'))
        self.assertEqual(result, '125 g sugar')

        result = getAmountOfIngredientInGrams('sugar', 10, getNumOfUnit('oz'))
        self.assertEqual(result, '283.5 g sugar')

    def test_getAmountOfIngredientInGrams_Fail(self):
        result = getAmountOfIngredientInGrams('sugar', 0, getNumOfUnit('oz'))
        self.assertEqual(result, "")

        result = getAmountOfIngredientInGrams('sugar', -1, getNumOfUnit('oz'))
        self.assertEqual(result, "")

        #ingredient not existing
        result = getAmountOfIngredientInGrams('made up ingredient', 0, getNumOfUnit('oz'))
        self.assertEqual(result, "")

        result = getAmountOfIngredientInGrams('sugar', 3, getNumOfUnit('gg'))
        self.assertEqual(result, "")

    def test_convertToFloat(self):
        self.assertEqual(convertToFloat("1.3"), 1.3)
        self.assertEqual(convertToFloat("1"), 1)
        self.assertEqual(convertToFloat("1 1/2"), 1.5)
        self.assertEqual(convertToFloat("5/2"), 2.5)
        self.assertEqual(convertToFloat("1,500"), 1500)


        self.assertEqual(convertToFloat("1*5"), None)
        self.assertEqual(convertToFloat("1-5"), None)
        self.assertEqual(convertToFloat("a"), None)
        self.assertEqual(convertToFloat("#"), None)



    def test_convertUnitToGrams_ConfusingIngredients(self):
        result = convertUnitToGrams("1 cup buttermilk", getNumOfUnit("cup"))
        self.assertEqual(result, "240 g buttermilk")

        result = convertUnitToGrams("1 cup butter", getNumOfUnit("cup"))
        self.assertEqual(result, "227 g butter")

        result = convertUnitToGrams("1 cup milk", getNumOfUnit("cup"))
        self.assertEqual(result, "240 g milk")

        result = convertUnitToGrams("1 cup coconut milk", getNumOfUnit("cup"))
        self.assertEqual(result, "240 g coconut milk")

        result = convertUnitToGrams("1 cup milk or buttermilk or coconut milk", getNumOfUnit("cup"))
        self.assertEqual(result, "240 g milk")

        result = convertUnitToGrams("1 cup coconut milk or buttermilk or milk", getNumOfUnit("cup"))
        self.assertEqual(result, "240 g coconut milk")


if __name__ == '__main__':
    unittest.main()



