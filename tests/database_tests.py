import sqlite3
import unittest

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        """Настроим тестовую базу данных перед каждым тестом."""
        self.db_name = ':memory:'  # Используем базу данных в памяти для тестов
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Создаем необходимые таблицы для теста
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Language (
                                id_language INTEGER PRIMARY KEY AUTOINCREMENT,
                                name_language TEXT UNIQUE)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Word (
                                id_word INTEGER PRIMARY KEY AUTOINCREMENT,
                                word TEXT UNIQUE)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WordTranslation (
                                id_translation INTEGER PRIMARY KEY AUTOINCREMENT,
                                word_id INTEGER,
                                language_id INTEGER,
                                translation TEXT,
                                is_correct INTEGER,
                                FOREIGN KEY (word_id) REFERENCES Word(id_word),
                                FOREIGN KEY (language_id) REFERENCES Language(id_language))''')

    def tearDown(self):
        """Закрываем соединение после каждого теста."""
        self.conn.close()

    def test_add_language(self):
        """Проверка добавления языков"""
        self.cursor.execute('INSERT INTO Language (name_language) VALUES (?)', ('Russian',))
        self.cursor.execute('SELECT name_language FROM Language WHERE name_language = ?', ('Russian',))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 'Russian')

    def test_add_word(self):
        """Проверка добавления слов"""
        self.cursor.execute('INSERT INTO Word (word) VALUES (?)', ('cat',))
        self.cursor.execute('SELECT word FROM Word WHERE word = ?', ('cat',))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 'cat')

    def test_add_translation(self):
        """Проверка добавления переводов"""
        # Добавляем язык и слово
        self.cursor.execute('INSERT INTO Language (name_language) VALUES (?)', ('English',))
        self.cursor.execute('INSERT INTO Word (word) VALUES (?)', ('cat',))
        self.cursor.execute('SELECT id_word FROM Word WHERE word = ?', ('cat',))
        word_id = self.cursor.fetchone()[0]
        self.cursor.execute('SELECT id_language FROM Language WHERE name_language = ?', ('English',))
        language_id = self.cursor.fetchone()[0]

        # Добавляем перевод
        self.cursor.execute('''INSERT INTO WordTranslation (word_id, language_id, translation, is_correct)
                               VALUES (?, ?, ?, ?)''', (word_id, language_id, 'cat', 1))

        # Проверка
        self.cursor.execute('''SELECT translation FROM WordTranslation WHERE word_id = ? AND language_id = ?''', (word_id, language_id))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 'cat')


if __name__ == "__main__":
    unittest.main()