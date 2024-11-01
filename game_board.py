import tkinter as tk

class GameBoard:
    """Manages the game board UI and interactions."""
    
    def __init__(self, parent, board_size, on_click_callback):
        self.parent = parent
        self.board_size = board_size
        self.on_click_callback = on_click_callback
        self.board_buttons = []
        self.create_board()

    def create_board(self):
        """Creates the game board dynamically."""
        # Clear any existing board elements
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.board_buttons = []
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                button = tk.Button(self.parent, text=' ', width=5, height=2,
                                   command=lambda r=i, c=j: self.on_click_callback(r, c))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)

    def update_button(self, row, col, text):
        """Updates a button at a specific position."""
        self.board_buttons[row][col].config(text=text)

    def disable_buttons(self):
        """Disables all buttons after the game ends."""
        if not self.board_buttons:
            return  # Exit if board_buttons is empty or not initialized

        for row in self.board_buttons:
            for button in row:
                try:
                    button.config(state="disabled")
                except tk.TclError:
                    # Button no longer exists, skip disabling
                    continue
