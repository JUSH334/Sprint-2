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
        self.game_mode = game_mode  # Set the game mode based on player selection
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Blue"
        self.is_game_active = True
        self.blue_score = 0
        self.red_score = 0


    def make_move(self, row, col, character):
        """Attempts to place the selected character on the board and applies rules based on game mode."""
        if self.board[row][col] != ' ' or not self.is_game_active:
            return False  # Invalid move

        self.board[row][col] = character  # Place the selected character

        # Simple Game mode: check for winner after each move
        if self.game_mode == "Simple":
            if self.is_sos(row, col):
                self.is_game_active = False
                return self.current_player  # Return "Blue" or "Red" as the winner if an "SOS" is formed

        # General Game mode: check for SOS and count it, then end game if board is full
        elif self.game_mode == "General":
            if self.is_sos(row, col):
                if self.current_player == "Blue":
                    self.blue_score += 1
                else:
                    self.red_score += 1

            # Check if the board is filled up after the move
            if self.is_board_filled():
                self.is_game_active = False
                return self.determine_general_game_winner()

        return True  # Game continues


    def switch_turn(self):
        """Switches the turn between players."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"

    def get_current_player(self):
        """Returns the current player."""
        return self.current_player

    def get_board_value(self, row, col):
        """Returns the value at a specific position on the board."""
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row][col]
        return None

    def is_board_filled(self):
        """Checks if the entire board is filled."""
        for row in self.board:
            for cell in row:
                if cell == ' ':  # Found an empty cell
                    return False
        return True  # No empty cells found; board is full


    def end_game(self):
        """Ends the current game by deactivating further moves."""
        self.is_game_active = False
        
    def check_for_winner(self):
        """Determines if there is a winner based on the game mode."""
        if self.game_mode == "Simple":
            return self.check_simple_game_winner()
        elif self.game_mode == "General":
            return self.check_general_game_winner()
        return False
    
    def check_simple_game_winner(self):
        """Checks if the current player has formed an SOS in Simple mode."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_sos(row, col):
                    self.is_game_active = False
                    return self.current_player  # Return the winner (either "Blue" or "Red")
        return None  # No winner yet
    
    def is_sos(self, row, col):
        """Checks if there is an 'SOS' pattern centered around (row, col) and returns coordinates if found."""
        if self.get_board_value(row, col) == 'O':
            # Horizontal "SOS"
            if col > 0 and col < self.board_size - 1:
                if self.get_board_value(row, col - 1) == 'S' and self.get_board_value(row, col + 1) == 'S':
                    return (row, col - 1), (row, col + 1)
            # Vertical "SOS"
            if row > 0 and row < self.board_size - 1:
                if self.get_board_value(row - 1, col) == 'S' and self.get_board_value(row + 1, col) == 'S':
                    return (row - 1, col), (row + 1, col)
            # Diagonal "\" "SOS"
            if row > 0 and row < self.board_size - 1 and col > 0 and col < self.board_size - 1:
                if self.get_board_value(row - 1, col - 1) == 'S' and self.get_board_value(row + 1, col + 1) == 'S':
                    return (row - 1, col - 1), (row + 1, col + 1)
            # Diagonal "/" "SOS"
            if row > 0 and row < self.board_size - 1 and col > 0 and col < self.board_size - 1:
                if self.get_board_value(row - 1, col + 1) == 'S' and self.get_board_value(row + 1, col - 1) == 'S':
                    return (row - 1, col + 1), (row + 1, col - 1)
        return None

    def check_general_game_winner(self):
        """Checks if the game should end in General mode (when board is full)."""
        blue_score = self.calculate_sos_score("Blue")
        red_score = self.calculate_sos_score("Red")
    
        if self.is_board_filled():
            self.is_game_active = False
            if blue_score > red_score:
                return "Blue"
            elif red_score > blue_score:
                return "Red"
            return "Draw"
        return None  # Game is not over yet
    
    def calculate_sos_score(self, player):
        """Counts the number of SOS patterns for the given player."""
        score = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_sos(row, col) and self.get_board_value(row, col) == player:
                    score += 1
        return score
    
    def make_move(self, row, col, character):
        """Attempts to place the selected character on the board and checks for winner."""
        if self.board[row][col] != ' ' or not self.is_game_active:
            return False  # Invalid move

        self.board[row][col] = character  # Place the selected character

        # Check if there is a winner based on the current game mode
        winner = self.check_for_winner()
        if winner:
            self.is_game_active = False
            return winner  # Return "Blue" or "Red" as the winner

        # Check for a draw if the board is full and there's no winner
        if self.is_board_filled():
            self.is_game_active = False
            return "Draw"  # Return "Draw" if the board is full and no winner

        return True  # Game continues







