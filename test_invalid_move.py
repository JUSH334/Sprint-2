import unittest
from game_manager import GameManager  # Assuming GameManager is in the file game_manager.py

class TestGameManager(unittest.TestCase):
    
    def test_invalid_move(self):
        """Test that placing a move in an occupied cell is rejected."""
        game_manager = GameManager(board_size=3, game_mode="Simple")
        game_manager.reset_game(3, "Simple")
        
        # First move by the player in [0,0]
        game_manager.make_move(0, 0, "S")
        
        # Attempt to place another move in the same cell [0,0]
        result = game_manager.make_move(0, 0, "O")
        
        # Ensure the second move is rejected (result should be False)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
