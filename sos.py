import tkinter as tk
from game_manager import GameManager  # Assuming the GameManager class is in game_manager.py

class SOSGameGUI:
    """Handles the user interface for the SOS game."""

    def __init__(self, root):
        """Initializes the GUI elements of the application."""
        self.root = root
        self.root.title("SOS Application")

        # Set full-screen mode
        self.root.attributes('-fullscreen', True)

        # Initialize Game Manager
        self.board_size = 3  # Default board size is 3
        self.game_mode = "Simple"
        self.game_manager = GameManager(self.board_size, self.game_mode)

        # Game active flag
        self.is_game_active = False

        # Create the user interface
        self.create_ui()

    def create_ui(self):
        """Creates the UI components for the game."""
        # Main frame for layout
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10)

        # Top Frame: Game title, radio buttons for game mode, and board size spinbox
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=3)

        # Game Label Title
        self.label = tk.Label(self.top_frame, text="SOS")
        self.label.grid(row=0, column=0, padx=5, pady=1, sticky="w")

        # Radio Buttons for Game Mode Selection
        self.radio_var = tk.StringVar(value="Simple Game")
        self.radio_frame = tk.Frame(self.top_frame)
        self.radio_frame.grid(row=0, column=1, padx=10, pady=1, sticky="w")

        # Radio button for Simple Game
        self.radio_simple_game = tk.Radiobutton(
            self.radio_frame, text="Simple game", variable=self.radio_var, value="Simple Game"
        )
        self.radio_simple_game.grid(row=0, column=0, padx=5, pady=1)

        # Radio button for General Game
        self.radio_general_game = tk.Radiobutton(
            self.radio_frame, text="General game", variable=self.radio_var, value="General Game"
        )
        self.radio_general_game.grid(row=0, column=1, padx=5, pady=1)

        # Board Size Selection (Spinbox)
        self.board_size_label = tk.Label(self.top_frame, text="Board size")
        self.board_size_label.grid(row=0, column=2, padx=5, pady=1, sticky="w")

        self.board_size_var = tk.IntVar(value=3)  # Set initial board size to 3
        vcmd = (self.root.register(self.validate_board_size), '%P')
        self.board_size_spinbox = tk.Spinbox(
            self.top_frame, from_=3, to=20, textvariable=self.board_size_var, 
            validate="key", validatecommand=vcmd, width=3
        )
        self.board_size_spinbox.grid(row=0, column=3, padx=5, pady=1, sticky="w")

        # Left Frame: Blue Player options
        self.blue_frame = tk.Frame(self.main_frame)
        self.blue_frame.grid(row=1, column=0, padx=20, pady=10)
        self.blue_label = tk.Label(self.blue_frame, text="Blue player")
        self.blue_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Blue Player Selection: S or O
        self.blue_player_choice = tk.StringVar(value="S")  # Default to "S"
        self.p1_s_button = tk.Radiobutton(self.blue_frame, text="S", variable=self.blue_player_choice, value="S")
        self.p1_s_button.grid(row=1, column=0, padx=5, pady=5)

        self.p1_o_button = tk.Radiobutton(self.blue_frame, text="O", variable=self.blue_player_choice, value="O")
        self.p1_o_button.grid(row=2, column=0, padx=5, pady=5)

        # Right Frame: Red Player options
        self.red_frame = tk.Frame(self.main_frame)
        self.red_frame.grid(row=1, column=2, padx=20, pady=10)
        self.red_label = tk.Label(self.red_frame, text="Red player")
        self.red_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Red Player Selection: S or O
        self.red_player_choice = tk.StringVar(value="S")  # Default to "S"
        self.p2_s_button = tk.Radiobutton(self.red_frame, text="S", variable=self.red_player_choice, value="S")
        self.p2_s_button.grid(row=1, column=0, padx=5, pady=5)

        self.p2_o_button = tk.Radiobutton(self.red_frame, text="O", variable=self.red_player_choice, value="O")
        self.p2_o_button.grid(row=2, column=0, padx=5, pady=5)

        # Middle Frame: Game board (initially empty)
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.grid(row=1, column=1, padx=10, pady=10)

        # Bottom Frame: Start Game button and Current Turn label
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.grid(row=2, column=0, columnspan=3, pady=20)

        # Start Game button (which will later become End Game button)
        self.start_button = tk.Button(self.bottom_frame, text="Start Game", command=self.toggle_game)
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        # Current Turn label (hidden initially)
        self.turn_label = tk.Label(self.bottom_frame, text="Current turn: Blue")
        self.turn_label.grid(row=1, column=0)
        self.turn_label.grid_remove()  # Hide by default

        # Close Application button
        self.close_button = tk.Button(self.bottom_frame, text="Close Application", command=self.close_application)
        self.close_button.grid(row=0, column=1, padx=10, pady=5)


    def validate_board_size(self, new_value):
        """Validates the board size input in the Spinbox to ensure it is between 3 and 20."""
        if new_value.isdigit():
            value = int(new_value)
            if 3 <= value <= 20:
                return True
        return False

    def toggle_game(self):
        """Toggles between starting and ending the game."""
        if self.start_button["text"] == "Start Game":
            # Start the game
            self.start_game()
            self.start_button.config(text="End Game")
        else:
            # End the game
            self.end_game()
            self.start_button.config(text="Start Game")

    def start_game(self):
        """Initializes the game board and sets up for play."""
        self.is_game_active = True  # Game is active when started
        self.game_mode = self.radio_var.get().split()[0]  # "Simple" or "General"
        self.board_size = self.board_size_var.get()
    
        # Get the selected characters for each player
        blue_character = self.blue_player_choice.get()  # Get the Blue player's choice of "S" or "O"
        red_character = self.red_player_choice.get()  # Get the Red player's choice of "S" or "O"

        # Reset the game with the selected board size and game mode (no need to pass characters)
        self.game_manager.reset_game(self.board_size, self.game_mode)


        # Show player controls and current turn label
        self.blue_frame.grid()  # Show Blue Player controls
        self.red_frame.grid()  # Show Red Player controls
        self.turn_label.grid()  # Show turn label

        # Clear the board and create the game board dynamically based on the selected size
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.board_buttons = []
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                button = tk.Button(self.board_frame, text=' ', width=2, height=1,
                                   command=lambda r=i, c=j: self.on_board_click(r, c))
                button.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)


    def on_board_click(self, row, col):
        """Handles a click on the board."""
        if not self.game_manager.is_game_active:
            return  # Ignore clicks if the game is not active

        # Get the current player's choice of "S" or "O"
        current_player = self.game_manager.get_current_player()

        if current_player == "Blue":
            character_choice = self.blue_player_choice.get()  # Get Blue player's choice of "S" or "O"
        else:
            character_choice = self.red_player_choice.get()  # Get Red player's choice of "S" or "O"

        # Make the move using the chosen character
        if self.game_manager.make_move(row, col, character_choice):
            self.board_buttons[row][col].config(text=character_choice)
            self.game_manager.switch_turn()
            next_turn = self.game_manager.get_current_player()
            self.turn_label.config(text=f"Current turn: {next_turn}")


    def end_game(self):
        """Ends the game, disables all buttons, and clears the board."""
        self.is_game_active = False
        self.game_manager.end_game()

        # Disable all buttons on the board
        for row in self.board_buttons:
            for button in row:
                button.config(state="disabled")

        # Hide player controls and turn label
        self.blue_frame.grid_remove()
        self.red_frame.grid_remove()
        self.turn_label.grid_remove()

    def close_application(self):
        """Closes the application."""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()
