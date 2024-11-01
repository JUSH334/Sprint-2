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

    def test_no_sos_no_win(self):
        """Test that the game does not end if no SOS is created."""
        self.game_manager.make_move(0, 0, 'S')
        self.game_manager.make_move(0, 1, 'S')
        result = self.game_manager.make_move(0, 2, 'O')
        
        # Expect the game to continue with no winner
        self.assertEqual(result["result"], "next_turn")
        self.assertTrue(self.game_manager.is_game_active)
        
    def test_initial_game_state(self):
        """Test that the game initializes with an empty board and correct settings."""
        # Check that the board is empty at the start
        empty_board = [[' ' for _ in range(3)] for _ in range(3)]
        self.assertEqual(self.game_manager.board, empty_board)
        
        # Check that the game mode is set to Simple
        self.assertEqual(self.game_manager.game_mode, "Simple")
        
        # Check that the starting player is Blue
        self.assertEqual(self.game_manager.current_player, "Blue")
        
        # Check that the game is active after reset
        self.assertTrue(self.game_manager.is_game_active)





