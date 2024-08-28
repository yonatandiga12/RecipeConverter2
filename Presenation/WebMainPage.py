from tkinter import *
from tkinter import filedialog
import numpy as np
#import cv2
from Business.Conversions import convertToGrams
from Business.convertToText import readPictureFromWeb
from Business.seleniumConvertToText import getIngredientsFromWebScraping

mask = np.ones((490, 500))

app = Tk()
app.title('Convert')
app.geometry('500x700')
title = Label(app, text='Recipe Converter', font=('Times', 24), fg='#068481')
title.pack()


def processURL(url):
    if url is None:
        return
    original, newIngredients = startFuncFromWebScraping(url)
    printList(newIngredients)


def printList(listToPrint):
    root = Tk()
    root.geometry("1024x640")
    root.title("Ingredients")

    txt_output = Text(root, height=1000, width=100)
    txt_output.config(font=('Helvatical bold', 20))
    txt_output.pack(pady=30)


    for item in listToPrint:
        txt_output.insert(END, item + "\n")
    root.mainloop()


def openAndPut():
    path = filedialog.askopenfilename()
    if path:
        original, newIngredients = startFuncFromImage(path)
        #printList(original)
        printList(newIngredients)



# image_area = Canvas(app, width=490, height=500, bg='#C8C8C8')
# image_area.pack(pady=(10, 0))

open_image = Button(app, width=20, text='OPEN IMAGE', font=('Helvatical bold', 20), command=openAndPut)
open_image.pack(pady=(10, 5))


# Input field for the URL
url_entry = Entry(app, width=50, font=('Helvetica', 16))
url_entry.pack(pady=(10, 5))

# Button to process the URL
process_button = Button(app, width=20, text='PROCESS LINK', font=('Helvetica bold', 20),
                        command=lambda: processURL(url_entry.get()))
process_button.pack(pady=(10, 5))

def startFuncFromWebScraping(url):
    result = list()
    ingredients = getIngredientsFromWebScraping(url)
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        result.append(curr)

    return ingredients, result


def startFuncFromImage(path):
    result = list()
    #img = cv2.imread(path)
    #ingredients = readPictureFromWeb(img)  #reading the photo
    ingredients = None
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        result.append(curr)

    return ingredients, result






if __name__ == '__main__':
    app.mainloop()
