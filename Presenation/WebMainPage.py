from tkinter import *
from tkinter.ttk import Notebook, Frame as TtkFrame, Style
from tkinter import filedialog
import numpy as np
import matplotlib.image as mpimg
from Business.Conversions import convertToGrams
from Business.RecipeObject import RecipeObject
from Business.convertToText import readPictureFromWeb
from Business.seleniumConvertToText import getIngredientsFromWebScraping
from Business.GoogleSearch import search_dessert_google  # Import logic for dessert search

mask = np.ones((490, 500))

# Main application window
app = Tk()
app.title('Recipe Converter')
app.geometry('1000x850')

# Create a style for the tabs
style = Style()
style.theme_use('default')

# Customizing the notebook tabs to fill the width of the window
style.configure('TNotebook', tabmargins=[0, 0, 0, 0])
style.configure('TNotebook.Tab', font=('Helvetica', 16), padding=[10, 10])

# Set the tab width to fill one-third of the window
style.configure('TNotebook.Tab', width=333)  # One-third of the 1000px window width

# Create Notebook for tabs
notebook = Notebook(app)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
url_tab = TtkFrame(notebook)
image_tab = TtkFrame(notebook)
search_tab = TtkFrame(notebook)  # New search tab

# Add frames to the notebook as tabs
notebook.add(url_tab, text='URL Converter')
notebook.add(image_tab, text='Open Image')
notebook.add(search_tab, text='Search')  # Add Search tab


# ================= URL Converter Tab =================
# Title Label
title = Label(url_tab, text='Recipe Converter', font=('Helvetica bold', 36), fg='black')
title.pack(pady=10)

# Input field for the URL
url_entry = Entry(url_tab, width=50, font=('Helvetica', 16))
url_entry.pack(pady=(10, 5))

# Button to process the URL
process_button = Button(url_tab, width=20, text='Convert', font=('Helvetica bold', 16),
                        command=lambda: processURL(url_entry.get()))
process_button.pack(pady=(10, 5))


# Function to add text frames to a tab
def add_text_frames(parent):
    text_frame = Frame(parent, width=900)
    text_frame.pack(pady=20, expand=True, fill='both')

    # Title above the original ingredients
    original_title = Label(text_frame, text='Original Ingredients', font=('Helvetica bold', 16))
    original_title.grid(row=0, column=0, padx=10)

    # Title above the converted ingredients
    converted_title = Label(text_frame, text='Converted Ingredients', font=('Helvetica bold', 16))
    converted_title.grid(row=0, column=1, padx=10)

    # Text widgets for ingredients
    txt_original = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
    txt_original.grid(row=1, column=0, padx=10)

    txt_converted = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
    txt_converted.grid(row=1, column=1, padx=10)

    return txt_original, txt_converted


# Add the shared text area to the URL tab
txt_original_url, txt_converted_url = add_text_frames(url_tab)




# ================= Image Converter Tab =================
# Button to open an image and process it
open_image = Button(image_tab, width=20, text='Open Image', font=('Helvetica bold', 20),
                    command=lambda: openPictureAndConvert())
open_image.pack(pady=(10, 5))

# Add shared text area to the Image tab
txt_original_img, txt_converted_img = add_text_frames(image_tab)




# ================= Search Tab =================
# Title for search functionality
search_label = Label(search_tab, text="Search Dessert Recipes", font=('Helvetica bold', 24))
search_label.pack(pady=10)

# Frame for search input and button
search_frame = Frame(search_tab)
search_frame.pack(pady=(10, 5))

# Input field for search
search_entry = Entry(search_frame, width=50, font=('Helvetica', 16))
search_entry.grid(row=0, column=0, padx=(10, 5))

# Button to perform search
def perform_search():
    dessert_name = search_entry.get()
    if not dessert_name.strip():
        sendError("Please enter a dessert name!")
        return

    sendSuccess("Searching for recipes...")
    results = search_dessert_google(dessert_name)  # Call the external logic
    results.sort(key=lambda x: x.reviews_count, reverse=True)
    if results:
        search_results_txt.delete(1.0, END)
        search_results_txt.insert(END, "\n".join([item.__str__() for item in results]))
        sendSuccess("Search completed!")
    else:
        sendError("No results found or an error occurred.")


search_button = Button(search_frame, text='Search', font=('Helvetica bold', 14), command=perform_search)
search_button.grid(row=0, column=1, padx=(5, 10))

# Text widget for displaying search results
search_results_txt = Text(search_tab, height=20, width=90, font=('Helvetica', 12))
search_results_txt.pack(pady=(10, 5))

# ================= Error/Success Messages =================
msg_label = Label(app, text="", font=('Helvetica bold', 16))
msg_label.pack(pady=10, side=BOTTOM)




# ================= Functions =================
def sendError(msg):
    msg_label.config(text=msg, fg='red')

def sendSuccess(msg):
    msg_label.config(text=msg, fg='green')

def processURL(url):
    if url is None:
        return
    original, newIngredients = startFuncFromWebScraping(url)
    if original is None:
        if newIngredients is None:
            sendError("Site is not configured in the system!")
        elif type(newIngredients) is str:
            sendError(newIngredients)
    else:
        sendSuccess("Recipe converted!")
        recipeObj = RecipeObject("", "", url)
        recipeObj.setConvertedIngredients(newIngredients)
        recipeObj.setOriginalIngredients(original)
        recipeObj.setInstructions([])
        printWithInstructions(recipeObj, txt_original_url, txt_converted_url)
        #printList(original, newIngredients, txt_original_url, txt_converted_url)


def printWithInstructions(recipeObject, txt_original, txt_converted):
    txt_original.delete(1.0, END)
    txt_converted.delete(1.0, END)
    for item in recipeObject.getOriginalIngredients():
        txt_original.insert(END, "• " + item + "\n")
    for item in recipeObject.getConvertedIngredients():
        txt_converted.insert(END, "• " + item + "\n")
    for item in recipeObject.getInstructions():
        #txt_instructions.insert(END, "• " + item + "\n")
        pass

def printList(originalList, convertedList, txt_original, txt_converted):
    txt_original.delete(1.0, END)
    txt_converted.delete(1.0, END)
    for item in originalList:
        txt_original.insert(END, "• " + item + "\n")
    for item in convertedList:
        txt_converted.insert(END, "• " + item + "\n")

def openPictureAndConvert():
    path = filedialog.askopenfilename()
    if path:
        original, newIngredients = startFuncFromImage(path)

        printList(original, newIngredients, txt_original_img, txt_converted_img)

def startFuncFromWebScraping(url):
    result = list()
    ingredients = getIngredientsFromWebScraping(url)
    if ingredients is None:
        return None, None
    if type(ingredients) is str:
        return None, ingredients
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        result.append(curr)
    return ingredients, result

def startFuncFromImage(path):
    converted = list()
    img = mpimg.imread(path)
    ingredients = readPictureFromWeb(img)
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        converted.append(curr)
    return ingredients, converted

# Run the app
if __name__ == '__main__':
    app.mainloop()








# from tkinter import *
# from tkinter.ttk import Notebook, Frame as TtkFrame, Style
#
# from tkinter import filedialog
# import numpy as np
# import matplotlib.image as mpimg
# from Business.Conversions import convertToGrams
# from Business.convertToText import readPictureFromWeb
# from Business.seleniumConvertToText import getIngredientsFromWebScraping
#
# mask = np.ones((490, 500))
#
# # Main application window
# app = Tk()
# app.title('Recipe Converter')
# app.geometry('1000x850')
#
#
# # Create a style for the tabs
# style = Style()
# style.theme_use('default')
#
# # Customizing the notebook tabs to fill the width of the window
# style.configure('TNotebook', tabmargins=[0, 0, 0, 0])
# style.configure('TNotebook.Tab', font=('Helvetica', 16), padding=[10, 10])
#
# # Set the tab width to fill half of the window
# style.configure('TNotebook.Tab', width=500)  # Half of the 1000px window width
#
# # Create Notebook for tabs
# notebook = Notebook(app)
# notebook.pack(expand=True, fill='both')
#
# # Create frames for each tab
# url_tab = TtkFrame(notebook)
# image_tab = TtkFrame(notebook)
#
# # Add frames to the notebook as tabs
# notebook.add(url_tab, text='URL Converter')
# notebook.add(image_tab, text='Open Image')
#
#
# # Tab 1: URL Converter
# # Title Label
# title = Label(url_tab, text='Recipe Converter', font=('Helvetica bold', 36), fg='black')
# title.pack(pady=10)
#
# # Input field for the URL
# url_entry = Entry(url_tab, width=50, font=('Helvetica', 16))
# url_entry.pack(pady=(10, 5))
#
# # Button to process the URL
# process_button = Button(url_tab, width=20, text='Convert', font=('Helvetica bold', 16),
#                         command=lambda: processURL(url_entry.get()))
# process_button.pack(pady=(10, 5))
#
#
# # Add a label for Supported Sites at the bottom
# supported_sites_label = Label(
#     app,
#     text="Supported Sites: Serious Eats, Food Network, Preppy Kitchen, Love and Lemons",
#     font=('Helvetica', 12),
#     fg='gray'
# )
# supported_sites_label.pack(side=BOTTOM, pady=5)  # Minimal vertical padding
#
# def add_text_frames(parent):
#     """
#     Function to add the shared section of text frames to the specified parent frame.
#     Returns the references to txt_original and txt_converted for external access.
#     """
#     # Frame to hold both text windows side by side
#     text_frame = Frame(parent, width=900)
#     text_frame.pack(pady=20, expand=True, fill='both')  # Expands and fills the available space
#
#     # Title above the original ingredients
#     original_title = Label(text_frame, text='Original Ingredients', font=('Helvetica bold', 16))
#     original_title.grid(row=0, column=0, padx=10)
#
#     # Title above the converted ingredients
#     converted_title = Label(text_frame, text='Converted Ingredients', font=('Helvetica bold', 16))
#     converted_title.grid(row=0, column=1, padx=10)
#
#     # Text widget for original ingredients
#     txt_original = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
#     txt_original.grid(row=1, column=0, padx=10)
#
#     # Text widget for converted ingredients
#     txt_converted = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
#     txt_converted.grid(row=1, column=1, padx=10)
#
#     # Return the text widgets to be accessible from other functions
#     return txt_original, txt_converted
#
#
# # Add the shared section to the URL tab
# txt_original_url, txt_converted_url = add_text_frames(url_tab)
#
# # Add the shared section to the Image tab
# txt_original_img, txt_converted_img = add_text_frames(image_tab)
#
# # Common message label for both tabs at the bottom
# msg_label = Label(app, text="", font=('Helvetica bold', 20))
# msg_label.pack(pady=20, side=BOTTOM)
#
#
# def sendError(msg):
#     msg_label.config(text=msg, fg='red')
#
#
# def sendSuccess(msg):
#     msg_label.config(text=msg, fg='green')
#
#
# def processURL(url):
#     if url is None:
#         return
#     original, newIngredients = startFuncFromWebScraping(url)
#     if original is None:
#         if newIngredients is None:
#             sendError("Site is not configured in the system!")
#         elif type(newIngredients) is str:
#             sendError(newIngredients)
#     else:
#         sendSuccess("Recipe converted!")
#         printList(original, newIngredients, txt_original_url, txt_converted_url)
#
#
# def printList(originalList, convertedList, txt_original, txt_converted):
#     # Clear any previous content in the Text widgets
#     txt_original.delete(1.0, END)
#     txt_converted.delete(1.0, END)
#
#     # Insert original ingredients into the first Text widget
#     for item in originalList:
#         txt_original.insert(END, "• " + item + "\n")
#
#     # Insert converted ingredients into the second Text widget
#     for item in convertedList:
#         txt_converted.insert(END, "• " + item + "\n")
#
#
# def openPictureAndConvert():
#     path = filedialog.askopenfilename()
#     if path:
#         original, newIngredients = startFuncFromImage(path)
#         printList(original, newIngredients, txt_original_img, txt_converted_img)
#
#
# # Tab 2: Open Image
# # Button to open an image and process it
# open_image = Button(image_tab, width=20, text='Open Image', font=('Helvetica bold', 20),
#                     command=openPictureAndConvert)
# open_image.pack(pady=(10, 5))
#
#
# # image_area = Canvas(app, width=490, height=500, bg='#C8C8C8')
# # image_area.pack(pady=(10, 0))
#
# # open_image = Button(app, width=20, text='Open Image', font=('Helvatical bold', 20), command=openAndPut)
# # open_image.pack(pady=(10, 5))
#
#
# # Button to open image and process ingredients
# # open_image = Button(app, width=20, text='OPEN IMAGE', font=('Helvetica bold', 20), command=openAndPut)
# # open_image.pack(pady=(10, 5))
#
#
# def startFuncFromWebScraping(url):
#     result = list()
#     ingredients = getIngredientsFromWebScraping(url)
#     if ingredients is None:
#         return None, None
#     if type(ingredients) is str:
#         return None, ingredients
#
#     for sentence in ingredients:
#         curr = convertToGrams(sentence)
#         result.append(curr)
#
#     return ingredients, result
#
#
# def startFuncFromImage(path):
#     converted = list()
#     # img = cv2.imread(path)
#
#     img = mpimg.imread(path)
#     ingredients = readPictureFromWeb(img)  # reading the photo
#     for sentence in ingredients:
#         curr = convertToGrams(sentence)
#         converted.append(curr)
#
#     return ingredients, converted
#
#
# if __name__ == '__main__':
#     app.mainloop()
