from unittest import TestCase

from Business.seleniumConvertToText import getIngredientsFromWebScraping


class Test(TestCase):



    def test_getIngredientsFromWebScraping_GoodFood(self):
        result = getIngredientsFromWebScraping("https://www.bbcgoodfood.com/recipes/easy-chocolate-cake")
        ingredients = result["ingredients"]
        instructions = result["instructions"]

        self.assertTrue(len(ingredients) == 22)
        self.assertTrue(len(instructions) == 11)
        self.assertEqual('25g white chocolate', ingredients[20])
        self.assertEqual('Shake the tray gently to level the mixture then leave to set somewhere cool. Chop into shards.',
                         instructions[10])


    def test_getIngredientsFromWebScraping_GoodFood2(self):
        result = getIngredientsFromWebScraping("https://www.bbcgoodfood.com/recipes/chocolate-chunk-cookies")
        ingredients = result["ingredients"]
        instructions = result["instructions"]

        self.assertTrue(len(ingredients) == 9)
        self.assertTrue(len(instructions) == 2)
        self.assertEqual('75g light brown sugar', ingredients[1])
        self.assertTrue('for a few mins before eating warm,' in instructions[1])



    def test_getIngredientsFromWebScraping_Sally1(self):
        result = getIngredientsFromWebScraping("https://sallysbakingaddiction.com/coffee-cake-recipe/")
        ingredients = result["ingredients"]
        instructions = result["instructions"]

        self.assertTrue(len(ingredients) == 23)
        self.assertTrue(len(instructions) == 9)
        self.assertEqual('Cinnamon Crumb Mixture', ingredients[0])
        self.assertEqual('1/4 teaspoon salt', ingredients[10])

        self.assertTrue('Cover leftovers tightly and store at room temperature' in instructions[8])


    def test_getIngredientsFromWebScraping_Sally2(self):
        result = getIngredientsFromWebScraping("https://sallysbakingaddiction.com/rice-krispie-treats/#tasty-recipes-68467")
        ingredients = result["ingredients"]
        instructions = result["instructions"]

        self.assertTrue(len(ingredients) == 6)
        self.assertTrue(len(instructions) == 7)
        self.assertEqual('9 cups ( 270g ) crispy rice cereal', ingredients[4])
        self.assertTrue('Cover and store leftover treats at room temperature for up to 3 days' in instructions[6])

