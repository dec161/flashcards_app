import tkinter as tk
from tkinter import ttk
import sqlite3
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
from .app_config import AppConfig
from .message_box import MessageBox


# Функция для сохранения статистики в базу данных
def save_game_statistics(correct_answers, wrong_answers):
    try:
        conn = sqlite3.connect("dictionary.db")
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO GameStatistics (correct_answers, wrong_answers)
            VALUES (?, ?)
        ''', (correct_answers, wrong_answers))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка при сохранении статистики: {e}")


# Функция для отображения статистики в виде графика
def show_statistic_chart(app_config: AppConfig):
    try:
        conn = sqlite3.connect("dictionary.db")
        cursor = conn.cursor()

        # Извлекаем статистику по последним играм
        cursor.execute("SELECT * FROM GameStatistics ORDER BY date DESC LIMIT 10")
        stats = cursor.fetchall()

        conn.close()

        if not stats:
            MessageBox.show("Нет данных о результатах игр.", "Информация")
            return

        # Обработка данных для графика
        stats.sort(key=lambda x: x[3])  # Сортируем по столбцу date (индекс 3)

        dates = [stat[3] for stat in stats]
        correct_answers = [stat[1] for stat in stats]
        wrong_answers = [stat[2] for stat in stats]

        # Преобразуем даты в формат, который matplotlib сможет интерпретировать
        dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in dates]

        # Строим график
        fig, ax = plt.subplots(figsize=(12, 7))  # Увеличиваем размер графика

        ax.plot(dates, correct_answers, label='Правильные ответы', marker='o',
                color=app_config.answer_correct_color)
        ax.plot(dates, wrong_answers, label='Неправильные ответы', marker='x',
                color=app_config.answer_incorrect_color)

        ax.set_xlabel('Дата')
        ax.set_ylabel('Количество')
        ax.set_title('Статистика игры', color=app_config.graph_foreground)

        # Форматирование даты на оси X
        ax.set_xticks(dates)  # Устанавливаем метки оси X как даты
        ax.set_xticklabels([date.strftime('%d-%m-%Y %H:%M') for date in dates], rotation=45, ha="right")

        ax.legend()

        fig.set_facecolor(app_config.primary_color)
        ax.set_facecolor(app_config.primary_color)
        ax.xaxis.label.set_color(app_config.graph_foreground)
        ax.yaxis.label.set_color(app_config.graph_foreground)
        ax.tick_params(colors=app_config.graph_foreground, which="both")
        for spine in ax.spines.values():
            spine.set_color(app_config.graph_foreground)


        # Создаем новое окно для отображения статистики
        stats_window = tk.Toplevel()
        stats_window.title("Статистика игры")
        stats_window.geometry("1200x800")  # Увеличиваем окно для графика
        stats_window.config(bg=app_config.primary_color)

        # Устанавливаем прокрутку (для случаев, когда график выходит за пределы)
        canvas_frame = tk.Frame(stats_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        canvas_frame.config(bg=app_config.primary_color)


        chart = FigureCanvasTkAgg(fig, canvas_frame)
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=20)  # Расширяем пространство для графика
        chart.draw()

        # Кнопка для удаления статистики
        delete_button = ttk.Button(stats_window, text="Удалить статистику",
                                   command=lambda: delete_statistics(stats_window))
        app_config.configure_button(delete_button)
        delete_button.pack(pady=10)

    except Exception as e:
        print(f"Ошибка при загрузке статистики: {e}")


# Функция для удаления статистики из базы данных
def delete_statistics(window):
    try:
        conn = sqlite3.connect("dictionary.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM GameStatistics")
        conn.commit()
        conn.close()

        MessageBox.show("Статистика успешно удалена!", "Удаление")
        window.destroy()  # Закрыть окно статистики после удаления данных

    except Exception as e:
        MessageBox.show(f"Не удалось удалить статистику: {e}", "Ошибка")


# Главное окно приложения
class TimerFlashcardsApp:
    def __init__(self, root, app_config: AppConfig):
        self.app_config = app_config
        self.root = root
        self.root.title("Игра на время")
        self.root.geometry("1200x600")
        self.root.configure(bg=self.app_config.primary_color)
        self.root.protocol("WM_DELETE_WINDOW", self.root.withdraw)

        self.db_name = 'dictionary.db'  # Имя базы данных
        self.language = None
        self.words = []
        self.current_word = None
        self.correct_answers = 0
        self.wrong_answers = 0
        self.time_left = 30  # Таймер на 30 секунд

        # Стартовый фрейм
        self.flashcards_frame = tk.Frame(root, bg=self.app_config.primary_color)
        self.flashcards_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=30)

        self.title_label = ttk.Label(self.flashcards_frame, text="Игра на время", font=("Segoe UI", 28, "bold"),
                                     background=self.app_config.primary_color,
                                     foreground=self.app_config.secondary_color, anchor="center")
        self.title_label.pack(pady=20)

        self.start_button = ttk.Button(self.flashcards_frame, text="Начать игру", command=self.start_game,
                                       style="TButton")
        self.app_config.configure_button(self.start_button)
        self.start_button.pack(pady=10)

        self.word_label = ttk.Label(self.flashcards_frame, text="", font=("Segoe UI", 40, "bold"), anchor="center",
                                    background=self.app_config.primary_color,
                                    foreground=self.app_config.secondary_color)
        self.word_label.pack(pady=10)

        self.entry = ttk.Entry(self.flashcards_frame, font=("Segoe UI", 18), justify="center", width=20,
                               background=self.app_config.alt_primary_color,
                               foreground=self.app_config.alt_secondary_color)
        self.entry.pack(pady=10)

        self.check_button = ttk.Button(self.flashcards_frame, text="Проверить перевод", command=self.check_translation,
                                       style="TButton")
        self.app_config.configure_button(self.check_button)
        self.check_button.pack(pady=5)

        self.timer_label = ttk.Label(self.flashcards_frame, text="Осталось времени: 30", font=("Segoe UI", 16),
                                     background=self.app_config.primary_color,
                                     foreground=self.app_config.secondary_color)
        self.timer_label.pack(pady=10)

        self.message_label = ttk.Label(self.flashcards_frame, text="", font=("Segoe UI", 16), anchor="center",
                                       background=self.app_config.primary_color,
                                       foreground=self.app_config.secondary_color)
        self.message_label.pack(pady=10)

        self.stats_button = ttk.Button(self.flashcards_frame, text="Посмотреть\nстатистику",
                                       command=lambda: show_statistic_chart(self.app_config))
        self.app_config.configure_button(self.stats_button)
        self.stats_button.pack(pady=10)

        self.stats_label = ttk.Label(self.flashcards_frame, text="Правильно: 0 | Неправильно: 0", font=("Segoe UI", 14),
                                     background=self.app_config.primary_color,
                                     foreground=self.app_config.secondary_color)
        self.stats_label.pack(pady=10)

        self.timer = None

    def stop(self):
        if self.timer:
            self.root.after_cancel(self.timer)

        for child in self.root.winfo_children():
            child.destroy()

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

    def start_game(self):
        """Запускает игру после выбора языка."""
        self.correct_answers = 0
        self.wrong_answers = 0
        self.update_stats()
        self.show_word()
        self.start_timer()
        self.start_button.config(state=tk.DISABLED)

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
        """Проверяет правильность перевода и обновляет слово."""
        if not self.current_word:
            MessageBox.show("Сначала выберите слово!", "Ошибка",
                            master=self.root, app_config=self.app_config)
            return

        user_input = self.entry.get().strip().lower()
        correct_translation = self.current_word[0].lower()

        if user_input == correct_translation:
            self.message_label.config(text="Правильно!", foreground=self.app_config.answer_correct_color)
            self.correct_answers += 1
        else:
            self.message_label.config(
                text=f"Ошибка! Правильный перевод: {correct_translation}",
                foreground=self.app_config.answer_incorrect_color
            )
            self.wrong_answers += 1

        self.update_stats()
        self.show_word()  # Показываем следующее слово

    def update_stats(self):
        """Обновляет статистику на экране."""
        self.stats_label.config(
            text=f"Правильно: {self.correct_answers} | Неправильно: {self.wrong_answers}"
        )

    def start_timer(self):
        """Запускает таймер на 30 секунд."""
        self.time_left = 30
        self.update_timer()
        self.timer = self.root.after(1000, self.countdown)

    def update_timer(self):
        """Обновляет таймер на экране."""
        self.timer_label.config(text=f"Осталось времени: {self.time_left}")

    def countdown(self):
        """Отсчитывает время и завершает игру."""
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer()
            self.timer = self.root.after(1000, self.countdown)
        else:
            self.end_game()

    def end_game(self):
        """Завершает игру и сохраняет статистику."""
        save_game_statistics(self.correct_answers, self.wrong_answers)
        MessageBox.show(f"Игра завершена!\nПравильных ответов: {self.correct_answers}\nНеправильных ответов: {self.wrong_answers}", "Игра завершена",
                        master=self.root, app_config=self.app_config)
        self.show_word()
        self.start_button.config(state=tk.NORMAL)
