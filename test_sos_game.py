import unittest
import tkinter as tk
from sos_game import SOSGameGUI
from game_manager import GameManager

class TestSOSGameGUI(unittest.TestCase):

    def setUp(self):
        # Create a root window for the tests
        self.root = tk.Tk()
        self.app = SOSGameGUI(self.root)

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    def test_initial_setup(self):
        """Test if the initial setup of the GUI is correct."""
        # Check the default board size
        self.assertEqual(self.app.board_size, 3)

        # Check the game mode is set to Simple
        self.assertEqual(self.app.game_mode, "Simple")

        # Check if the game is inactive initially
        self.assertFalse(self.app.is_game_active)

    def test_start_game(self):
        """Test starting a game."""
        self.app.board_size_var.set(3)
        self.app.radio_var.set("Simple Game")
        self.app.start_game()

        # Check if the game is active after starting
        self.assertTrue(self.app.is_game_active)

        # Check if the board is created with the right number of buttons
        self.assertEqual(len(self.app.board.buttons), 3)  # 3 rows for 3x3 board
        self.assertEqual(len(self.app.board.buttons[0]), 3)  # 3 columns per row

        # Ensure the turn label is showing after the game starts
        self.assertTrue(self.app.turn_label.winfo_ismapped())

    def test_end_game(self):
        """Test ending a game."""
        self.app.start_game()
        self.app.end_game()

        # Check if the game is inactive after ending
        self.assertFalse(self.app.is_game_active)

        # Check if all buttons on the board are disabled
        for row in self.app.board.buttons:
            for button in row:
                self.assertEqual(button.cget("state"), "disabled")

        # Ensure the turn label is hidden after the game ends
        self.assertFalse(self.app.turn_label.winfo_ismapped())

    def test_toggle_game(self):
        """Test toggling the game between start and end."""
        self.assertEqual(self.app.start_button.cget("text"), "Start Game")
        self.app.toggle_game()
        self.assertEqual(self.app.start_button.cget("text"), "End Game")

        # Game should now be active
        self.assertTrue(self.app.is_game_active)

        # Toggle to end the game
        self.app.toggle_game()
        self.assertEqual(self.app.start_button.cget("text"), "Start Game")

        # Game should now be inactive
        self.assertFalse(self.app.is_game_active)

    def test_on_board_click(self):
        """Test clicking on the game board."""
        self.app.start_game()

        # Simulate clicking on an empty board cell
        self.app.on_board_click(0, 0)

        # Check if the button was updated correctly
        self.assertEqual(self.app.board.buttons[0][0].cget("text"), self.app.blue_controls.choice.get())

        # Check if the turn switched to Red after the move
        self.assertEqual(self.app.game_manager.get_current_player(), "Red")

    def test_validate_board_size(self):
        """Test board size validation."""
        self.assertTrue(self.app.validate_board_size("5"))  # Valid board size
        self.assertFalse(self.app.validate_board_size("22"))  # Invalid, out of bounds
        self.assertFalse(self.app.validate_board_size("abc"))  # Invalid, not a number

if __name__ == "__main__":
    unittest.main()

