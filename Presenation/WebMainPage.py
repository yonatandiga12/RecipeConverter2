from tkinter import *
from tkinter.ttk import Notebook, Frame as TtkFrame, Style

from tkinter import filedialog
import numpy as np
# import cv2
import matplotlib.image as mpimg
from Business.Conversions import convertToGrams
from Business.convertToText import readPictureFromWeb
from Business.seleniumConvertToText import getIngredientsFromWebScraping

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

# Set the tab width to fill half of the window
style.configure('TNotebook.Tab', width=500)  # Half of the 1000px window width

# Create Notebook for tabs
notebook = Notebook(app)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
url_tab = TtkFrame(notebook)
image_tab = TtkFrame(notebook)

# Add frames to the notebook as tabs
notebook.add(url_tab, text='URL Converter')
notebook.add(image_tab, text='Open Image')


# Tab 1: URL Converter
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


def add_text_frames(parent):
    """
    Function to add the shared section of text frames to the specified parent frame.
    Returns the references to txt_original and txt_converted for external access.
    """
    # Frame to hold both text windows side by side
    text_frame = Frame(parent)
    text_frame.pack(pady=20)

    # Title above the original ingredients
    original_title = Label(text_frame, text='Original Ingredients', font=('Helvetica bold', 16))
    original_title.grid(row=0, column=0, padx=10)

    # Title above the converted ingredients
    converted_title = Label(text_frame, text='Converted Ingredients', font=('Helvetica bold', 16))
    converted_title.grid(row=0, column=1, padx=10)

    # Text widget for original ingredients
    txt_original = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
    txt_original.grid(row=1, column=0, padx=10)

    # Text widget for converted ingredients
    txt_converted = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
    txt_converted.grid(row=1, column=1, padx=10)

    # Return the text widgets to be accessible from other functions
    return txt_original, txt_converted


# Add the shared section to the URL tab
txt_original_url, txt_converted_url = add_text_frames(url_tab)

# Add the shared section to the Image tab
txt_original_img, txt_converted_img = add_text_frames(image_tab)

# Common message label for both tabs at the bottom
msg_label = Label(app, text="", font=('Helvetica bold', 20))
msg_label.pack(pady=20, side=BOTTOM)


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
        printList(original, newIngredients, txt_original_url, txt_converted_url)


def printList(originalList, convertedList, txt_original, txt_converted):
    # Clear any previous content in the Text widgets
    txt_original.delete(1.0, END)
    txt_converted.delete(1.0, END)

    # Insert original ingredients into the first Text widget
    for item in originalList:
        txt_original.insert(END, item + "\n")

    # Insert converted ingredients into the second Text widget
    for item in convertedList:
        txt_converted.insert(END, item + "\n")


def openPictureAndConvert():
    path = filedialog.askopenfilename()
    if path:
        original, newIngredients = startFuncFromImage(path)
        printList(original, newIngredients, txt_original_img, txt_converted_img)


# Tab 2: Open Image
# Button to open an image and process it
open_image = Button(image_tab, width=20, text='Open Image', font=('Helvetica bold', 20),
                    command=openPictureAndConvert)
open_image.pack(pady=(10, 5))


# image_area = Canvas(app, width=490, height=500, bg='#C8C8C8')
# image_area.pack(pady=(10, 0))

# open_image = Button(app, width=20, text='Open Image', font=('Helvatical bold', 20), command=openAndPut)
# open_image.pack(pady=(10, 5))


# Button to open image and process ingredients
# open_image = Button(app, width=20, text='OPEN IMAGE', font=('Helvetica bold', 20), command=openAndPut)
# open_image.pack(pady=(10, 5))


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
    # img = cv2.imread(path)

    img = mpimg.imread(path)
    ingredients = readPictureFromWeb(img)  # reading the photo
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        converted.append(curr)

    return ingredients, converted


if __name__ == '__main__':
    app.mainloop()
