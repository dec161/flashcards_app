import tkinter as tk
from tkinter import ttk
import sqlite3
import random
from .app_config import AppConfig
from .message_box import MessageBox


class FlashcardsApp:
    def __init__(self, root, app_config: AppConfig):
        self.app_config = app_config
        self.root = root
        self.root.title("Угадалка")
        self.root.geometry("1200x600")
        self.root.configure(bg=self.app_config.primary_color)

        self.db_name = 'dictionary.db'  # Имя базы данных
        self.language = None
        self.words = []
        self.current_word = None
        self.correct_answers = 0
        self.wrong_answers = 0

        # Main Frame
        self.flashcards_frame = tk.Frame(root, bg=self.app_config.primary_color)
        self.flashcards_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.title_label = ttk.Label(self.flashcards_frame, text="Угадалка", font=("Segoe UI", 28, "bold"),
                                     anchor="center")
        self.title_label.pack(pady=20)

        # Загрузка и установка изображения для кнопки "Начать игру"
        self.start_button = ttk.Button(self.flashcards_frame, text="Начать игру",
                                       command=self.start_game)
        self.app_config.configure_button(self.start_button)
        self.start_button.pack(pady=10)

        self.word_label = ttk.Label(self.flashcards_frame, text="", font=("Segoe UI", 40, "bold"), anchor="center")
        self.word_label.pack(pady=10)

        self.entry = ttk.Entry(self.flashcards_frame, font=("Segoe UI", 18), justify="center", width=20)
        self.entry.pack(pady=10)

        # Загрузка и установка изображения для кнопки "Проверить перевод"
        self.check_button = ttk.Button(self.flashcards_frame, text="Проверить перевод", command=self.check_translation)
        self.app_config.configure_button(self.check_button)
        self.check_button.pack(pady=5)

        self.message_label = ttk.Label(self.flashcards_frame, text="", font=("Segoe UI", 16), anchor="center")
        self.message_label.pack(pady=10)

        self.stats_label = ttk.Label(self.flashcards_frame, text="Правильно: 0 | Неправильно: 0", font=("Segoe UI", 14))
        self.stats_label.pack(pady=10)

    def set_language(self, language):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT id_language FROM Language WHERE name_language=?", (language,))
            language_id = cursor.fetchone()[0]

            cursor.execute(''' 
                SELECT DISTINCT w.word, t.translation
                FROM Word w
                JOIN Translation t ON w.id_word = t.word_id
                WHERE t.language_id = ? 
            ''', (language_id,))
            self.words = cursor.fetchall()
            conn.close()
        except Exception as e:
            MessageBox.show(f"Не удалось загрузить слова из базы данных: {e}", "Ошибка",
                            master=self.root, app_config=self.app_config)
        else:
            if not self.words:
                MessageBox.show(f"Нет данных для языка {self.language} в базе данных!", "Ошибка",
                                master=self.root, app_config=self.app_config)

    def stop(self):
        for child in self.root.winfo_children():
            child.destroy()

    def start_game(self):
        """Запускает игру после выбора языка."""
        self.correct_answers = 0
        self.wrong_answers = 0
        self.update_stats()
        self.show_word()

    def show_word(self):
        """Показывает новое слово для изучения на выбранном языке."""
        if not self.words:
            MessageBox.show("Нет слов для изучения!", "Информация",
                            master=self.root, app_config=self.app_config)
            return

        new_word = random.choice(self.words)
        if len(self.words) > 1:
            while new_word == self.current_word:
                new_word = random.choice(self.words)

        self.current_word = new_word
        self.word_label.config(text=self.current_word[1])  # Показываем слово на выбранном языке (например, английский)
        self.entry.delete(0, tk.END)
        self.message_label.config(text="")

    def check_translation(self):
        """Проверяет правильность перевода на русский язык."""
        if not self.current_word:
            MessageBox.show("Сначала выберите слово!", "Ошибка",
                            master=self.root, app_config=self.app_config)
            return

        user_input = self.entry.get().strip().lower()
        correct_translation = self.current_word[0].lower()  # Перевод на русский

        if user_input == correct_translation:
            self.message_label.config(text="Правильно!", foreground=self.app_config.answer_correct_color)
            self.correct_answers += 1
            self.show_word()
        else:
            self.message_label.config(
                text=f"Ошибка! пробуй снова :))))",
                foreground=self.app_config.answer_incorrect_color
            )
            self.wrong_answers += 1

        self.update_stats()

    def update_stats(self):
        """Обновляет статистику."""
        self.stats_label.config(
            text=f"Правильно: {self.correct_answers} | Неправильно: {self.wrong_answers}"
        )
