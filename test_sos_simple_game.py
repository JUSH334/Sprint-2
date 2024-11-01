import unittest
from game_manager import GameManager

class TestSimpleGameMode(unittest.TestCase):
    
    def setUp(self):
        """Set up a new 3x3 Simple game for each test."""
        self.game_manager = GameManager(board_size=3, game_mode="Simple")
        self.game_manager.reset_game(3, "Simple")

    def test_simple_mode_win_with_first_sos(self):
        """Test that the game ends with a win as soon as the first SOS is created."""
        self.game_manager.make_move(0, 0, 'S')
        self.game_manager.make_move(0, 1, 'O')
        result = self.game_manager.make_move(0, 2, 'S')
        
        self.assertEqual(result["result"], "win")
        self.assertEqual(result["winner"], "Blue")

    def test_simple_mode_draw_when_board_filled_no_sos(self):
        """Test that the game ends in a draw if the board is filled without any SOS created."""
        moves = [
            (0, 0, 'S'), (0, 1, 'S'), (0, 2, 'O'),
            (1, 0, 'O'), (1, 1, 'O'), (1, 2, 'S'),
            (2, 0, 'S'), (2, 1, 'O'), (2, 2, 'S')
        ]
    
        for row, col, char in moves:
            self.game_manager.make_move(row, col, char)
    
        # Get the end game result after filling the board with no SOS
        result = self.game_manager.end_game()
    
        # Check that the result indicates a draw
        self.assertEqual(result["winner"], "Draw")





