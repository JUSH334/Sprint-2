class GameManager:
    """Manages the game state, player turns, and game logic for SOS."""

    def __init__(self, board_size=3, game_mode="Simple"):
        """Initializes the game manager with players, board, and game mode."""
        self.board_size = board_size
        self.game_mode = game_mode
        self.current_player = "Blue"  # Start with Blue player
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]  # Initialize empty board
        self.is_game_active = False  # Game active flag
        self.sos_count = {"Blue": 0, "Red": 0}  # Track SOS counts for each player in General mode
        self.sos_occurred = False  # Track if any SOS has occurred

    def reset_game(self, board_size, game_mode):
        """Resets the game with a new board size and game mode."""
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Blue"
        self.is_game_active = True
        self.sos_count = {"Blue": 0, "Red": 0}  # Reset SOS counters for a new game
        self.sos_occurred = False  # Reset SOS tracker for a new game

    def is_board_full(self):
        """Checks if the entire board is filled."""
        for row in self.board:
            if ' ' in row:
                return False
        return True
    
    def make_move(self, row, col, character):
        """Attempts to place the selected character on the board, checks for SOS, and determines the game result."""
        if self.board[row][col] != ' ' or not self.is_game_active:
            return False  # Invalid move

        # Place the selected character
        self.board[row][col] = character
        sos_created = self.check_sos(row, col)

        # Check for Simple Game Mode win condition
        if self.game_mode == "Simple" and sos_created:
            self.is_game_active = False
            return {"result": "win", "winner": self.current_player}

        # General Game Mode: Update SOS count if an SOS is created
        if self.game_mode == "General" and sos_created:
            self.sos_count[self.current_player] += sos_created
            # Return "continue" to allow the player to take another turn
            return {"result": "continue"}

        # Check if board is full to determine end game result
        if self.is_board_full():
            blue_score = self.sos_count["Blue"]
            red_score = self.sos_count["Red"]

            if self.game_mode == "General":
                # Determine the winner based on SOS count
                if blue_score > red_score:
                    winner = "Blue"
                elif red_score > blue_score:
                    winner = "Red"
                else:
                    winner = "Draw"  # Both players have the same SOS count
                return {"result": "end", "winner": winner, "blue_score": blue_score, "red_score": red_score}
            else:
                # Simple Game mode - No SOS created, so it's a draw
                return {"result": "draw"}

        # Pass turn to the next player if no SOS created
        return {"result": "next_turn"}



    def switch_turn(self):
        """Switches the turn between players."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"

    def check_sos(self, row, col):
        """Checks if an SOS pattern is created at the given row and col."""
        sos_count = 0

        # Horizontal SOS (left-right)
        if col - 1 >= 0 and col + 1 < self.board_size:
            if self.board[row][col - 1] == 'S' and self.board[row][col] == 'O' and self.board[row][col + 1] == 'S':
                sos_count += 1
                return sos_count

        # Vertical SOS (up-down)
        if row - 1 >= 0 and row + 1 < self.board_size:
            if self.board[row - 1][col] == 'S' and self.board[row][col] == 'O' and self.board[row + 1][col] == 'S':
                sos_count += 1
                return sos_count
            
        # Diagonal SOS (top-left to bottom-right)
        if row - 1 >= 0 and col - 1 >= 0 and row + 1 < self.board_size and col + 1 < self.board_size:
            if self.board[row - 1][col - 1] == 'S' and self.board[row][col] == 'O' and self.board[row + 1][col + 1] == 'S':
                sos_count += 1
                return sos_count
            
        # Diagonal SOS (bottom-left to top-right)
        if row + 1 < self.board_size and col - 1 >= 0 and row - 1 >= 0 and col + 1 < self.board_size:
            if self.board[row + 1][col - 1] == 'S' and self.board[row][col] == 'O' and self.board[row - 1][col + 1] == 'S':
                sos_count += 1
                return sos_count
            
        # "OSO" pattern horizontally (left-right)
        if col - 2 >= 0:
            if self.board[row][col - 2] == 'S' and self.board[row][col - 1] == 'O' and self.board[row][col] == 'S':
                sos_count += 1
        if col + 2 < self.board_size:
            if self.board[row][col] == 'S' and self.board[row][col + 1] == 'O' and self.board[row][col + 2] == 'S':
                sos_count += 1
                return sos_count
            
        # "OSO" pattern vertically (up-down)
        if row - 2 >= 0:
            if self.board[row - 2][col] == 'S' and self.board[row - 1][col] == 'O' and self.board[row][col] == 'S':
                sos_count += 1
        if row + 2 < self.board_size:
            if self.board[row][col] == 'S' and self.board[row + 1][col] == 'O' and self.board[row + 2][col] == 'S':
                sos_count += 1
                return sos_count
            
        # "OSO" pattern diagonally (top-left to bottom-right)
        if row - 2 >= 0 and col - 2 >= 0:
            if self.board[row - 2][col - 2] == 'S' and self.board[row - 1][col - 1] == 'O' and self.board[row][col] == 'S':
                sos_count += 1
                return sos_count
            
        if row + 2 < self.board_size and col + 2 < self.board_size:
            if self.board[row][col] == 'S' and self.board[row + 1][col + 1] == 'O' and self.board[row + 2][col + 2] == 'S':
                sos_count += 1
                return sos_count
            
        # "OSO" pattern diagonally (bottom-left to top-right)
        if row + 2 < self.board_size and col - 2 >= 0:
            if self.board[row + 2][col - 2] == 'S' and self.board[row + 1][col - 1] == 'O' and self.board[row][col] == 'S':
                sos_count += 1
                return sos_count
            
        if row - 2 >= 0 and col + 2 < self.board_size:
            if self.board[row][col] == 'S' and self.board[row - 1][col + 1] == 'O' and self.board[row - 2][col + 2] == 'S':
                sos_count += 1
                return sos_count
          
        return sos_count

    def is_board_filled(self):
        """Checks if the entire board is filled."""
        for row in self.board:
            for cell in row:
                if cell == ' ':  # Found an empty cell
                    return False
        return True

    def end_game(self):
        """Ends the game by determining the winner based on game mode and returning the result."""
        self.is_game_active = False
        blue_score = self.sos_count["Blue"]
        red_score = self.sos_count["Red"]
        result = {"winner": None, "blue_score": blue_score, "red_score": red_score}

        if self.game_mode == "General" and self.is_board_full():
            # Determine the winner based on SOS count
            if blue_score > red_score:
                result["winner"] = "Blue"
            elif red_score > blue_score:
                result["winner"] = "Red"
            else:
                result["winner"] = "Draw"  # Both players have the same SOS count

        return result
    
    def get_current_player(self):
        """Returns the current player."""
        return self.current_player
