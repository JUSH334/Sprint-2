import unittest
from game_manager import GameManager

class TestGameManager(unittest.TestCase):

    def setUp(self):
        self.game_manager = GameManager(board_size=3, game_mode="Simple")

    def test_reset_game(self):
        """Test the reset_game function resets the board size and game mode."""
        self.game_manager.reset_game(5, "General")
        self.assertEqual(self.game_manager.board_size, 5)
        self.assertEqual(self.game_manager.game_mode, "General")
        self.assertTrue(self.game_manager.is_game_active)

    def test_make_move(self):
        """Test if a move is correctly placed on the board."""
        self.game_manager.reset_game(3, "Simple")
        self.assertTrue(self.game_manager.make_move(0, 0, "S"))
        self.assertEqual(self.game_manager.board[0][0], "S")
        self.assertFalse(self.game_manager.make_move(0, 0, "O"))  # Should fail, as the cell is already filled

    def test_switch_turn(self):
        """Test if the player turn is correctly switched."""
        self.game_manager.switch_turn()
        self.assertEqual(self.game_manager.current_player, "Red")
        self.game_manager.switch_turn()
        self.assertEqual(self.game_manager.current_player, "Blue")

    def test_get_current_player(self):
        """Test if the current player is returned correctly."""
        self.assertEqual(self.game_manager.get_current_player(), "Blue")
        self.game_manager.switch_turn()
        self.assertEqual(self.game_manager.get_current_player(), "Red")

    def test_is_board_filled(self):
        """Test if the is_board_filled method works properly."""
        # Initially, the board is empty, so it should return False
        self.assertFalse(self.game_manager.is_board_filled())

        # Fill up the board except for one space
        self.game_manager.board = [['S', 'O', 'S'],
                                   ['O', 'S', 'O'],
                                   ['S', 'O', ' ']]  # One space left
        self.assertFalse(self.game_manager.is_board_filled())

        # Fill the last space
        self.game_manager.board[2][2] = 'S'
        self.assertTrue(self.game_manager.is_board_filled())

    def test_get_board_value(self):
        """Test if the correct value is retrieved from the board."""
        self.game_manager.reset_game(3, "Simple")
        self.game_manager.make_move(0, 0, "S")
        self.assertEqual(self.game_manager.get_board_value(0, 0), "S")
        self.assertIsNone(self.game_manager.get_board_value(10, 10))  # Out of bounds should return None

    def test_end_game(self):
        """Test if the game ends properly by deactivating further moves."""
        self.game_manager.end_game()
        self.assertFalse(self.game_manager.is_game_active)

if __name__ == "__main__":
    unittest.main()

