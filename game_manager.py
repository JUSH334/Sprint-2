import tkinter as tk

class GameManager:
    """Manages the game state, player turns, and game logic for SOS."""

    def __init__(self, board_size=3, game_mode="Simple"):
        """Initializes the game manager with players, board, and game mode."""
        self.board_size = board_size
        self.game_mode = game_mode
        self.current_player = "Blue"  # Start with Blue player
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]  # Initialize empty board
        self.is_game_active = False  # Game active flag

    def reset_game(self, board_size, game_mode):
        """Resets the game with a new board size and game mode."""
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Blue"
        self.is_game_active = True

    def make_move(self, row, col, character):
        """Attempts to place the selected character on the board."""
        if self.board[row][col] != ' ' or not self.is_game_active:
            return False  # Invalid move
        self.board[row][col] = character  # Place the selected character
        return True

    def switch_turn(self):
        """Switches the turn between players."""
        if self.current_player == "Blue":
            self.current_player = "Red"
        else:
            self.current_player = "Blue"

    def get_current_player(self):
        """Returns the current player."""
        return self.current_player

    def get_board_value(self, row, col):
        """Returns the value at a specific position on the board."""
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row][col]
        return None

    def end_game(self):
        """Ends the current game by deactivating further moves."""
        self.is_game_active = False
