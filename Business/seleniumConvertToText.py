from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# works with https://www.seriouseats.com
def findSiteName(url):
    try:
        splitedUrl = url.split('.')
        return splitedUrl[1]
    except:
        return ""


def getIngredientsFromWebScraping(url):
    siteName = findSiteName(url)

    match siteName:
        case "seriouseats":
            return getFromSeriousEats(url)
        case "foodnetwork":
            return getFromFoodNetwork(url)
        case _:
            return None


def getFromFoodNetwork(url):
    # Set up Selenium with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    # Wait until the ingredients section is loaded
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "o-Ingredients__m-Body")))

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the ingredients section
    ingredients_section = soup.find('section', class_='o-Ingredients')

    if not ingredients_section:
        print("Could not find the ingredients section on this page.")
        driver.quit()
        return []

    # Extract the text from each list item within the section
    ingredients = []
    for item in ingredients_section.find_all('p', class_='o-Ingredients__a-Ingredient'):
        ingredient_text = ' '.join(item.stripped_strings)
        ingredients.append(ingredient_text)

    driver.quit()

    return ingredients


def getFromSeriousEats(url):
    # Set up Selenium
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait until the specific div with ingredients is loaded
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "structured-ingredients_1-0")))

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
