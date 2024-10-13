import unittest
from tkinter import Tk
from sos_game_gui import SOSGameGUI

class TestSOSGameGUI(unittest.TestCase):
    
    # Test for User Story 3 - Start a New Game
    def test_start_game(self):
        """Test starting a new game with valid board size and game mode."""
        root = Tk()
        app = SOSGameGUI(root)
        
        # Set board size and game mode
        app.board_size_var.set(5)
        app.radio_var.set("Simple Game")
        
        # Call the start_game method
        app.start_game()
        
        # Check that the game has been initialized with correct settings
        self.assertEqual(app.board_size, 5)
        self.assertEqual(app.game_mode, "Simple")
        root.destroy()

if __name__ == '__main__':
    unittest.main()





