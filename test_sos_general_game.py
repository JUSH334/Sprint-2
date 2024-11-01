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

    def test_general_mode_end_game_with_sos_counts(self):
        """Test that the game ends with the player with the most SOS counts winning."""
        moves = [
            (0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'),  # Blue creates 1 SOS
            (1, 0, 'S'), (1, 1, 'O'), (1, 2, 'S'),  # Red creates 1 SOS
            (2, 0, 'S'), (2, 1, 'O'), (2, 2, 'S')   # Blue creates 1 more SOS
        ]
    
        for row, col, char in moves:
            self.game_manager.make_move(row, col, char)
    
        # Now get the game result to check SOS counts
        result = self.game_manager.end_game()
    
        # Expect Blue to have 2 SOSs and Red to have 1, making Blue the winner
        self.assertEqual(result["blue_score"], 2)
        self.assertEqual(result["red_score"], 1)
        self.assertEqual(result["winner"], "Blue")

    def test_general_mode_draw_with_equal_sos_counts(self):
        """Test that the game ends in a draw if both players have the same number of SOS sequences."""
        # Simulate moves to create equal SOS counts for both players
        moves = [
            (0, 0, 'S'), (0, 1, 'O'), (0, 2, 'S'),  # Blue creates 1 SOS
            (1, 0, 'S'), (1, 1, 'O'), (1, 2, 'S')   # Red creates 1 SOS
        ]
    
        for row, col, char in moves:
            self.game_manager.make_move(row, col, char)
    
        # Manually set equal sos_count for a controlled test case
        self.game_manager.sos_count["Blue"] = 1
        self.game_manager.sos_count["Red"] = 1
    
        # Call end_game() to get the final result
        result = self.game_manager.end_game()
    
        # Check that the result indicates a draw
        self.assertEqual(result["winner"], "Draw")


