import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from Business.RecipeObject import RecipeObject
from Business.seleniumConvertToText import SUPPORTED_SITES


def search_dessert_google(dessert):
    """
    Searches Google for the dessert query, extracts recipe title, URL, rating,
    and the number of people who rated it, only within the current 'MjjYud' div.
    """
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    # service = Service()  # Automatically detects ChromeDriver

    driver_path = os.path.join(
        os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__),
        'chromedriver.exe')
    service = Service(executable_path=driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    RECIPES_COUNTER = 5
    results = []
    driver = None
    for site in SUPPORTED_SITES:
        query = f"{dessert} site:{site}.com"
        print(f"Searching: {query}")

        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(f"https://www.google.com/search?q={query}")
            driver.implicitly_wait(5)

            # Parse the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Locate the recipe blocks (MjjYud divs)
            blocks = soup.find_all('div', class_='MjjYud')
            for i in range(RECIPES_COUNTER):
                recipe_block = blocks[i]
                # Extract title
                h3_tag = recipe_block.find('h3')
                title = h3_tag.get_text() if h3_tag else None

                # Extract URL from the parent 'a' tag
                parent_a = h3_tag.find_parent('a') if h3_tag else None
                url = parent_a['href'] if parent_a and 'href' in parent_a.attrs else None

                # Extract rating and reviews (within the same div block)
                rating_tag = recipe_block.find('span', class_='yi40Hd YrbPuc')  # Rating
                rating = rating_tag.get_text() if rating_tag else None

                reviews_tag = recipe_block.find('span', class_='RDApEe YrbPuc')  # Reviews
                reviews_count = reviews_tag.get_text() if reviews_tag else 0

                if reviews_count != 0:
                    reviews_count = int(''.join([char for char in reviews_count if char.isalnum()]))
                if rating is not None:
                    rating = float(rating)

                # Create RecipeObject instance if title and URL exist
                if title and url:
                    recipe_obj = RecipeObject(site, title, url)
                    recipe_obj.rating = rating
                    recipe_obj.reviews_count = reviews_count
                    results.append(recipe_obj)

        except Exception as e:
            print("Error:", e)
        finally:
            if driver is not None:
                driver.quit()

    return results
