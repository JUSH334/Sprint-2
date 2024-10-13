import unittest
from game_manager import GameManager

class TestGameManager(unittest.TestCase):
    
    # Test for User Story 4 - Make a Move in Simple Game
    def test_valid_simple_move(self):
        """Test that a valid move is correctly registered in a simple game."""
        game_manager = GameManager(board_size=3, game_mode="Simple")
        game_manager.reset_game(3, "Simple")
        
        # Place a valid move at (0,0) with "S"
        result = game_manager.make_move(0, 0, "S")
        
        # Check if the move was successfully made
        self.assertTrue(result)
        self.assertEqual(game_manager.get_board_value(0, 0), "S")

    def test_invalid_simple_move(self):
        """Test that placing a move in an occupied cell is rejected."""
        game_manager = GameManager(board_size=3, game_mode="Simple")
        game_manager.reset_game(3, "Simple")
        
        # Place a valid move at (0,0) with "S"
        game_manager.make_move(0, 0, "S")
        
        # Try placing a move in the same cell (0,0)
        result = game_manager.make_move(0, 0, "O")
        
        # Ensure the move is rejected
        self.assertFalse(result)

    # Test for User Story 6 - Make a Move in General Game
    def test_valid_general_move(self):
        """Test that a valid move is registered in a general game and turn switches."""
        game_manager = GameManager(board_size=5, game_mode="General")
        game_manager.reset_game(5, "General")
        
        # Place a valid move
        result = game_manager.make_move(0, 0, "S")
        
        # Ensure the move is valid
        self.assertTrue(result)
        self.assertEqual(game_manager.get_board_value(0, 0), "S")
        
        # Check that turn has switched to the other player
        game_manager.switch_turn()
        self.assertEqual(game_manager.get_current_player(), "Red")

if __name__ == '__main__':
    unittest.main()


