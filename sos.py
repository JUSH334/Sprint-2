import tkinter as tk
from game_manager import GameManager 
from PlayerControls import PlayerControls  
from GameBoard import GameBoard

class SOSGameGUI:
    """Handles the user interface for the SOS game."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Application")

        # Initialize Game Manager
        self.board_size = 3
        self.game_mode = "Simple"
        self.game_manager = GameManager(self.board_size, self.game_mode)

        # Game active flag
        self.is_game_active = False

        # Create the main UI structure
        self.create_ui()

    def create_ui(self):
        """Sets up the main layout for the game."""
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)  # Added padding

        # Top Frame for mode and size selection
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Set up the game controls
        self.setup_game_controls(self.top_frame)

        # Player control frames
        self.blue_frame = tk.Frame(self.main_frame)
        self.blue_controls = PlayerControls(self.blue_frame, "Blue")
        self.blue_frame.grid(row=1, column=0, padx=20, pady=10)

        self.red_frame = tk.Frame(self.main_frame)
        self.red_controls = PlayerControls(self.red_frame, "Red")
        self.red_frame.grid(row=1, column=2, padx=20, pady=10)

        # Board Frame (Game board) - Initially hidden
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.grid(row=1, column=1, padx=20, pady=10)
        self.board_frame.grid_remove()  # Hide the board frame initially
        self.board = GameBoard(self.board_frame, self.board_size, self.on_board_click)

        # Bottom Frame for start/end game and close buttons
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.grid(row=2, column=0, columnspan=3, pady=20)

        self.setup_bottom_controls(self.bottom_frame)

    def setup_game_controls(self, parent):
        """Sets up game mode and board size selection."""
        label = tk.Label(parent, text="SOS")
        label.grid(row=0, column=0, padx=5, pady=1, sticky="w")

        # Initialize the radio button variable for game mode selection
        self.radio_var = tk.StringVar(value="Simple Game")

        # Create a frame for radio buttons (game mode selection)
        radio_frame = tk.Frame(parent)
        radio_frame.grid(row=0, column=1, padx=10, pady=1, sticky="w")

        # Simple Game Radio Button
        tk.Radiobutton(radio_frame, text="Simple game", variable=self.radio_var, value="Simple Game").grid(row=0, column=0, padx=5, pady=1)

        # General Game Radio Button
        tk.Radiobutton(radio_frame, text="General game", variable=self.radio_var, value="General Game").grid(row=0, column=1, padx=5, pady=1)

        # Board size label
        board_size_label = tk.Label(parent, text="Board size")
        board_size_label.grid(row=0, column=2, padx=5, pady=1, sticky="w")

        # Initialize the Spinbox for board size selection
        self.board_size_var = tk.IntVar(value=3)
        
        # Validate command for the board size Spinbox
        vcmd = (self.root.register(self.validate_board_size), '%P')

        # Spinbox for selecting board size (from 3 to 20)
        self.board_size_spinbox = tk.Spinbox(parent, from_=3, to=20, textvariable=self.board_size_var, 
                                             validate="key", validatecommand=vcmd, width=3)
        self.board_size_spinbox.grid(row=0, column=3, padx=5, pady=1, sticky="w")

    def setup_bottom_controls(self, parent):
        """Sets up the bottom controls like Start/End game buttons."""
        self.start_button = tk.Button(parent, text="Start Game", command=self.toggle_game)
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        self.turn_label = tk.Label(parent, text="Current turn: Blue")
        self.turn_label.grid(row=1, column=0)
        self.turn_label.grid_remove()

        self.close_button = tk.Button(parent, text="Close Application", command=self.close_application)
        self.close_button.grid(row=0, column=1, padx=10, pady=5)

    def validate_board_size(self, new_value):
        """Validates the board size input in the Spinbox to ensure it is between 3 and 20."""
        if new_value.isdigit():
            value = int(new_value)
            return 3 <= value <= 20
        return False

    def toggle_game(self):
        """Toggles between starting and ending the game."""
        if self.start_button["text"] == "Start Game":
            self.start_game()
            self.start_button.config(text="End Game")
        else:
            self.end_game()
            self.start_button.config(text="Start Game")

    def start_game(self):
        """Initializes the game board and sets up for play."""
        self.is_game_active = True  # Game is active when started
        self.game_mode = self.radio_var.get().split()[0]  # "Simple" or "General"
        self.board_size = self.board_size_var.get()

        # Reset the game with the selected board size and game mode
        self.game_manager.reset_game(self.board_size, self.game_mode)

        # Show the board and prepare for play
        self.board.board_size = self.board_size  # Update board size in GameBoard instance
        self.board_frame.grid()  # Show the board frame when the game starts
        self.board.create_board()  # Recreate the board with the new size
        self.turn_label.grid()  # Show turn label

    def on_board_click(self, row, col):
        """Handles a click on the board."""
        if not self.game_manager.is_game_active:
            return  # Ignore clicks if the game is not active

        # Get the current player's choice of "S" or "O"
        current_player = self.game_manager.get_current_player()
        character_choice = self.blue_controls.choice.get() if current_player == "Blue" else self.red_controls.choice.get()

        # Make the move using the chosen character
        if self.game_manager.make_move(row, col, character_choice):
            self.board.update_button(row, col, character_choice)

            # Switch turns after a valid move
            self.game_manager.switch_turn()
            next_turn = self.game_manager.get_current_player()
            self.turn_label.config(text=f"Current turn: {next_turn}")

    def end_game(self):
        """Ends the game, disables all buttons, and clears the board."""
        self.is_game_active = False
        self.game_manager.end_game()

        # Disable all buttons on the board
        self.board.disable_buttons()

        # Hide the turn label and the board frame when the game ends
        self.turn_label.grid_remove()
        self.board_frame.grid_remove()

    def close_application(self):
        """Closes the application."""
        self.root.destroy()


def main():
    """Main function to run the Tkinter application."""
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
