import unittest
from game_manager import GameManager

class TestGeneralGameMode(unittest.TestCase):

    def setUp(self):
        """Set up a new 3x3 General game for each test."""
        self.game_manager = GameManager(board_size=3, game_mode="General")
        self.game_manager.reset_game(3, "General")

    def test_general_mode_sos_additional_turn(self):
        """Test that creating an SOS in General mode grants an extra turn."""
        self.game_manager.make_move(0, 0, 'S')
        self.game_manager.make_move(0, 1, 'O')
        result = self.game_manager.make_move(0, 2, 'S')

        self.assertEqual(result["result"], "continue")  # Indicates player gets an extra turn
        self.assertEqual(self.game_manager.sos_count["Blue"], 1)
        
    def test_no_sos_game_continues(self):
        """Test that the game continues if no SOS is created and the board is not full."""
        self.game_manager.make_move(0, 0, 'S')
        self.game_manager.make_move(0, 1, 'S')
        result = self.game_manager.make_move(0, 2, 'O')  # No SOS created here
        
        # Expect the game to continue with no winner and still active
        self.assertEqual(result["result"], "next_turn")
        self.assertTrue(self.game_manager.is_game_active)

    def test_initial_game_state_general_mode(self):
        """Test that the game initializes correctly for General mode with an empty board."""
        # Check that the board is empty at the start
        empty_board = [[' ' for _ in range(3)] for _ in range(3)]
        self.assertEqual(self.game_manager.board, empty_board)
        
        # Check that the game mode is set to General
        self.assertEqual(self.game_manager.game_mode, "General")
        
        # Check that the starting player is Blue
        self.assertEqual(self.game_manager.current_player, "Blue")
        
        # Check that the game is active after reset
        self.assertTrue(self.game_manager.is_game_active)
    