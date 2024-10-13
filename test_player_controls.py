import unittest
import tkinter as tk
from player_controls import PlayerControls

class TestPlayerControls(unittest.TestCase):
    
    def setUp(self):
        root = tk.Tk()  # Create a Tkinter root for testing
        self.player_controls = PlayerControls(root, "Blue")

    def test_initial_choice(self):
        """Test if the initial choice is set to 'S'."""
        self.assertEqual(self.player_controls.choice.get(), "S")  # Default should be "S"

    def test_change_choice(self):
        """Test if player choice can be changed."""
        self.player_controls.choice.set("O")
        self.assertEqual(self.player_controls.choice.get(), "O")

    def test_default_color(self):
        """Test the initial label color for Blue player."""
        self.assertEqual(self.player_controls.label.cget("fg"), "blue")

    def test_label_text(self):
        """Test if the label text is correctly set."""
        self.assertEqual(self.player_controls.label.cget("text"), "Blue Player")

if __name__ == "__main__":
    unittest.main()

