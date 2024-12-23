from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

SUPPORTED_SITES = ["seriouseats", "foodnetwork", "loveandlemons", "preppykitchen",
                   "kingarthurbaking", "sallysbakingaddiction"]


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
    elif siteName == "kingarthurbaking":
        return getFromKingArthurBaking(url)
    elif siteName == "sallysbakingaddiction":
        return getFromSallysBakingAddiction(url)
    elif siteName == "bbcgoodfood":
        return getFromGoodFood(url)
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

    # INSTRUCTIONS
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

    return {
        "ingredients": ingredients,
        "instructions": directions
    }


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

    # INSTRUCTIONS
    # Locate the section containing the directions
    instructions_section = soup.find('section', id='section--instructions_1-0')

    # Extract the ordered list within the section
    directions_list = instructions_section.find('ol',
                                        class_='comp mntl-sc-block mntl-sc-block-startgroup mntl-sc-block-group--OL')

    # Extract each step in the list
    directions = []
    if directions_list:
        steps = directions_list.find_all('li')
        for step in steps:
            instruction = step.get_text(strip=True)
            junkIndex = instruction.find(
                'Serious Eats / ')  # If there is a photo in the directions, it will be saved like this
            if junkIndex != -1:
                instruction_without_junk = instruction[:junkIndex]
                directions.append(instruction_without_junk)
            else:
                directions.append(instruction)

    # Print the extracted directions
    for i, direction in enumerate(directions, 1):
        print(f"Step {i}: {direction}\n")

    driver.quit()

    return {
        "ingredients": ingredients,
        "instructions": directions
    }


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

        # INSTRUCTIONS

        # Search for instruction steps by matching IDs with the specific prefix
        instruction_steps = soup.find_all('li', id=lambda x: x and x.startswith('wprm-recipe-42187-step'))

        # Extract the text content for each step
        directions = []
        for step in instruction_steps:
            text_div = step.find('div', class_='wprm-recipe-instruction-text')
            if text_div:
                directions.append(text_div.get_text(strip=True))

        # Print the extracted directions
        for i, direction in enumerate(directions, 1):
            print(f"Step {i}: {direction}")


    except Exception as e:
        return f"Error extracting ingredients: {str(e)}"

    finally:
        driver.quit()

    return {
        "ingredients": ingredients,
        "instructions": directions
    }


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

        # INSTRUCTIONS

        # Locate the instructions container
        instruction_groups = soup.find_all('div', class_='wprm-recipe-instruction-group')

        # Extract the instructions
        directions = []
        for group in instruction_groups:
            # Extract group header (if any, e.g., "For the Brownie Base")
            group_name = group.find('h4', class_='wprm-recipe-group-name')
            if group_name:
                directions.append(group_name.get_text(strip=True))

            # Extract each step in the group
            steps = group.find_all('li', id=lambda x: x and x.startswith('wprm-recipe'))
            for step in steps:
                text_div = step.find('div', class_='wprm-recipe-instruction-text')
                if text_div:
                    directions.append(text_div.get_text(strip=True))

        # Print the extracted directions
        for i, direction in enumerate(directions, 1):
            print(f"Step {i}: {direction}")


    except Exception as e:
        return f"Error extracting ingredients: {str(e)}"

    finally:
        driver.quit()

    return {
        "ingredients": ingredients,
        "instructions": directions
    }


def getFromKingArthurBaking(url):
    # Set up Selenium with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # INGREDIENTS
        # Find the ingredients section using its unique identifiers
        ingredients_section = soup.find('div', class_='ingredient-section')

        if not ingredients_section:
            return "Could not find the ingredients section on this page."

        # Extract the text from each list item within the section
        ingredients = []
        for item in ingredients_section.find_all('li'):
            ingredient_text = ' '.join(item.stripped_strings)
            ingredients.append(ingredient_text)

        # INSTRUCTIONS
        # Locate the instructions container
        instructions_section = soup.find('div', class_='field field--recipe-steps')

        if not instructions_section:
            return "Could not find the instructions section on this page."

        # Extract the text from each list item within the section
        instructions = []
        for item in instructions_section.find_all('li', class_='field__item'):
            step_paragraph = item.find('p')
            if step_paragraph:
                instructions.append(step_paragraph.get_text(strip=True))


    except Exception as e:
        return f"Error extracting ingredients or instructions: {str(e)}"

    finally:
        driver.quit()

    # Return the extracted ingredients and instructions
    return {
        "ingredients": ingredients,
        "instructions": instructions
    }


def getFromSallysBakingAddiction(url):
    # Set up Selenium with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # INGREDIENTS
        # Locate the ingredients section
        ingredients_section = soup.find('div', class_='tasty-recipes-ingredients-body')

        if not ingredients_section:
            return "Could not find the ingredients section on this page."

        # Extract ingredient groups and items
        ingredients = []
        for section in ingredients_section.find_all('ul'):
            # Find the header for the group (if it exists)
            header = section.find_previous('h4')
            if header:
                ingredients.append(header.get_text(strip=True))  # Add the header

            # Extract each ingredient within the group
            # for item in section.find_all('li', class_='data-tr-ingredient-checkbox'):
            #     ingredient_text = ' '.join(item.stripped_strings)
            #     ingredients.append(ingredient_text)
            for item in section.find_all('li'):
                ingredient_text = ' '.join(item.stripped_strings)
                if ingredient_text:  # Ensure it's not empty
                    ingredients.append(ingredient_text)

            ingredients.append('\n')

        # INSTRUCTIONS
        # Locate the instructions container
        instructions_section = soup.find('div', class_='tasty-recipes-instructions-body')

        if not instructions_section:
            return "Could not find the instructions section on this page."

        # Extract each instruction step
        instructions = []
        for step in instructions_section.find_all('li', id=lambda x: x and x.startswith('instruction-step')):
            step_text = ' '.join(step.stripped_strings)
            instructions.append(step_text)


    except Exception as e:
        return f"Error extracting data: {str(e)}"

    finally:
        driver.quit()

    # Return the extracted ingredients and instructions
    return {
        "ingredients": ingredients,
        "instructions": instructions
    }


def getFromGoodFood(url):
    # Set up Selenium with headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    all_ingredients = []
    instructions = []
    try:
        driver.get(url)

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate the parent container of all ingredient sections
        parent_container = soup.find('section', id='ingredients-list')

        if not parent_container:
            print("Could not find the parent container for ingredients.")
        else:
            # Locate all nested sections within the parent container
            ingredient_sections = parent_container.find_all('section')

            if not ingredient_sections:
                print("Could not find any ingredients sections.")
            else:
                all_ingredients = []

                # Loop through each nested section
                for section in ingredient_sections:
                    # Get the heading text (e.g., "For the cake")
                    heading = section.find('h3', class_='ingredients-list__heading')
                    heading_text = heading.get_text(strip=True) if heading else "No heading"
                    if heading_text is not "No heading":
                        all_ingredients.append(heading_text)

                    # Locate the <ul> inside the section
                    ingredients_list = section.find('ul', class_='ingredients-list')

                    # Extract all <li> elements under the ingredients list
                    if ingredients_list:
                        ingredient_items = ingredients_list.find_all('li')
                        ingredients = [item.get_text(separator=' ', strip=True) for item in ingredient_items]
                    else:
                        ingredients = []

                    # Save the ingredients under the heading
                    all_ingredients += ingredients
                    all_ingredients += '\n'

        # INSTRUCTIONS
        # Locate the instructions container
        directions_section = soup.find('section', class_='method-steps')

        if not directions_section:
            print("Could not find the directions section on this page.")
        else:
            # Extract each step
            instructions = []
            for step in directions_section.find_all('li', class_='method-steps__list-item'):
                paragraph = step.find('p')  # Locate the <p> tag
                if paragraph:
                    instructions.append(paragraph.get_text(strip=True))  # Get text content


    except Exception as e:
        return f"Error extracting data: {str(e)}"

    finally:
        driver.quit()

    # Return the extracted ingredients and instructions
    return {
        "ingredients": all_ingredients,
        "instructions": instructions
    }
