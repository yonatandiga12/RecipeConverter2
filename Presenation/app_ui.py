import threading
import time
import webbrowser
from tkinter import *
from tkinter.ttk import Notebook, Frame as TtkFrame, Style
from tkinter import filedialog, ttk
from typing import List

from Business.RecipeObject import RecipeObject
from Business.seleniumConvertToText import SUPPORTED_SITES
from Presenation.recipe_processor import RecipeProcessor

FONT = 'Courier'
BOLD_FONT = 'Courier bold'

class RecipeConverterUI:

    def __init__(self):
        self.app = Tk()
        self.processor = RecipeProcessor()
        self.setup_main_window()
        self.setup_styles()
        self.create_notebook()
        self.create_tabs()
        self.create_status_bar()

    def setup_main_window(self):
        self.app.title('Recipe Converter')
        self.app.state('zoomed')
        self.app.configure(bg="sky blue")

    def setup_styles(self):
        style = Style()
        style.theme_use('default')

        # Configure notebook tabs
        style.configure('TNotebook',
                        tabposition='wn')

        style.configure('TNotebook.Tab',
                        font=(FONT, 16),
                        padding=[20, 15],
                        width=13,
                        anchor="w")

        # Configure frames
        style.configure('Tab.TFrame')


    def create_notebook(self):
        self.notebook = Notebook(self.app)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)


    def create_tabs(self):
        # Create tab frames
        self.url_tab = TtkFrame(self.notebook)
        self.image_tab = TtkFrame(self.notebook)
        self.search_tab = TtkFrame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.url_tab, text='URL Converter')
        self.notebook.add(self.search_tab, text='Search')
        self.notebook.add(self.image_tab, text='Open Image')

        # Setup each tab's content
        self.setup_url_tab()
        self.setup_image_tab()
        self.setup_search_tab()

    def setup_url_tab(self):
        # Title
        title = Label(self.url_tab, text='Recipe Converter',
                     font=(BOLD_FONT, 50), bg="sky blue")
        title.pack(pady=50)

        # Center container
        center_frame = Frame(self.url_tab, bg="sky blue")
        center_frame.pack(expand=True)

        # URL Entry
        self.url_entry = Entry(center_frame, width=60, font=(FONT, 22))
        self.url_entry.pack(pady=(10, 5))

        # Convert Button
        convert_btn = Button(center_frame, width=20, text='Convert',
                           font=(BOLD_FONT, 25),
                           command=self.process_url2, fg="black")
        convert_btn.pack(pady=(10, 5))

    #   #For displaying the conversion in the same window
    # def setup_url_tab(self):
    #     # Title
    #     title = Label(self.url_tab, text='Recipe Converter',
    #                   font=(BOLD_FONT, 36), bg="#d3eaf7")
    #     title.pack(pady=10)
    #
    #     # URL Entry
    #     self.url_entry = Entry(self.url_tab, width=50, font=(FONT, 16))
    #     self.url_entry.pack(pady=(10, 5))
    #
    #     # Convert Button
    #     convert_btn = Button(self.url_tab, width=20, text='Convert',
    #                          font=(BOLD_FONT, 16),
    #                          command=self.process_url,
    #                          bg="#6aa7cf", fg="white")
    #     convert_btn.pack(pady=(10, 5))
    #
    #     # Text areas
    #     self.txt_original_url, self.txt_converted_url = self.add_text_frames(self.url_tab)
    #
    #     # Instructions area
    #     self.create_instructions_area()

    def create_instructions_area(self):
        self.instructions_frame = LabelFrame(self.url_tab, text="Recipe Instructions",
                                             font=(BOLD_FONT, 16), bg="#d3eaf7")
        self.instructions_frame.pack(fill="x", pady=10, padx=20)

        self.instructions_text = Text(self.instructions_frame, height=8,
                                      font=(FONT, 12), bg="#d3eaf7", wrap=WORD)
        self.instructions_text.pack(padx=10, pady=10, fill="both", expand=True)

    def setup_image_tab(self):
        open_btn = Button(self.image_tab, width=20, text='Open Image',
                          font=(BOLD_FONT, 20),
                          command=self.open_image,
                          bg="#6aa7cf", fg="white")
        open_btn.pack(pady=(10, 5))

        self.txt_original_img, self.txt_converted_img = self.add_text_frames(self.image_tab)

    def setup_search_tab(self):
        # Search label
        search_label = Label(self.search_tab, text="Search Dessert Recipes",
                             font=(BOLD_FONT, 24), bg="#d3eaf7")
        search_label.pack(pady=10)

        # Search frame
        search_frame = Frame(self.search_tab, bg="#d3eaf7")
        search_frame.pack(pady=(10, 5))

        # Search entry
        self.search_entry = Entry(search_frame, width=50, font=(FONT, 16))
        self.search_entry.grid(row=0, column=0, padx=(10, 5))

        # Search button
        search_btn = Button(search_frame, text='Search',
                            font=(BOLD_FONT, 14),
                            command=self.search_with_loading,
                            bg="#6aa7cf", fg="white")
        search_btn.grid(row=0, column=1, padx=(5, 10))

        # Results area
        self.setup_search_results()

    # def setup_search_results(self):
    #     screen_width = self.app.winfo_screenwidth()
    #     screen_height = self.app.winfo_screenheight()
    #
    #     text_width = int(screen_width * 0.8 / 10)
    #     text_height = int(screen_height * 0.6 / 20)
    #
    #     self.search_results_txt = Text(self.search_tab, height=text_height,
    #                                    width=text_width, font=(FONT, 12),
    #                                    bg="white")
    #     self.search_results_txt.pack(pady=(10, 5), expand=True, fill='both')

    def setup_search_results(self):
        # Create a scrollable canvas
        self.canvas_frame = Frame(self.search_tab, bg="#d3eaf7")
        self.canvas_frame.pack(expand=True, fill='both', pady=(10, 5))

        self.results_canvas = Canvas(self.canvas_frame, bg="#d3eaf7")
        self.results_scrollbar = Scrollbar(self.canvas_frame, orient="vertical", command=self.results_canvas.yview)
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)

        self.scrollable_frame = Frame(self.results_canvas, bg="#d3eaf7")

        # Bind the canvas to the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )

        self.results_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.results_canvas.pack(side=LEFT, expand=True, fill="both")
        self.results_scrollbar.pack(side=RIGHT, fill="y")

    def create_status_bar(self):
        self.msg_label = Label(self.app, text="", font=(BOLD_FONT, 16),
                               bg="#d3eaf7")
        self.msg_label.pack(pady=10, side=BOTTOM)

    # Only for Image Tab
    def add_text_frames(self, parent):
        container = Frame(parent, bg="#d3eaf7")
        container.pack(pady=20, expand=True, fill='both')
        container.grid_columnconfigure(0, weight=1)

        text_frame = Frame(container, bg="#d3eaf7")
        text_frame.grid(row=1, column=0)

        # Titles
        Label(text_frame, text='Original Ingredients',
              font=(BOLD_FONT, 16), bg="#d3eaf7").grid(row=0, column=0,
                                                              padx=20, pady=(0, 10))
        Label(text_frame, text='Converted Ingredients',
              font=(BOLD_FONT, 16), bg="#d3eaf7").grid(row=0, column=1,
                                                              padx=20, pady=(0, 10))

        # Text widgets
        txt_original = Text(text_frame, height=20, width=50,
                            font=(FONT, 14), bg="#d3eaf7")
        txt_original.grid(row=1, column=0, padx=20)

        txt_converted = Text(text_frame, height=20, width=50,
                             font=(FONT, 14), bg="#d3eaf7")
        txt_converted.grid(row=1, column=1, padx=20)

        return txt_original, txt_converted

    def send_error(self, msg):
        self.msg_label.config(text=msg, fg='red')

    def send_success(self, msg):
        self.msg_label.config(text=msg, fg='green')

    #   # For displaying the conversion in the same window
    # def process_url(self):
    #     url = self.url_entry.get()
    #     if url:
    #         result = self.processor.process_url(url)
    #         if result.success:
    #             self.send_success("Recipe converted!")
    #             self.update_display(result)
    #         else:
    #             self.send_error(result.error_message)

    def process_url2(self):
        url = self.url_entry.get()
        if url:
            self.process_with_loading(url)  #Using the function with the loading bar, if don't want it, uncomment bottom
            # result = self.processor.process_url(url)
            # if result.success:
            #     self.send_success("Recipe converted!")
            #     # Create popup window with recipe details
            #     RecipeDisplayWindow(self.app, result)
            # else:
            #     self.send_error(result.error_message)


    def open_image(self):
        path = filedialog.askopenfilename()
        if path:
            result = self.processor.process_image(path)
            if result.success:
                self.update_display(result)
            else:
                self.send_error(result.error_message)

    # def perform_search(self):
    #     query = self.search_entry.get()
    #     if not query.strip():
    #         self.send_error("Please enter a dessert name!")
    #         return
    #
    #     self.send_success("Searching for recipes...")
    #     result = self.processor.search_recipes(query)
    #     if result.success:
    #         self.search_results_txt.delete(1.0, END)
    #         self.search_results_txt.insert(END, result.formatted_results)
    #         self.send_success("Search completed!")
    #     else:
    #         self.send_error(result.error_message)

    import webbrowser  # Add this import at the top of your file

    def populate_search_results(self, recipes: List[RecipeObject]):
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for i, recipe in enumerate(recipes):
            siteName = recipe.getSiteName()
            recipeName = recipe.getRecipeName()
            rating = recipe.getRating()
            reviewCount = recipe.getReviewsCount()
            urlOfRecipe = recipe.getURL()

            # Create a small "cube" for each recipe
            recipe_frame = Frame(self.scrollable_frame, bg="white", borderwidth=1, relief="solid")
            recipe_frame.grid(row=i // 7, column=i % 7, padx=10, pady=10, sticky="nsew")

            # Recipe details
            recipe_label = Label(recipe_frame, text=recipeName, font=(FONT, 14), bg="white", wraplength=150)
            recipe_label.pack(pady=(10, 5), padx=10)

            site_label = Label(recipe_frame, text=f"From: {siteName}", font=(FONT, 10), bg="white")
            site_label.pack(pady=(0, 5))

            rating_label = Label(recipe_frame, text=f"Rating: {rating} ({reviewCount} reviews)",
                                 font=(FONT, 10), bg="white")
            rating_label.pack(pady=(0, 10))

            # Clickable button for site processing
            view_button = Button(recipe_frame, text="Convert Recipe", font=(FONT, 10), bg="#6aa7cf", fg="white",
                                 command=lambda url=urlOfRecipe: self.process_with_loading(url))
            view_button.pack(pady=(0, 5), padx=10)

            # New button to open URL in the browser
            open_url_button = Button(recipe_frame, text="Open URL", font=(FONT, 10), bg="#3cb371", fg="white",
                                     command=lambda url=urlOfRecipe: webbrowser.open(url))
            open_url_button.pack(pady=(0, 10), padx=10)

        # Adjust column weights
        for col in range(7):
            self.scrollable_frame.grid_columnconfigure(col, weight=1)

    def process_with_loading(self, url):
        """
        Displays a loading popup and processes the recipe URL.
        """
        # Create a popup window for the progress bar
        progress_popup = Toplevel(self.app)
        progress_popup.title("Processing Recipe")
        progress_popup.geometry("300x100")
        progress_popup.configure(bg="#d3eaf7")
        progress_popup.transient(self.app)
        progress_popup.grab_set()

        # Center the popup
        progress_popup.update_idletasks()
        x = (progress_popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (progress_popup.winfo_screenheight() // 2) - (100 // 2)
        progress_popup.geometry(f"+{x}+{y}")

        # Add a label and progress bar
        label = Label(progress_popup, text=f"Processing Recipe...", font=("Helvetica", 14), bg="#d3eaf7")
        label.pack(pady=(20, 10))
        progress_bar = ttk.Progressbar(progress_popup, mode="indeterminate", length=250)
        progress_bar.pack(pady=(0, 20))
        progress_bar.start()

        # Function to process the URL in a separate thread
        def process_task():
            try:
                result = self.processor.process_url(url)
                self.app.after(0, lambda: self.handle_processing_result(result))
            except Exception as e:
                self.app.after(0, lambda: self.send_error(f"An error occurred: {str(e)}"))
            finally:
                self.app.after(0, progress_popup.destroy)

        # Start processing in a new thread
        process_thread = threading.Thread(target=process_task)
        process_thread.start()

    def handle_processing_result(self, result):
        if result.success:
            self.send_success("Recipe processed successfully!")
            RecipeDisplayWindow(self.app, result)
        else:
            self.send_error(result.error_message)

    def search_with_loading(self):
        """
        Displays a loading popup with a progress bar while performing the search.
        """
        query = self.search_entry.get()
        if not query.strip():
            self.send_error("Please enter a dessert name!")
            return
        # Create a popup window for the progress bar
        progress_popup = Toplevel(self.app)
        progress_popup.title("Searching Recipes")
        progress_popup.geometry("300x150")  # Increased height for text and progress bar
        progress_popup.configure(bg="#d3eaf7")
        progress_popup.transient(self.app)
        progress_popup.grab_set()

        # Center the popup
        progress_popup.update_idletasks()
        x = (progress_popup.winfo_screenwidth() // 2) - (300 // 2)
        y = (progress_popup.winfo_screenheight() // 2) - (150 // 2)
        progress_popup.geometry(f"+{x}+{y}")

        # Add a label and progress bar
        label = Label(progress_popup, text="Searching for Recipes...", font=("Helvetica", 14), bg="#d3eaf7")
        label.pack(pady=(10, 10))
        progress_bar = ttk.Progressbar(progress_popup, mode="indeterminate", length=250)
        progress_bar.pack(pady=(0, 10))
        progress_bar.start()

        # Add dynamic text below the progress bar
        dynamic_label = Label(progress_popup, text="", font=("Helvetica", 12), bg="#d3eaf7")
        dynamic_label.pack(pady=(5, 10))

        # Function to update dynamic text
        def update_dynamic_text():
            steps = SUPPORTED_SITES
            for step in steps:
                dynamic_label.config(text=f"Searching in {step}")
                progress_popup.update_idletasks()
                #When doing sleep it freezes the progressbar but shows all the sites
                #time.sleep(9)  # Simulate a delay for each step

        # Function to perform the search in a separate thread
        def search_task():
            try:
                self.app.after(0, update_dynamic_text)  # Update dynamic text in the main thread
                result = self.processor.search_recipes(query)
                self.app.after(0, lambda: self.handle_search_result(result))
            except Exception as e:
                self.app.after(0, lambda: self.send_error(f"An error occurred: {str(e)}"))
            finally:
                self.app.after(0, progress_popup.destroy)

        # Start search in a new thread
        search_thread = threading.Thread(target=search_task)
        search_thread.start()

    def handle_search_result(self, result):
        if result.success:
            self.populate_search_results(result.resultList)
            self.send_success("Search completed successfully!")
        else:
            self.send_error(result.error_message)



    # def update_display(self, result):
    #     # Clear previous content
    #     self.txt_original_url.delete(1.0, END)
    #     self.txt_converted_url.delete(1.0, END)
    #     self.instructions_text.delete(1.0, END)
    #
    #     # Update with new content
    #     for item in result.original_ingredients:
    #         self.txt_original_url.insert(END, f"• {item}\n")
    #     for item in result.converted_ingredients:
    #         self.txt_converted_url.insert(END, f"• {item}\n")
    #     for item in result.instructions:
    #         self.instructions_text.insert(END, f"• {item}\n")

    def run(self):
        self.app.mainloop()





class RecipeDisplayWindow:
    def __init__(self, parent, recipe_result):
        self.window = Toplevel(parent)
        self.window.title('Recipe Details')
        self.window.state('zoomed')
        self.window.configure(bg="#d3eaf7")

        self.create_recipe_display()
        self.update_display(recipe_result)

    #For pop up window
    def create_recipe_display(self):
        # Create main container
        container = Frame(self.window, bg="#d3eaf7")
        container.pack(pady=20, expand=True, fill='both')

        # Top frame for ingredients
        ingredients_frame = Frame(container, bg="#d3eaf7")
        ingredients_frame.pack(fill='both', padx=20, pady=(0, 10))

        # Original ingredients
        original_frame = LabelFrame(ingredients_frame, text='Original Ingredients',
                                    font=(BOLD_FONT, 16), bg="#d3eaf7")
        original_frame.pack(side=LEFT, fill='both', expand=True, padx=10)

        self.txt_original = Text(original_frame, height=10, width=50,
                                 font=(FONT, 16), bg="#d3eaf7")
        self.txt_original.pack(padx=10, pady=10, fill='both', expand=True)

        # Converted ingredients
        converted_frame = LabelFrame(ingredients_frame, text='Converted Ingredients',
                                     font=(BOLD_FONT, 16), bg="#d3eaf7")
        converted_frame.pack(side=LEFT, fill='both', expand=True, padx=10)

        self.txt_converted = Text(converted_frame, height=20, width=50,
                                  font=(FONT, 16), bg="#d3eaf7")
        self.txt_converted.pack(padx=10, pady=10, fill='both', expand=True)

        # Instructions frame at bottom
        instructions_frame = LabelFrame(container, text="Recipe Instructions",
                                        font=(BOLD_FONT, 16), bg="#d3eaf7")
        instructions_frame.pack(fill='both', expand=True, padx=20, pady=(20, 10))

        self.txt_instructions = Text(instructions_frame, height=8,
                                     font=(FONT, 16), bg="#d3eaf7", wrap=WORD)
        self.txt_instructions.pack(padx=10, pady=10, fill='both', expand=True)

    def update_display(self, result):
        # Clear previous content
        self.txt_original.delete(1.0, END)
        self.txt_converted.delete(1.0, END)
        self.txt_instructions.delete(1.0, END)

        # Update with new content
        for item in result.original_ingredients:
            DOTORNOT = '' if item == '\n' else '•'
            self.txt_original.insert(END, f"{DOTORNOT} {item}\n")

        for item in result.converted_ingredients:
            DOTORNOT = '' if item == '\n' else '•'
            self.txt_converted.insert(END, f"{DOTORNOT} {item}\n")

        for item in result.instructions:
            DOTORNOT = '' if item == '\n' else '•'
            self.txt_instructions.insert(END, f"{DOTORNOT} {item}\n\n")

