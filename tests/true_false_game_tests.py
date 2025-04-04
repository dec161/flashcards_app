import unittest
from unittest.mock import MagicMock, patch

import src.message_box
from src.True_False import TrueFalseGame  # Импортируем класс игры


class TestTrueFalseGame(unittest.TestCase):
    def setUp(self):
        """Настроим тестовую среду для игры."""
        self.root = MagicMock()
        self.app_config = MagicMock()  # Создаем поддельную конфигурацию
        self.game = TrueFalseGame(self.root, self.app_config)
        self.game.correct_answers = 0
        self.game.wrong_answers = 0

        # Подменяем stats_label для проверки вызова метода config
        self.game.stats_label = MagicMock()

    def test_check_answer_correct(self):
        """Проверка правильного ответа"""
        with patch.object(src.message_box.MessageBox, "show"):
            self.game.current_question = ("Слово 'cat' переводится как 'кошка'.", "Правда", "Ложь")
            self.game.check_answer(True)  # Игрок отвечает "Правда"
            self.assertEqual(self.game.correct_answers, 1)

    def test_check_answer_incorrect(self):
        """Проверка неправильного ответа"""
        with patch.object(src.message_box.MessageBox, "show"):
            self.game.current_question = ("Слово 'cat' переводится как 'кошка'.", "Правда", "Ложь")
            self.game.check_answer(False)  # Игрок отвечает "Ложь"
            self.assertEqual(self.game.wrong_answers, 1)

    def test_update_stats(self):
        """Проверка обновления статистики правильных и неправильных ответов"""
        self.game.correct_answers = 3
        self.game.wrong_answers = 2
        self.game.update_stats()

        # Проверяем, что метод config был вызван с правильным текстом
        self.game.stats_label.config.assert_called_with(text="Правильно: 3 | Неправильно: 2")


if __name__ == "__main__":
    unittest.main()
