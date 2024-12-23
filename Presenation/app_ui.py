from tkinter import *
from tkinter.ttk import Notebook, Frame as TtkFrame, Style
from tkinter import filedialog

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
                           command=self.process_url, fg="black")
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
                            command=self.perform_search,
                            bg="#6aa7cf", fg="white")
        search_btn.grid(row=0, column=1, padx=(5, 10))

        # Results area
        self.setup_search_results()

    def setup_search_results(self):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        text_width = int(screen_width * 0.8 / 10)
        text_height = int(screen_height * 0.6 / 20)

        self.search_results_txt = Text(self.search_tab, height=text_height,
                                       width=text_width, font=(FONT, 12),
                                       bg="white")
        self.search_results_txt.pack(pady=(10, 5), expand=True, fill='both')

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

    def process_url(self):
        url = self.url_entry.get()
        if url:
            result = self.processor.process_url(url)
            if result.success:
                self.send_success("Recipe converted!")
                # Create popup window with recipe details
                RecipeDisplayWindow(self.app, result)
            else:
                self.send_error(result.error_message)

    def open_image(self):
        path = filedialog.askopenfilename()
        if path:
            result = self.processor.process_image(path)
            if result.success:
                self.update_display(result)
            else:
                self.send_error(result.error_message)

    def perform_search(self):
        query = self.search_entry.get()
        if not query.strip():
            self.send_error("Please enter a dessert name!")
            return

        self.send_success("Searching for recipes...")
        result = self.processor.search_recipes(query)
        if result.success:
            self.search_results_txt.delete(1.0, END)
            self.search_results_txt.insert(END, result.formatted_results)
            self.send_success("Search completed!")
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
            self.txt_original.insert(END, f"• {item}\n")
        for item in result.converted_ingredients:
            self.txt_converted.insert(END, f"• {item}\n")
        for item in result.instructions:
            self.txt_instructions.insert(END, f"• {item}\n")

