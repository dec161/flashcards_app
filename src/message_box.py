import tkinter as tk
from tkinter import ttk

from .app_config import AppConfig


class MessageBox(tk.Toplevel):
    def __init__(self, message: str, *args, app_config = None, **kwargs):
        super().__init__(*args, **kwargs)

        if not app_config:
            if hasattr(self.master, "app_config"):
                app_config = self.master.app_config
            else:
                app_config = AppConfig()

        self.config(bg=app_config.primary_color)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        frame = tk.Frame(self, background=app_config.primary_color)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=3)
        frame.rowconfigure(1, weight=1)

        frame.pack(ipady=10, ipadx=20)

        label = ttk.Label(frame, text=message,
                          background=app_config.primary_color,
                          foreground=app_config.secondary_color,
                          font=("Segoe UI", 16, "bold"))
        label.grid(row=0, column=0)

        button = ttk.Button(frame, text="OK", command=self.destroy)
        app_config.configure_button(button)
        button.grid(row=1, column=0, pady=10)

    @staticmethod
    def show(message: str, title: str = None, app_config = None, **kwargs):
        message_box = MessageBox(message, app_config=app_config, **kwargs)

        if title:
            message_box.title(title)

        message_box.deiconify()
