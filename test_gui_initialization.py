import unittest
from tkinter import Tk
from sos_game_gui import SOSGameGUI

class TestSOSGameGUI(unittest.TestCase):
    
    # Test for User Story 1 - Choose a Board Size
    def test_valid_board_size_selection(self):
        """Test that a valid board size is correctly set."""
        root = Tk()
        app = SOSGameGUI(root)
        
        # Set board size to 10 (valid value)
        app.board_size_var.set(10)
        
        # Check if the internal board size is set to 10
        self.assertEqual(app.board_size_var.get(), 10)
        root.destroy()

    def test_invalid_board_size_selection(self):
        """Test that invalid board size is rejected."""
        root = Tk()
        app = SOSGameGUI(root)
        
        # Try to set board size to 25 (invalid value)
        app.board_size_var.set(25)
        is_valid = app.validate_board_size(str(app.board_size_var.get()))
        
        # Ensure the validation fails
        self.assertFalse(is_valid)
        root.destroy()
    
    # Test for User Story 2 - Choose the Game Mode
    def test_game_mode_selection(self):
        """Test that a valid game mode is correctly set."""
        root = Tk()
        app = SOSGameGUI(root)
        
        # Set game mode to "General Game"
        app.radio_var.set("General Game")
        
        # Check if the internal game mode is correctly set
        self.assertEqual(app.radio_var.get(), "General Game")
        root.destroy()

if __name__ == '__main__':
    unittest.main()





