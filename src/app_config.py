from tkinter import ttk
from PIL import Image, ImageTk


class AppConfig:
    def __init__(self):
        self.primary_color = "#1e1e1e"
        self.secondary_color = "#4caf50"

        self.alt_primary_color = "#ffffff"
        self.alt_secondary_color = "#000000"

        self.button_foreground = "#000000"

        self.answer_correct_color = "green"
        self.answer_incorrect_color = "red"

        self.graph_foreground = "#ffffff"

        try:
            image_dimensions = 200, 50

            self.button_image = ImageTk.PhotoImage(Image.open("button.png")
                                                   .resize(image_dimensions, Image.Resampling.LANCZOS))
            self.button_highlight = ImageTk.PhotoImage(Image.open("button-highlight.png")
                                                       .resize(image_dimensions, Image.Resampling.LANCZOS))
        except FileNotFoundError:
            self.button_image = None
            self.button_highlight = None

        self.style = ttk.Style()

        self.style.configure("TLabel", font=("Segoe UI", 14), background=self.primary_color,
                             foreground=self.secondary_color)

        self.style.configure("TCombobox", background=self.alt_primary_color, foreground=self.alt_secondary_color)
        self.style.configure("TEntry", background=self.alt_primary_color, foreground=self.alt_secondary_color)

        if self.button_image:
            self.style.configure("TButton", border="0", font=("Segoe UI", 14), padding=0, relief="flat",
                                 background=self.primary_color, foreground=self.button_foreground, borderwidth=0, width=15,
                                 justify="center", image=self.button_image, compound="center")
            self.style.map("TButton", background=[("active", self.primary_color)])


    def configure_button(self, button: ttk.Button):
        if self.button_image:
            def on_enter(_):
                button.config(image=self.button_highlight)
                button.image = self.button_highlight
            button.bind("<Enter>", func=on_enter)

        if self.button_highlight:
            def on_leave(_):
                button.config(image=self.button_image)
                button.image = self.button_image
            button.bind("<Leave>", func=on_leave)
