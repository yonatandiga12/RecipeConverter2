# File: business/recipe_processor.py

from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import matplotlib.image as mpimg
from Business.Conversions import convertToGrams
from Business.RecipeObject import RecipeObject
from Business.convertToText import readPictureFromWeb
from Business.seleniumConvertToText import getIngredientsFromWebScraping
from Business.GoogleSearch import search_dessert_google


@dataclass
class ProcessingResult:
    success: bool
    error_message: Optional[str] = None
    original_ingredients: List[str] = None
    converted_ingredients: List[str] = None
    instructions: List[str] = None
    formatted_results: str = ""
    resultList: List[RecipeObject] = None


class RecipeProcessor:
    def __init__(self):
        self.mask = np.ones((490, 500))

    def process_url(self, url: str) -> ProcessingResult:
        """
        Process a recipe URL to extract and convert ingredients
        """
        if url is None:
            return ProcessingResult(
                success=False,
                error_message="No URL provided"
            )

        original, new_ingredients, instructions = self._start_func_from_web_scraping(url)

        if original is None:
            if new_ingredients is None:
                return ProcessingResult(
                    success=False,
                    error_message="Site is not configured in the system!"
                )
            elif isinstance(new_ingredients, str):
                return ProcessingResult(
                    success=False,
                    error_message=new_ingredients
                )

        recipe_obj = RecipeObject("", "", url)
        recipe_obj.setConvertedIngredients(new_ingredients)
        recipe_obj.setOriginalIngredients(original)
        recipe_obj.setInstructions(instructions)

        return ProcessingResult(
            success=True,
            original_ingredients=recipe_obj.getOriginalIngredients(),
            converted_ingredients=recipe_obj.getConvertedIngredients(),
            instructions=recipe_obj.getInstructions()
        )

    def process_image(self, path: str) -> ProcessingResult:
        """
        Process a recipe image to extract and convert ingredients
        """
        try:
            original, converted = self._start_func_from_image(path)

            return ProcessingResult(
                success=True,
                original_ingredients=original,
                converted_ingredients=converted,
                instructions=[]
            )
        except Exception as e:
            return ProcessingResult(
                success=False,
                error_message=f"Error processing image: {str(e)}"
            )

    def search_recipes(self, query: str) -> ProcessingResult:
        """
        Search for dessert recipes
        """
        try:
            results = search_dessert_google(query)
            if not results:
                return ProcessingResult(
                    success=False,
                    error_message="No results found or an error occurred."
                )

            # Sort results by review count
            results.sort(key=lambda x: x.reviews_count, reverse=True)

            # Format results into a string
            #formatted_results = "\n".join([item.__str__() for item in results])

            return ProcessingResult(
                success=True,
                #formatted_results=formatted_results
                resultList=results
            )
        except Exception as e:
            return ProcessingResult(
                success=False,
                error_message=f"Error searching recipes: {str(e)}"
            )

    def _start_func_from_web_scraping(self, url: str):
        """
        Internal method to process URL using web scraping
        """
        result = []
        ingredients_and_directions = getIngredientsFromWebScraping(url)

        if ingredients_and_directions is None:
            return None, None

        if isinstance(ingredients_and_directions, str):
            return None, ingredients_and_directions

        ingredients = ingredients_and_directions["ingredients"]
        instructions = ingredients_and_directions["instructions"]

        if isinstance(ingredients, str):
            return None, ingredients

        for sentence in ingredients:
            curr = convertToGrams(sentence)
            result.append(curr)

        return ingredients, result, instructions

    def _start_func_from_image(self, path: str):
        """
        Internal method to process image and extract ingredients
        """
        converted = []
        img = mpimg.imread(path)
        ingredients = readPictureFromWeb(img)

        for sentence in ingredients:
            curr = convertToGrams(sentence)
            converted.append(curr)

        return ingredients, converted