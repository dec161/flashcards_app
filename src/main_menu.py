import tkinter as tk
from tkinter import ttk

import sqlite3

from .app_config import AppConfig
from .flashcards_game import FlashcardsApp
from .translator_app import TranslatorApp  # Импортируем новый файл для переводчика
from .play_timer import TimerFlashcardsApp  # Импортируем play_timer для запуска игры
from .True_False import TrueFalseGame  # Импортируем класс игры
from .message_box import MessageBox


class MainMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_name = "dictionary.db"
        self.app_config = AppConfig()
        self.config(bg=self.app_config.primary_color)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.close)

        title_text = "Polyglot Nexus"
        self.title(title_text)

        self.game = None
        
        self.game_window = tk.Toplevel(self)
        self.game_window.protocol("WM_DELETE_WINDOW", self.close_game)
        self.game_window.withdraw()

        self.translator_window = tk.Toplevel(self)
        TranslatorApp(self.translator_window, self.app_config)
        self.translator_window.protocol("WM_DELETE_WINDOW", self.translator_window.withdraw)
        self.translator_window.withdraw()

        frame = tk.Frame()
        frame.config(bg=self.app_config.primary_color)
        frame.grid(ipadx=50, ipady=60)

        for i in range(1, 4):
            frame.rowconfigure(i, weight=1)
        for i in range(2):
            frame.rowconfigure(i, weight=2)
            frame.columnconfigure(i, weight=1)

        title_label = ttk.Label(frame, text=title_text, font=("Segoe UI", 28, "bold"))
        title_label.grid(row=0, column=0, columnspan=2)

        translator_button = ttk.Button(frame, text="Переводчик",
                                            command=self.start_translator)
        self.app_config.configure_button(translator_button)
        translator_button.grid(row=3, column=1)

        flashcards_game_button = ttk.Button(frame, text="Обычная игра", command=lambda: self.open_game(FlashcardsApp))
        self.app_config.configure_button(flashcards_game_button)
        flashcards_game_button.grid(row=2, column=0)

        play_game_button = ttk.Button(frame, text="Игра на время", command=lambda: self.open_game(TimerFlashcardsApp))
        self.app_config.configure_button(play_game_button)
        play_game_button.grid(row=3, column=0)

        true_false_game_button = ttk.Button(frame, text="Правда или Ложь", command=lambda: self.open_game(TrueFalseGame))
        self.app_config.configure_button(true_false_game_button)
        true_false_game_button.grid(row=2, column=1)

        language_select_frame = tk.Frame(frame)
        language_select_frame.config(bg=self.app_config.primary_color)
        language_select_frame.grid(row=1, column=0, columnspan=2, ipady=10)

        for i in range(2):
            language_select_frame.rowconfigure(i, weight=1)

        self.language_label = ttk.Label(language_select_frame, text="Выберите язык для игры",
                                        font=("Segoe UI", 18, "bold"))
        self.language_label.grid(row=0, column=0)

        self.language_combobox = ttk.Combobox(language_select_frame, values=[], font=("Segoe UI", 14))
        self.language_combobox.grid(row=1, column=0)

        self.load_languages()

    def close(self):
        self.translator_window.destroy()
        self.game_window.destroy()
        self.destroy()

    def get_language(self):
        selected_language = self.language_combobox.get()

        if not selected_language:
            MessageBox.show("Выберите язык для игры!", "Ошибка",
                            master=self, app_config=self.app_config)

        return selected_language

    def start_translator(self):
        """Запускает окно переводчика."""
        self.translator_window.deiconify()
        self.translator_window.lift()

    def open_game(self, game_type):
        language = self.get_language()

        if not language:
            return

        if self.game:
            self.game.stop()

        self.game = game_type(self.game_window, self.app_config)
        self.game.set_language(language)

        self.game_window.protocol("WM_DELETE_WINDOW", self.close_game)
        self.game_window.deiconify()
        self.game_window.lift()

    def close_game(self):
        if self.game:
            self.game.stop()
        self.game_window.withdraw()

    def load_languages(self):
        """Загружает доступные языки из базы данных."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name_language FROM Language")
            languages = [row[0] for row in cursor.fetchall()]
            conn.close()

            if languages:
                if "Russian" in languages:
                    languages.remove("Russian")
                self.language_combobox['values'] = languages
            else:
                MessageBox.show("В базе данных нет доступных языков!", "Ошибка",
                                master=self, app_config=self.app_config)
        except Exception as e:
            MessageBox.show(f"Не удалось загрузить языки: {e}", "Ошибка",
                            master=self, app_config=self.app_config)
