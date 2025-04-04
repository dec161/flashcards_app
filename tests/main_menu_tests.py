import unittest
from unittest.mock import Mock, patch

from src.main_menu import MainMenu
from src.translator_app import TranslatorApp


class TestMainMenu(unittest.TestCase):
    def setUp(self):
        with (patch.object(TranslatorApp, "load_languages"),
              patch.object(MainMenu, "load_languages")):
            self.menu = MainMenu()

    def test_close_game(self):
        """Проверка закрытия игры"""
        self.menu.game = Mock()
        self.menu.game_window = Mock()

        self.menu.close_game()

        self.menu.game_window.withdraw.assert_called()
        self.menu.game.stop.assert_called()

    def test_open_game(self):
        """Проверка открытия игры"""
        self.menu.get_language = Mock(return_value="language")
        self.menu.game_window = Mock()
        mock = Mock()

        self.menu.open_game(Mock(return_value=mock))

        self.assertEqual(self.menu.game, mock)
        self.menu.game.set_language.assert_called_with("language")
        self.menu.game_window.protocol.assert_called_with("WM_DELETE_WINDOW", self.menu.close_game)
        self.menu.game_window.deiconify.assert_called()
        self.menu.game_window.lift.assert_called()

    def test_start_translator(self):
        """Проверка запуска переводчика"""
        self.menu.translator_window = Mock()

        self.menu.start_translator()

        self.menu.translator_window.deiconify.assert_called()
        self.menu.translator_window.lift.assert_called()


if __name__ == "__main__":
    unittest.main()
