from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#works with https://www.seriouseats.com
def getIngredientsFromWebScraping(url):
    # Set up Selenium
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait until the specific div with ingredients is loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "structured-ingredients_1-0")))

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the div with the specific ID
    ingredients_div = soup.find('div', id='structured-ingredients_1-0')

    if not ingredients_div:
        print("Could not find the ingredients section on this page.")
        driver.quit()
        return []

    # Extract the text from each list item within the div
    ingredients = []
    for li in ingredients_div.find_all('li'):
        # Join text with spaces where necessary
        ingredient_text = ' '.join(li.stripped_strings)
        ingredients.append(ingredient_text)

    driver.quit()

    return ingredients

# # Usage example
# url = 'https://www.seriouseats.com/bravetarts-devils-food-cake'
# url = 'https://www.seriouseats.com/best-chocolate-cupcake-recipe-8700276'
# ingredients = getIngredientsFromWebScraping(url)
#
# print("\nIngredients found:")
# for ingredient in ingredients:
#     print(ingredient)
