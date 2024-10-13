import unittest
from tkinter import Tk
from sos_game_gui import SOSGameGUI  # Assuming SOSGameGUI is in the file sos_game_gui.py

class TestSOSGameGUI(unittest.TestCase):
    
    def test_valid_board_size_selection(self):
        """Test that a valid board size is correctly set."""
        root = Tk()
        app = SOSGameGUI(root)
        
        # Set board size to 10 (valid value)
        app.board_size_var.set(10)
        
        # Check if the internal board size is set to 10
        self.assertEqual(app.board_size_var.get(), 10)
        root.destroy()

if __name__ == '__main__':
    unittest.main()
