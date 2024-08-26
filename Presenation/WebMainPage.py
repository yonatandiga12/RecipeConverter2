from tkinter import *
from tkinter import filedialog
import numpy as np
import cv2
from Business.Conversions import convertToGrams
from Business.convertToText import readPictureFromWeb
from Business.seleniumConvertToText import getIngredientsFromWebScraping

mask = np.ones((490, 500))

app = Tk()
app.title('Convert')
app.geometry('500x700')
title = Label(app, text='Recipe Converter', font=('Times', 24), fg='#068481')
title.pack()


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
        original, newIngredients = startFuncForWeb(path)
        #printList(original)
        printList(newIngredients)



image_area = Canvas(app, width=490, height=500, bg='#C8C8C8')
image_area.pack(pady=(10, 0))

open_image = Button(app, width=20, text='OPEN IMAGE', font=('Helvatical bold', 20), command=openAndPut)
open_image.pack(pady=(10, 5))




def startFuncForWeb(path):
    result = list()
    img = cv2.imread(path)
    #ingredients = readPictureFromWeb(img)  #reading the photo
    link = "https://www.seriouseats.com/bravetarts-devils-food-cake"
    ingredients = getIngredientsFromWebScraping(link)
    for sentence in ingredients:
        curr = convertToGrams(sentence)
        result.append(curr)

    return ingredients, result






if __name__ == '__main__':
    app.mainloop()
