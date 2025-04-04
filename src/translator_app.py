from tkinter import ttk
import sqlite3
from .app_config import AppConfig
from .message_box import MessageBox


class TranslatorApp:
    def __init__(self, root, app_config: AppConfig):
        self.app_config = app_config
        self.root = root
        self.root.title("Переводчик")
        self.root.geometry("400x300")
        self.root.config(bg=self.app_config.primary_color)
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        self.db_name = 'dictionary.db'  # Имя базы данных
        self.language_from = None
        self.language_to = None

        self.title_label = ttk.Label(self.root, text="Переводчик", font=("Segoe UI", 18, "bold"),
                                     background=self.app_config.primary_color,
                                     foreground=self.app_config.secondary_color)
        self.title_label.pack(pady=20)

        self.language_from_label = ttk.Label(self.root, text="Выберите исходный язык", font=("Segoe UI", 14),
                                             background=self.app_config.primary_color,
                                             foreground=self.app_config.secondary_color)
        self.language_from_label.pack(pady=5)

        self.language_from_combobox = ttk.Combobox(self.root, values=[], font=("Segoe UI", 14),
                                                   background=self.app_config.alt_primary_color,
                                                   foreground=self.app_config.alt_secondary_color)
        self.language_from_combobox.pack(pady=5)

        self.language_to_label = ttk.Label(self.root, text="Выберите целевой язык", font=("Segoe UI", 14),
                                           background=self.app_config.primary_color,
                                           foreground=self.app_config.secondary_color)
        self.language_to_label.pack(pady=5)

        self.language_to_combobox = ttk.Combobox(self.root, values=[], font=("Segoe UI", 14),
                                                 background=self.app_config.alt_primary_color,
                                                 foreground=self.app_config.alt_secondary_color)
        self.language_to_combobox.pack(pady=5)

        self.word_entry_label = ttk.Label(self.root, text="Введите слово для перевода", font=("Segoe UI", 14),
                                          background=self.app_config.primary_color,
                                          foreground=self.app_config.secondary_color)
        self.word_entry_label.pack(pady=10)

        self.word_entry = ttk.Entry(self.root, font=("Segoe UI", 14),
                                    background=self.app_config.alt_primary_color,
                                    foreground=self.app_config.alt_secondary_color)
        self.word_entry.pack(pady=5)

        # Создаем кнопку с изображением
        self.translate_button = ttk.Button(self.root, text="Перевести", command=self.translate_word)
        self.app_config.configure_button(self.translate_button)
        self.translate_button.pack(pady=10)

        self.result_label = ttk.Label(self.root, text="", font=("Segoe UI", 14),
                                      background=self.app_config.primary_color,
                                      foreground=self.app_config.secondary_color)
        self.result_label.pack(pady=10)

        self.load_languages()

    def load_languages(self):
        """Загружает доступные языки для перевода из базы данных."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name_language FROM Language")
            languages = [row[0] for row in cursor.fetchall()]
            conn.close()

            if languages:
                self.language_from_combobox['values'] = languages
                self.language_to_combobox['values'] = languages
            else:
                MessageBox.show("В базе данных нет доступных языков!", "Ошибка",
                                master=self.root, app_config=self.app_config)
        except Exception as e:
            MessageBox.show(f"Не удалось загрузить языки: {e}", "Ошибка",
                            master=self.root, app_config=self.app_config)

    def translate_word(self):
        """Переводит слово с одного языка на другой."""
        word = self.word_entry.get().strip().lower()  # Приводим слово к нижнему регистру
        if not word:
            MessageBox.show("Введите слово для перевода!", "Ошибка",
                            master=self.root, app_config=self.app_config)
            return

        language_from = self.language_from_combobox.get()
        language_to = self.language_to_combobox.get()

        if not language_from or not language_to:
            MessageBox.show("Выберите оба языка!", "Ошибка",
                            master=self.root, app_config=self.app_config)
            return

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Получаем id языка исходного и целевого
            cursor.execute("SELECT id_language FROM Language WHERE name_language=?", (language_from,))
            language_from_id = cursor.fetchone()
            cursor.execute("SELECT id_language FROM Language WHERE name_language=?", (language_to,))
            language_to_id = cursor.fetchone()

            if not language_from_id or not language_to_id:
                MessageBox.show("Один из языков не найден!", "Ошибка",
                                master=self.root, app_config=self.app_config)
                return

            language_to_id = language_to_id[0]

            # Получаем id слова на исходном языке и приводим к нижнему регистру
            cursor.execute("SELECT id_word FROM Word WHERE LOWER(word)=?", (word,))  # Приводим слово из базы данных к нижнему регистру
            word_id = cursor.fetchone()

            if not word_id:
                MessageBox.show(f"Слово '{word}' не найдено в базе данных!", "Ошибка",
                                master=self.root, app_config=self.app_config)
                return

            word_id = word_id[0]

            # Получаем перевод для слова с одного языка на другой
            cursor.execute(''' 
                SELECT t.translation
                FROM Translation t
                WHERE t.word_id = ? AND t.language_id = ?
            ''', (word_id, language_to_id))

            result = cursor.fetchone()
            conn.close()

            if result:
                # Применяем str.capitalize() для результата перевода
                translated_word = result[0].capitalize()
                self.result_label.config(text=f"Перевод: {translated_word}")
            else:
                self.result_label.config(text="Перевод не найден.")

        except Exception as e:
            MessageBox.show(f"Ошибка при переводе: {e}", "Ошибка",
                            master=self.root, app_config=self.app_config)