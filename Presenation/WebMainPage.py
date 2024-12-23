#
# ################################################################################################################
#
#
#
# from tkinter import *
# from tkinter.ttk import Notebook, Frame as TtkFrame, Style
# from tkinter import filedialog
# import numpy as np
# import matplotlib.image as mpimg
# from Business.Conversions import convertToGrams
# from Business.RecipeObject import RecipeObject
# from Business.convertToText import readPictureFromWeb
# from Business.seleniumConvertToText import getIngredientsFromWebScraping
# from Business.GoogleSearch import search_dessert_google
#
# mask = np.ones((490, 500))
#
# # Main application window
# app = Tk()
# app.title('Recipe Converter')
# app.state('zoomed')  # Open in full-screen mode
# app.configure(bg="#d3eaf7")  # Light blue-gray background
#
# # Create a style for the tabs
# style = Style()
# style.theme_use('default')
#
# # Customize the notebook tabs to appear on the left
# style.configure('TNotebook', tabposition='wn', background="#d3eaf7")
# style.configure('TNotebook.Tab', font=('Helvetica', 16), padding=[10, 10], anchor="w")  # Align text to the left
#
# # Create Notebook for tabs
# notebook = Notebook(app)
# notebook.pack(expand=True, fill='both', padx=10, pady=10)
#
# # Create frames for each tab
# url_tab = TtkFrame(notebook)
# image_tab = TtkFrame(notebook)
# search_tab = TtkFrame(notebook)  # New search tab
#
# # Add frames to the notebook as tabs
# notebook.add(url_tab, text='URL Converter')
# notebook.add(search_tab, text='Search')
# notebook.add(image_tab, text='Open Image')
#
# # ================= URL Converter Tab =================
# # Title Label
# title = Label(url_tab, text='Recipe Converter', font=('Helvetica bold', 36), bg="#d3eaf7")
# title.pack(pady=10)
#
# # Input field for the URL
# url_entry = Entry(url_tab, width=50, font=('Helvetica', 16))
# url_entry.pack(pady=(10, 5))
#
# # Button to process the URL
# process_button = Button(url_tab, width=20, text='Convert', font=('Helvetica bold', 16),
#                         command=lambda: processURL(url_entry.get()), bg="#6aa7cf", fg="white")
# process_button.pack(pady=(10, 5))
#
# # Function to add text frames to a tab
# def add_text_frames(parent):
#     text_frame = Frame(parent, bg="#d3eaf7")
#     text_frame.pack(pady=20, expand=True, fill='both')
#
#     # Title above the original ingredients
#     original_title = Label(text_frame, text='Original Ingredients', font=('Helvetica bold', 16), bg="#d3eaf7")
#     original_title.grid(row=0, column=0, padx=10)
#
#     # Title above the converted ingredients
#     converted_title = Label(text_frame, text='Converted Ingredients', font=('Helvetica bold', 16), bg="#d3eaf7")
#     converted_title.grid(row=0, column=1, padx=10)
#
#     # Text widgets for ingredients
#     txt_original = Text(text_frame, height=20, width=50, font=('Helvetica', 14), bg="white")
#     txt_original.grid(row=1, column=0, padx=10)
#
#     txt_converted = Text(text_frame, height=20, width=50, font=('Helvetica', 14), bg="white")
#     txt_converted.grid(row=1, column=1, padx=10)
#
#     return txt_original, txt_converted
#
# # Add the shared text area to the URL tab
# txt_original_url, txt_converted_url = add_text_frames(url_tab)
#
# # Add an instructions frame below
# instructions_frame = LabelFrame(url_tab, text="Instructions", font=('Helvetica bold', 16), bg="#e9f3fa")
# instructions_frame.pack(fill="x", pady=10)
#
# instructions_label = Label(
#     instructions_frame,
#     text="1. Enter the recipe URL and click 'Convert' to extract ingredients.\n"
#          "2. View the original and converted ingredients side by side.\n"
#          "3. Use the 'Search' or 'Open Image' tabs for more features.",
#     font=('Helvetica', 12), bg="#e9f3fa", justify="left"
# )
# instructions_label.pack(padx=10, pady=10)
#
# # ================= Image Converter Tab =================
# open_image = Button(image_tab, width=20, text='Open Image', font=('Helvetica bold', 20),
#                     command=lambda: openPictureAndConvert(), bg="#6aa7cf", fg="white")
# open_image.pack(pady=(10, 5))
#
# # Add shared text area to the Image tab
# txt_original_img, txt_converted_img = add_text_frames(image_tab)
#
#
#
# # ================= Search Tab =================
#
# # Button to perform search
# def perform_search():
#     dessert_name = search_entry.get()
#     if not dessert_name.strip():
#         sendError("Please enter a dessert name!")
#         return
#
#     sendSuccess("Searching for recipes...")
#     results = search_dessert_google(dessert_name)  # Call the external logic
#     results.sort(key=lambda x: x.reviews_count, reverse=True)
#     if results:
#         search_results_txt.delete(1.0, END)
#         search_results_txt.insert(END, "\n".join([item.__str__() for item in results]))
#         sendSuccess("Search completed!")
#     else:
#         sendError("No results found or an error occurred.")
#
# # Adjust text widget dimensions based on the screen size
# screen_width = app.winfo_screenwidth()
# screen_height = app.winfo_screenheight()
#
# # Width and height for the text widget
# text_width = int(screen_width * 0.8 / 10)  # Approximate characters per row
# text_height = int(screen_height * 0.6 / 20)  # Approximate lines per widget
#
# search_label = Label(search_tab, text="Search Dessert Recipes", font=('Helvetica bold', 24), bg="#d3eaf7")
# search_label.pack(pady=10)
#
# search_frame = Frame(search_tab, bg="#d3eaf7")
# search_frame.pack(pady=(10, 5))
#
# search_entry = Entry(search_frame, width=50, font=('Helvetica', 16))
# search_entry.grid(row=0, column=0, padx=(10, 5))
#
# search_button = Button(search_frame, text='Search', font=('Helvetica bold', 14), command=perform_search,
#                        bg="#6aa7cf", fg="white")
# search_button.grid(row=0, column=1, padx=(5, 10))
#
# # Dynamically adjusted text widget for search results
# search_results_txt = Text(search_tab, height=text_height, width=text_width, font=('Helvetica', 12), bg="white")
# search_results_txt.pack(pady=(10, 5), expand=True, fill='both')
#
#
# # ================= Error/Success Messages =================
# msg_label = Label(app, text="", font=('Helvetica bold', 16), bg="#d3eaf7")
# msg_label.pack(pady=10, side=BOTTOM)
#
#
#
# # ================= Functions =================
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
#         recipeObj = RecipeObject("", "", url)
#         recipeObj.setConvertedIngredients(newIngredients)
#         recipeObj.setOriginalIngredients(original)
#         recipeObj.setInstructions([])
#         printWithInstructions(recipeObj, txt_original_url, txt_converted_url)
#         # printList(original, newIngredients, txt_original_url, txt_converted_url)

#
# def printWithInstructions(recipeObject, txt_original, txt_converted):
#     txt_original.delete(1.0, END)
#     txt_converted.delete(1.0, END)
#     for item in recipeObject.getOriginalIngredients():
#         txt_original.insert(END, "• " + item + "\n")
#     for item in recipeObject.getConvertedIngredients():
#         txt_converted.insert(END, "• " + item + "\n")
#     for item in recipeObject.getInstructions():
#         # txt_instructions.insert(END, "• " + item + "\n")
#         pass
#
#
# def printList(originalList, convertedList, txt_original, txt_converted):
#     txt_original.delete(1.0, END)
#     txt_converted.delete(1.0, END)
#     for item in originalList:
#         txt_original.insert(END, "• " + item + "\n")
#     for item in convertedList:
#         txt_converted.insert(END, "• " + item + "\n")
#
#
# def openPictureAndConvert():
#     path = filedialog.askopenfilename()
#     if path:
#         original, newIngredients = startFuncFromImage(path)
#
#         printList(original, newIngredients, txt_original_img, txt_converted_img)
#
#
# def startFuncFromWebScraping(url):
#     result = list()
#     ingredientsAndDirections = getIngredientsFromWebScraping(url)
#     if ingredientsAndDirections is None:
#         return None, None
#     if type(ingredientsAndDirections) is str:
#         sendError(ingredientsAndDirections)
#         return None, None
#     ingredients = ingredientsAndDirections["ingredients"]
#     instructions = ingredientsAndDirections["instructions"]
#     if type(ingredients) is str:
#         return None, ingredients
#     for sentence in ingredients:
#         curr = convertToGrams(sentence)
#         result.append(curr)
#     return ingredients, result
#
#
# def startFuncFromImage(path):
#     converted = list()
#     img = mpimg.imread(path)
#     ingredients = readPictureFromWeb(img)
#     for sentence in ingredients:
#         curr = convertToGrams(sentence)
#         converted.append(curr)
#     return ingredients, converted

#
# # Run the app
# if __name__ == '__main__':
#     app.mainloop()
#

###################################################################################################################


# from tkinter import *
# from tkinter.ttk import Notebook, Frame as TtkFrame, Style
# from tkinter import filedialog
# import numpy as np
# import matplotlib.image as mpimg
# from Business.Conversions import convertToGrams
# from Business.RecipeObject import RecipeObject
# from Business.convertToText import readPictureFromWeb
# from Business.seleniumConvertToText import getIngredientsFromWebScraping
# from Business.GoogleSearch import search_dessert_google  # Import logic for dessert search
#
# mask = np.ones((490, 500))
#
# # Main application window
# app = Tk()
# app.title('Recipe Converter')
# app.geometry('1000x850')
#
# # Create a style for the tabs
# style = Style()
# style.theme_use('default')
#
# # Customizing the notebook tabs to fill the width of the window
# style.configure('TNotebook', tabmargins=[0, 0, 0, 0])
# style.configure('TNotebook.Tab', font=('Helvetica', 16), padding=[10, 10])
#
# # Set the tab width to fill one-third of the window
# style.configure('TNotebook.Tab', width=333)  # One-third of the 1000px window width
#
# # Create Notebook for tabs
# notebook = Notebook(app)
# notebook.pack(expand=True, fill='both')
#
# # Create frames for each tab
# url_tab = TtkFrame(notebook)
# image_tab = TtkFrame(notebook)
# search_tab = TtkFrame(notebook)  # New search tab
#
# # Add frames to the notebook as tabs
# notebook.add(url_tab, text='URL Converter')
# notebook.add(search_tab, text='Search')  # Add Search tab
# notebook.add(image_tab, text='Open Image')
#
#
# # ================= URL Converter Tab =================
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
# # Function to add text frames to a tab
# def add_text_frames(parent):
#     text_frame = Frame(parent, width=900)
#     text_frame.pack(pady=20, expand=True, fill='both')
#
#     # Title above the original ingredients
#     original_title = Label(text_frame, text='Original Ingredients', font=('Helvetica bold', 16))
#     original_title.grid(row=0, column=0, padx=10)
#
#     # Title above the converted ingredients
#     converted_title = Label(text_frame, text='Converted Ingredients', font=('Helvetica bold', 16))
#     converted_title.grid(row=0, column=1, padx=10)
#
#     # Text widgets for ingredients
#     txt_original = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
#     txt_original.grid(row=1, column=0, padx=10)
#
#     txt_converted = Text(text_frame, height=20, width=40, font=('Helvetica', 14))
#     txt_converted.grid(row=1, column=1, padx=10)
#
#     return txt_original, txt_converted
#
#
# # Add the shared text area to the URL tab
# txt_original_url, txt_converted_url = add_text_frames(url_tab)
#
#
#
#
# # ================= Image Converter Tab =================
# # Button to open an image and process it
# open_image = Button(image_tab, width=20, text='Open Image', font=('Helvetica bold', 20),
#                     command=lambda: openPictureAndConvert())
# open_image.pack(pady=(10, 5))
#
# # Add shared text area to the Image tab
# txt_original_img, txt_converted_img = add_text_frames(image_tab)
#
#
#
#
# # ================= Search Tab =================
# # Title for search functionality
# search_label = Label(search_tab, text="Search Dessert Recipes", font=('Helvetica bold', 24))
# search_label.pack(pady=10)
#
# # Frame for search input and button
# search_frame = Frame(search_tab)
# search_frame.pack(pady=(10, 5))
#
# # Input field for search
# search_entry = Entry(search_frame, width=50, font=('Helvetica', 16))
# search_entry.grid(row=0, column=0, padx=(10, 5))
#
# # Button to perform search
# def perform_search():
#     dessert_name = search_entry.get()
#     if not dessert_name.strip():
#         sendError("Please enter a dessert name!")
#         return
#
#     sendSuccess("Searching for recipes...")
#     results = search_dessert_google(dessert_name)  # Call the external logic
#     results.sort(key=lambda x: x.reviews_count, reverse=True)
#     if results:
#         search_results_txt.delete(1.0, END)
#         search_results_txt.insert(END, "\n".join([item.__str__() for item in results]))
#         sendSuccess("Search completed!")
#     else:
#         sendError("No results found or an error occurred.")
#
#
# search_button = Button(search_frame, text='Search', font=('Helvetica bold', 14), command=perform_search)
# search_button.grid(row=0, column=1, padx=(5, 10))
#
# # Text widget for displaying search results
# search_results_txt = Text(search_tab, height=20, width=90, font=('Helvetica', 12))
# search_results_txt.pack(pady=(10, 5))
#
# # ================= Error/Success Messages =================
# msg_label = Label(app, text="", font=('Helvetica bold', 16))
# msg_label.pack(pady=10, side=BOTTOM)
#
#
#
#
# # ================= Functions =================
# def sendError(msg):
#     msg_label.config(text=msg, fg='red')
#
# def sendSuccess(msg):
#     msg_label.config(text=msg, fg='green')
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
#         recipeObj = RecipeObject("", "", url)
#         recipeObj.setConvertedIngredients(newIngredients)
#         recipeObj.setOriginalIngredients(original)
#         recipeObj.setInstructions([])
#         printWithInstructions(recipeObj, txt_original_url, txt_converted_url)
#         #printList(original, newIngredients, txt_original_url, txt_converted_url)
#
#
# def printWithInstructions(recipeObject, txt_original, txt_converted):
#     txt_original.delete(1.0, END)
#     txt_converted.delete(1.0, END)
#     for item in recipeObject.getOriginalIngredients():
#         txt_original.insert(END, "• " + item + "\n")
#     for item in recipeObject.getConvertedIngredients():
#         txt_converted.insert(END, "• " + item + "\n")
#     for item in recipeObject.getInstructions():
#         #txt_instructions.insert(END, "• " + item + "\n")
#         pass
#
# def printList(originalList, convertedList, txt_original, txt_converted):
#     txt_original.delete(1.0, END)
#     txt_converted.delete(1.0, END)
#     for item in originalList:
#         txt_original.insert(END, "• " + item + "\n")
#     for item in convertedList:
#         txt_converted.insert(END, "• " + item + "\n")
#
# def openPictureAndConvert():
#     path = filedialog.askopenfilename()
#     if path:
#         original, newIngredients = startFuncFromImage(path)
#
#         printList(original, newIngredients, txt_original_img, txt_converted_img)
#
# def startFuncFromWebScraping(url):
#     result = list()
#     ingredientsAndDirections = getIngredientsFromWebScraping(url)
#     if ingredientsAndDirections is None:
#         return None, None
#     if type(ingredientsAndDirections) is str:
#         sendError(ingredientsAndDirections)
#         return None, None
#     ingredients = ingredientsAndDirections["ingredients"]
#     instructions = ingredientsAndDirections["instructions"]
#     if type(ingredients) is str:
#         return None, ingredients
#     for sentence in ingredients:
#         curr = convertToGrams(sentence)
#         result.append(curr)
#     return ingredients, result
#
# def startFuncFromImage(path):
#     converted = list()
#     img = mpimg.imread(path)
#     ingredients = readPictureFromWeb(img)
#     for sentence in ingredients:
#         curr = convertToGrams(sentence)
#         converted.append(curr)
#     return ingredients, converted
#
#
# # Run the app
# if __name__ == '__main__':
#     app.mainloop()
#
