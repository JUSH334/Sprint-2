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
        
        # Labels for SOS counts in General mode
        blue_count = self.game_manager.sos_count["Blue"]
        red_count = self.game_manager.sos_count["Red"]
            
        self.blue_sos_label = tk.Label(self.main_frame, text=f"Blue SOS Count:{blue_count}")
        self.blue_sos_label.grid(row=3, column=0, padx=5, pady=5)

        self.red_sos_label = tk.Label(self.main_frame, text=f"Red SOS Count: {red_count}")
        self.red_sos_label.grid(row=3, column=2, padx=5, pady=5)

    def create_scrollable_board_frame(self):
        """Create a scrollable frame for the game board."""
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.scrollbar_x = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=3, column=1, sticky="ew")

        self.scrollbar_y = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=1, column=3, sticky="ns")

        self.canvas.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

        self.board_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.board_frame, anchor="nw")

        self.board_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def setup_game_controls(self, parent):
        """Sets up game mode and board size selection."""
        label = tk.Label(parent, text="SOS")
        label.grid(row=0, column=0, padx=5, pady=1, sticky="w")

        self.radio_var = tk.StringVar(value="Simple Game")

        radio_frame = tk.Frame(parent)
        radio_frame.grid(row=0, column=1, padx=10, pady=1, sticky="w")

        tk.Radiobutton(radio_frame, text="Simple game", variable=self.radio_var, value="Simple Game").grid(row=0, column=0, padx=5, pady=1)
        tk.Radiobutton(radio_frame, text="General game", variable=self.radio_var, value="General Game").grid(row=0, column=1, padx=5, pady=1)

        board_size_label = tk.Label(parent, text="Board size")
        board_size_label.grid(row=0, column=2, padx=5, pady=1, sticky="w")

        self.board_size_var = tk.IntVar(value=3)
        vcmd = (self.root.register(self.validate_board_size), '%P')
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
        # Retrieve the game mode as selected by the user in the radio button ("Simple" or "General")
        selected_mode = self.radio_var.get().split()[0]  # "Simple" or "General"

        self.game_mode = selected_mode  # Update GUI�s game mode
        self.board_size = self.board_size_var.get()  # Get selected board size from spinbox
        
        print("Selected game mode:", self.game_mode)

        # Pass the selected game mode to the GameManager
        self.game_manager.reset_game(self.board_size, self.game_mode)

        # Adjust the window size and initialize the game board
        self.adjust_window_size(self.board_size)
        self.board = GameBoard(self.board_frame, self.board_size, self.on_board_click)
        self.board.create_board()
        
        initial_turn = self.game_manager.get_current_player()
        self.turn_label.config(text=f"Current turn: {initial_turn}")
        self.turn_label.grid()  # Show the turn label to start displaying turns


    def adjust_window_size(self, board_size):
        """Adjusts the window size based on the board size."""
        cell_size = 50
        board_pixel_size = board_size * cell_size
        max_window_size = 600

        if board_pixel_size > max_window_size:
            self.canvas.grid()
        else:
            self.root.geometry(f"{board_pixel_size + 600}x{board_pixel_size + 600}")

    def on_board_click(self, row, col):
        """Handles a click on the board."""
        if not self.game_manager.is_game_active:
            return

        current_player = self.game_manager.get_current_player()
        character_choice = self.blue_controls.choice.get() if current_player == "Blue" else self.red_controls.choice.get()

        move_result = self.game_manager.make_move(row, col, character_choice)

        if move_result:
            # Update the board visually
            self.board.update_button(row, col, character_choice)

            # Handle different results from make_move
            if move_result["result"] == "win":
                self.turn_label.config(text=f"{move_result['winner']} wins by creating the first SOS!")
                self.end_game()
            elif move_result["result"] == "continue":
                self.update_sos_count_display()
                self.turn_label.config(text=f"SOS! Current Turn: {current_player}")
            elif move_result["result"] == "draw":
                self.turn_label.config(text="The game is a draw! No SOS was created.")
                self.end_game()
            elif move_result["result"] == "end":
                winner = move_result["winner"]
                blue_score = move_result["blue_score"]
                red_score = move_result["red_score"]

                if winner == "Draw":
                    self.turn_label.config(text=f"The game is a draw! (Blue: {blue_score}, Red: {red_score})")
                else:
                    self.turn_label.config(text=f"{winner} wins! (Blue: {blue_score}, Red: {red_score})")
                self.end_game()
            else:
                # Switch to the next player if no SOS created
                self.game_manager.switch_turn()
                next_turn = self.game_manager.get_current_player()
                self.turn_label.config(text=f"Current turn: {next_turn}")


    def update_sos_count_display(self):
        """Updates the SOS count display for each player."""
        blue_count = self.game_manager.sos_count["Blue"]
        red_count = self.game_manager.sos_count["Red"]
        self.blue_sos_label.config(text=f"Blue SOS Count: {blue_count}")
        self.red_sos_label.config(text=f"Red SOS Count: {red_count}")

    def end_game(self):
        """Ends the game, disables all buttons, and clears the board."""
        self.is_game_active = False
        self.game_manager.end_game()

        self.board.disable_buttons()
        self.blue_controls.choice.set("S")
        self.red_controls.choice.set("S")
        self.board_frame.grid_remove()

def main():
    """Main function to run the Tkinter application."""
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    
