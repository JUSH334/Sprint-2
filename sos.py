import tkinter as tk
from tkinter import ttk
from game_manager import GameManager
from player_controls import PlayerControls
from game_board import GameBoard

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
        self.main_frame.grid(row=0, column=0, padx=20, pady=20)

        # Top Frame for mode and size selection
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Set up the game controls
        self.setup_game_controls(self.top_frame)

        # Player control frames
        self.blue_frame = tk.Frame(self.main_frame)
        self.blue_controls = PlayerControls(self.blue_frame, "Blue")
        self.blue_frame.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        self.red_frame = tk.Frame(self.main_frame)
        self.red_controls = PlayerControls(self.red_frame, "Red")
        self.red_frame.grid(row=1, column=2, padx=20, pady=10, sticky="n")

        # Create the Scrollable Board Frame
        self.create_scrollable_board_frame()

        # Bottom Frame for start/end game buttons
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.grid(row=2, column=0, columnspan=3, pady=20)

        self.setup_bottom_controls(self.bottom_frame)

    def create_scrollable_board_frame(self):
        """Create a scrollable frame for the game board."""
        # Create a canvas to hold the board
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        # Add scrollbars to the canvas
        self.scrollbar_x = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=3, column=1, sticky="ew")

        self.scrollbar_y = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=1, column=3, sticky="ns")

        # Configure the canvas to use the scrollbars
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

        # Create a frame inside the canvas to hold the board
        self.board_frame = tk.Frame(self.canvas)

        # Add the frame to the canvas using a window
        self.canvas.create_window((0, 0), window=self.board_frame, anchor="nw")

        # Update the scroll region to fit the frame
        self.board_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

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
        self.is_game_active = True
        self.game_mode = self.radio_var.get().split()[0]  # "Simple" or "General"
        self.board_size = self.board_size_var.get()

        # Clear any existing result label
        if hasattr(self, 'result_label') and self.result_label:
            self.result_label.destroy()
            self.result_label = None

        # Adjust the window size based on the board size and reset the game with the selected mode
        self.adjust_window_size(self.board_size)
        self.game_manager.reset_game(self.board_size, self.game_mode)

        # Initialize the GameBoard instance and create the board
        self.board = GameBoard(self.board_frame, self.board_size, self.on_board_click)
        self.board.create_board()

        # Show the turn label
        self.turn_label.grid()

    def adjust_window_size(self, board_size):
        """Adjusts the window size based on the board size."""
        # Define size per cell (button) in pixels
        cell_size = 50

        # Calculate desired window size
        board_pixel_size = board_size * cell_size

        # Set a threshold window size for scrollbars
        max_window_size = 600

        # If the board size exceeds the threshold, enable scrollbars and set window size to max
        if board_pixel_size > max_window_size:
            self.canvas.grid()
        else:
            # Resize window to fit the board perfectly without scrollbars
            self.root.geometry(f"{board_pixel_size + 200}x{board_pixel_size + 200}")  # +200 for padding and controls

    def end_game(self):
        """Ends the game, disables all buttons, and clears the board."""
        self.is_game_active = False
        self.game_manager.end_game()

        # Disable all buttons on the board
        self.board.disable_buttons()

        # Reset player choices (both players default to "S")
        self.blue_controls.choice.set("S")
        self.red_controls.choice.set("S")

        # Reset the turn label to indicate Blue player starts first
        self.turn_label.config(text="Current turn: Blue")

        # Hide the turn label and the board frame when the game ends
        self.turn_label.grid_remove()

    def on_board_click(self, row, col):
        """Handles a click on the board."""
        if not self.game_manager.is_game_active:
            return  # Ignore clicks if the game is not active

        current_player = self.game_manager.get_current_player()
        character_choice = self.blue_controls.choice.get() if current_player == "Blue" else self.red_controls.choice.get()

        # Make the move and check the result
        result = self.game_manager.make_move(row, col, character_choice)
        self.board.update_button(row, col, character_choice)

        # Handle the result based on the game mode
        if result == "Blue" or result == "Red":
            if self.game_mode == "Simple":
                self.show_game_result(f"{result} player wins!")
            else:  # General Game mode final result with scores
                self.show_game_result(f"{result} player wins with score: Blue {self.game_manager.blue_score} - Red {self.game_manager.red_score}")
        elif result == "Draw":
            self.show_game_result("The game is a draw!")
        elif result:
            # Continue to the next turn if game is still ongoing
            self.game_manager.switch_turn()
            next_turn = self.game_manager.get_current_player()
            self.turn_label.config(text=f"Current turn: {next_turn}")

    def show_game_result(self, message):
        """Displays the game result and disables the board."""
        # Check if a result label already exists, and if so, remove it
        if hasattr(self, 'result_label') and self.result_label:
            self.result_label.destroy()

        # Create a new result label and store it in an instance variable
        self.result_label = tk.Label(self.main_frame, text=message, font=("Arial", 14))
        self.result_label.grid(row=4, column=1, pady=10)

 
def main():
    """Main function to run the Tkinter application."""
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
