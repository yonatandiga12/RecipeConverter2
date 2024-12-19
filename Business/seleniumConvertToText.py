from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SUPPORTED_SITES=["seriouseats", "foodnetwork", "loveandlemons", "preppykitchen"]


# works with https://www.seriouseats.com
def findSiteName(url):
    try:
        splitedOnce = url.split("//")
        url = splitedOnce[1]
        splitedUrl = url.split('.')
        if 'www' not in splitedUrl[0]:
            return splitedUrl[0]
        return splitedUrl[1]
    except:
        return ""


def getIngredientsFromWebScraping(url):
    siteName = findSiteName(url)
    if siteName == "seriouseats":
        return getFromSeriousEats(url)
    elif siteName == "foodnetwork":
        return getFromFoodNetwork(url)
    elif siteName == "loveandlemons":
        return getFromLoveAndLemons(url)
    elif siteName == "preppykitchen":
        return getFromPreppyKitchen(url)
    else:
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
        driver.quit()
        return "Could not find the ingredients section on this page."

    # Extract the text from each list item within the section
    ingredients = []
    for item in ingredients_section.find_all('p', class_='o-Ingredients__a-Ingredient'):
        ingredient_text = ' '.join(item.stripped_strings)
        ingredients.append(ingredient_text)


    # Directions
    # Locate the section containing the directions
    method_section = soup.find('section', class_='o-Method')

    # Extract the list items representing the steps
    directions = []
    if method_section:
        steps = method_section.find_all('li', class_='o-Method__m-Step')
        for step in steps:
            directions.append(step.get_text(strip=True))

    # Print the extracted directions
    for i, direction in enumerate(directions, 1):
        print(f"Step {i}: {direction}")




    driver.quit()

    return ingredients


def getFromSeriousEats(url):
    # Set up Selenium with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait until the specific div with ingredients is loaded
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "structured-ingredients_1-0")))

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the div with the specific ID
    ingredients_div = soup.find('div', id='structured-ingredients_1-0')

    if not ingredients_div:
        driver.quit()
        return "Could not find the ingredients section on this page."

    # Extract the text from each list item within the div
    ingredients = []
    for li in ingredients_div.find_all('li'):
        # Join text with spaces where necessary
        ingredient_text = ' '.join(li.stripped_strings)
        ingredients.append(ingredient_text)


    ## DIRECTIONS
    # Locate the section containing the directions
    instructions_section = soup.find('section', id='section--instructions_1-0')

    # Extract the ordered list within the section
    directions_list = instructions_section.find('ol', class_='comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--OL')

    # Extract each step in the list
    directions = []
    if directions_list:
        steps = directions_list.find_all('li')
        for step in steps:
            instruction = step.get_text(strip=True)
            junkIndex = instruction.find('Serious Eats / ')   #If there is a photo in the directions, it will be saved like this
            if junkIndex != -1:
                instruction_without_junk = instruction[:junkIndex]
                directions.append(instruction_without_junk)
            else:
                directions.append(instruction)

    # Print the extracted directions
    for i, direction in enumerate(directions, 1):
        print(f"Step {i}: {direction}\n")


    driver.quit()

    return ingredients


def getFromLoveAndLemons(url):
    # Set up Selenium with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the ingredients section using its unique identifiers
        ingredients_section = soup.find('div', class_='wprm-recipe-ingredient-group')

        if not ingredients_section:
            return "Could not find the ingredients section on this page."

        # Extract the text from each list item within the section
        ingredients = []
        for item in ingredients_section.find_all(['li', 'p']):
            ingredient_text = ' '.join(item.stripped_strings)
            ingredients.append(ingredient_text)

    except Exception as e:
        return f"Error extracting ingredients: {str(e)}"

    finally:
        driver.quit()

    return ingredients


#wprm-recipe-ingredient-group


def getFromPreppyKitchen(url):
    # Set up Selenium with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the ingredients section using its unique identifiers
        ingredients_section = soup.find('div', class_='wprm-recipe-ingredients-container')

        if not ingredients_section:
            return "Could not find the ingredients section on this page."

        # Extract the text from each list item within the section
        ingredients = []
        for item in ingredients_section.find_all('li', class_='wprm-recipe-ingredient'):
            ingredient_text = ' '.join(item.stripped_strings)
            ingredients.append(ingredient_text)

    except Exception as e:
        return f"Error extracting ingredients: {str(e)}"

    finally:
        driver.quit()

    return ingredients

