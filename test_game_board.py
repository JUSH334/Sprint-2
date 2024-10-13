import unittest
import tkinter as tk
from game_board import GameBoard

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()  # Create a Tkinter root for testing
        self.game_board = GameBoard(root, 3, lambda row, col: None)

    def test_create_board(self):
        """Test creating the board."""
        self.game_board.create_board()
        self.assertEqual(len(self.game_board.buttons), 3)  # 3 rows for 3x3 board
        self.assertEqual(len(self.game_board.buttons[0]), 3)  # 3 columns for each row

    def test_update_button(self):
        """Test updating a button on the board."""
        self.game_board.create_board()
        self.game_board.update_button(0, 0, "S")
        self.assertEqual(self.game_board.buttons[0][0].cget("text"), "S")

    def test_disable_buttons(self):
        """Test disabling all buttons on the board."""
        self.game_board.create_board()
        self.game_board.disable_buttons()
        for row in self.game_board.buttons:
            for button in row:
                self.assertEqual(button.cget("state"), "disabled")

if __name__ == "__main__":
    unittest.main()

