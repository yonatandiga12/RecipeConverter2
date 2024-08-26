import pytesseract
import cv2



picturesPath = 'pictures\\'
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\יונתן\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'


def readPicture(nameOfPicture):

    img = cv2.imread(picturesPath + nameOfPicture)

    text = pytesseract.image_to_string(img)
    splitted = text.split('\n')
    removeSpace = [x for x in splitted if x != ""]

    result = removeSpace
    return result


def readPictureFromWeb(img):

    text = pytesseract.image_to_string(img)
    splitted = text.split('\n')
    removeSpace = [x for x in splitted if x != ""]

    result = removeSpace
    return result

