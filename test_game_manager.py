import unittest
from game_manager import GameManager

class TestGameManager(unittest.TestCase):

    def setUp(self):
        """Set up a new game before each test."""
        self.game_manager = GameManager(board_size=3, game_mode="Simple")

    def test_reset_game(self):
        """Test that the game resets correctly."""
        self.game_manager.reset_game(5, "General")
        self.assertEqual(self.game_manager.board_size, 5)
        self.assertEqual(self.game_manager.game_mode, "General")
        self.assertEqual(self.game_manager.current_player, "Blue")
        self.assertEqual(self.game_manager.is_game_active, True)
        # Check that the board is empty
        self.assertTrue(all(all(cell == ' ' for cell in row) for row in self.game_manager.board))

    def test_make_move_valid(self):
        """Test making a valid move."""
        self.game_manager.reset_game(3, "Simple")
        result = self.game_manager.make_move(0, 0, "S")
        self.assertTrue(result)
        self.assertEqual(self.game_manager.board[0][0], "S")

    def test_make_move_invalid(self):
        """Test making an invalid move (cell already occupied)."""
        self.game_manager.reset_game(3, "Simple")
        self.game_manager.make_move(0, 0, "S")
        result = self.game_manager.make_move(0, 0, "O")  # Invalid move
        self.assertFalse(result)  # Expecting False because the cell is already taken
        self.assertEqual(self.game_manager.board[0][0], "S")  # The original move stays

    def test_make_move_after_game_end(self):
        """Test making a move after the game has ended."""
        self.game_manager.reset_game(3, "Simple")
        self.game_manager.end_game()  # End the game
        result = self.game_manager.make_move(0, 0, "S")
        self.assertFalse(result)  # Expecting False because the game has ended
        self.assertEqual(self.game_manager.board[0][0], ' ')  # The move should not be placed

    def test_switch_turn(self):
        """Test that turns switch correctly between Blue and Red."""
        self.game_manager.reset_game(3, "Simple")
        self.assertEqual(self.game_manager.current_player, "Blue")
        self.game_manager.switch_turn()
        self.assertEqual(self.game_manager.current_player, "Red")
        self.game_manager.switch_turn()
        self.assertEqual(self.game_manager.current_player, "Blue")

    def test_check_board_filled(self):
        """Test that the board correctly detects when it is filled."""
        self.game_manager.reset_game(3, "Simple")
        # Fill the board
        for i in range(3):
            for j in range(3):
                self.game_manager.make_move(i, j, "S")

        self.assertTrue(self.game_manager.check_board_filled())  # Board should be filled

    def test_check_board_not_filled(self):
        """Test that the board correctly detects when it is not filled."""
        self.game_manager.reset_game(3, "Simple")
        self.game_manager.make_move(0, 0, "S")
        self.assertFalse(self.game_manager.check_board_filled())  # Board is not fully filled

    def test_end_game(self):
        """Test that the game ends and prevents further moves."""
        self.game_manager.reset_game(3, "Simple")
        self.game_manager.end_game()
        self.assertFalse(self.game_manager.is_game_active)
        result = self.game_manager.make_move(0, 0, "S")
        self.assertFalse(result)  # Expecting False because the game has ended

    def test_get_board_value_valid(self):
        """Test getting a valid board value."""
        self.game_manager.reset_game(3, "Simple")
        self.game_manager.make_move(0, 0, "S")
        self.assertEqual(self.game_manager.get_board_value(0, 0), "S")

    def test_get_board_value_invalid(self):
        """Test getting an invalid board value (out of bounds)."""
        self.game_manager.reset_game(3, "Simple")
        self.assertIsNone(self.game_manager.get_board_value(5, 5))  # Out of bounds

if __name__ == "__main__":
    unittest.main()




