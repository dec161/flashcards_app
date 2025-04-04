import tkinter as tk
from tkinter import ttk
import random
from .app_config import AppConfig
from .message_box import MessageBox


# Главное окно приложения
class TrueFalseGame:
    def __init__(self, root, app_config: AppConfig):
        self.app_config = app_config
        self.root = root
        self.root.title("Игра: Правда или Ложь")
        self.root.geometry("1400x400")
        self.root.configure(bg=self.app_config.primary_color)
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        self.questions = None
        self.current_question = None
        self.language = None
        self.correct_answers = 0
        self.wrong_answers = 0
        self.questions_db = {
            "English": [
                ("Слово 'house' переводится как 'дом'.", "Правда", "Ложь"),
                ("Слово 'pneumonoultramicroscopicsilicovolcanoconiosis' существует", "Правда", "Ложь"),
                ("Слово 'hippopotomonstrosesquippedaliophobia' существует", "Правда", "Ложь"),
                ("Слово 'dog' переводится как 'собака'.", "Правда", "Ложь"),
                ("Слово 'apple' переводится как 'яблоко'.", "Правда", "Ложь"),
                ("Слово 'tree' переводится как 'дерево'.", "Правда", "Ложь"),
                ("Предложение 'I are a student' построено правильно.", "Ложь", "Правда"),
                ("Слово 'car' переводится как 'машина'.", "Правда", "Ложь"),
                ("Слово 'car' переводится как 'друг'.", "Ложь", "Правда"),
                ("Слово 'water' переводится как 'вода'.", "Правда", "Ложь"),
                ("Слово 'friend' переводится как 'друг'.", "Правда", "Ложь"),
                ("Слово 'school' переводится как 'школа'.", "Правда", "Ложь"),
                ("Слово 'city' переводится как 'город'.", "Правда", "Ложь"),
                ("Слово 'sun' переводится как 'солнце'.", "Правда", "Ложь"),
                ("Слово 'moon' переводится как 'луна'.", "Правда", "Ложь"),
                ("Слово 'food' переводится как 'еда'.", "Правда", "Ложь"),
                ("Предложение 'She are playing the piano' построено правильно.", "Ложь", "Правда"),
                ("Слово 'cat' переводится как 'кошка'.", "Правда", "Ложь"),
            ],
            "French": [
                ("Слово 'maison' переводится как 'дом'.", "Правда", "Ложь"),
                ("Слово 'maison' переводится как 'кастрюля'.", "Ложь", "Правда"),
                ("Слово 'chien' переводится как 'собака'.", "Правда", "Ложь"),
                ("Слово 'chat' переводится как 'кошка'.", "Правда", "Ложь"),
                ("Слово 'pomme' переводится как 'яблоко'.", "Правда", "Ложь"),
                ("Предложение 'Je suis un étudiant' построено правильно.", "Правда", "Ложь"),
                ("Слово 'arbre' переводится как 'дерево'.", "Правда", "Ложь"),
                ("Слово 'livre' переводится как 'книга'.", "Правда", "Ложь"),
                ("Слово 'voiture' переводится как 'машина'.", "Правда", "Ложь"),
                ("Слово 'voiture' переводится как 'школа'.", "Ложь", "Правда"),
                ("Слово 'eau' переводится как 'вода'.", "Правда", "Ложь"),
                ("Слово 'ami' переводится как 'друг'.", "Правда", "Ложь"),
                ("Слово 'famille' переводится как 'семья'.", "Правда", "Ложь"),
                ("Слово 'école' переводится как 'школа'.", "Правда", "Ложь"),
                ("Предложение 'Il mange une pomme' построено правильно.", "Правда", "Ложь"),
                ("Слово 'soleil' переводится как 'солнце'.", "Правда", "Ложь"),
                ("Слово 'lune' переводится как 'луна'.", "Правда", "Ложь"),
            ],
            "German": [
                ("Слово 'Haus' переводится как 'дом'.", "Правда", "Ложь"),
                ("Слово 'Hund' переводится как 'собака'.", "Правда", "Ложь"),
                ("Слово 'Hund' переводится как 'кошка'.", "Ложь", "Правда"),
                ("Слово 'Katze' переводится как 'кошка'.", "Правда", "Ложь"),
                ("Слово 'Apfel' переводится как 'яблоко'.", "Правда", "Ложь"),
                ("Слово 'Apfel' переводится как 'дом'.", "Ложь", "Правда"),
                ("Предложение 'Ich bin ein Student' построено правильно.", "Правда", "Ложь"),
                ("Слово 'Baum' переводится как 'дерево'.", "Правда", "Ложь"),
                ("Слово 'Buch' переводится как 'книга'.", "Правда", "Ложь"),
                ("Слово 'Auto' переводится как 'машина'.", "Правда", "Ложь"),
                ("Слово 'Wasser' переводится как 'вода'.", "Правда", "Ложь"),
                ("Слово 'Freund' переводится как 'друг'.", "Правда", "Ложь"),
                ("Слово 'Familie' переводится как 'семья'.", "Правда", "Ложь"),
                ("Слово 'Schule' переводится как 'школа'.", "Правда", "Ложь"),
                ("Предложение 'Er spielt Klavier' построено правильно.", "Правда", "Ложь"),
                ("Слово 'Stadt' переводится как 'город'.", "Правда", "Ложь"),
                ("Слово 'Sonne' переводится как 'солнце'.", "Правда", "Ложь"),
            ]
        }

        self.game_frame = tk.Frame(root, bg=self.app_config.primary_color)
        self.game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=30)
        self.game_frame.config(bg=self.app_config.primary_color)

        for i in range(7):
            self.game_frame.rowconfigure(i, weight=1)
        self.game_frame.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self.game_frame, text="Игра: Правда или Ложь", font=("Segoe UI", 24, "bold"),
                                     anchor="center", background=self.app_config.primary_color,
                                     foreground=self.app_config.secondary_color)
        self.title_label.grid(row=0, column=0)

        self.start_button = ttk.Button(self.game_frame, text="Начать игру", command=self.start_game)
        self.app_config.configure_button(self.start_button)
        self.start_button.grid(row=1, column=0)

        self.expression_label = ttk.Label(self.game_frame, text="", font=("Segoe UI", 30, "bold"), anchor="center",
                                          background=self.app_config.primary_color,
                                          foreground=self.app_config.secondary_color)
        self.expression_label.grid(row=2, column=0)

        self.button_frame = tk.Frame(self.game_frame, bg=self.app_config.primary_color)
        self.button_frame.rowconfigure(0, weight=1)
        for i in range(2):
            self.button_frame.columnconfigure(i, weight=1)
        self.button_frame.grid(row=3, column=0, ipadx=50)

        self.true_button = ttk.Button(self.button_frame, text="Правда", command=lambda: self.check_answer(True))
        self.app_config.configure_button(self.true_button)
        self.true_button.grid(row=0, column=0)

        self.false_button = ttk.Button(self.button_frame, text="Ложь", command=lambda: self.check_answer(False))
        self.app_config.configure_button(self.false_button)
        self.false_button.grid(row=0, column=1)

        self.stats_label = ttk.Label(self.game_frame, text="Правильно: 0 | Неправильно: 0", font=("Segoe UI", 14),
                                     background=self.app_config.primary_color,
                                     foreground=self.app_config.secondary_color)
        self.stats_label.grid(row=6, column=0)

    def stop(self):
        for child in self.root.winfo_children():
            child.destroy()

    def set_language(self, language):
        self.language = language

    def start_game(self):
        """Запускает игру после выбора языка."""
        self.questions = self.questions_db[self.language]  # Загружаем вопросы для выбранного языка
        self.correct_answers = 0
        self.wrong_answers = 0
        self.update_stats()
        self.show_question()

    def show_question(self):
        """Показывает новый вопрос для игры."""
        if not self.questions:
            MessageBox.show("Нет вопросов для игры!", "Информация",
                            master=self.root, app_config=self.app_config)
            return

        self.current_question = random.choice(self.questions)
        self.expression_label.config(text=self.current_question[0])  # Показываем вопрос

    def check_answer(self, answer):
        """Проверяет, правильно ли ответил игрок."""
        if not hasattr(self, 'current_question'):
            return

        correct_answer = self.current_question[1]
        if (answer and correct_answer == "Правда") or (not answer and correct_answer == "Ложь"):
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

        self.show_question()
        self.update_stats()

    def update_stats(self):
        """Обновляет статистику на экране."""
        self.stats_label.config(
            text=f"Правильно: {self.correct_answers} | Неправильно: {self.wrong_answers}"
        )
