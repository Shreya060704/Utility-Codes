import tkinter as tk
import random

# List of letters (A-Z) and their corresponding words
words = {
    "A": "Apple", "B": "Banana", "C": "Cat", "D": "Dog", "E": "Elephant",
    "F": "Fish", "G": "Giraffe", "H": "Horse", "I": "Ice", "J": "Juice",
    "K": "Kite", "L": "Lion", "M": "Monkey", "N": "Nest", "O": "Orange",
    "P": "Pineapple", "Q": "Queen", "R": "Rabbit", "S": "Snake", "T": "Tiger",
    "U": "Umbrella", "V": "Van", "W": "Whale", "X": "Xylophone", "Y": "Yacht", "Z": "Zebra"
}

class MemoryGame:
    def _init_(self, root):
        self.root = root
        self.root.title("Memory Game: Letters and Words")
        
        # Initialize game board
        self.game_board = self.initialize_game_board()
        self.hidden_board = [["_" for _ in range(5)] for _ in range(5)]
        self.buttons = []
        self.first_selection = None
        self.second_selection = None
        self.pairs_matched = 0
        
        # Create buttons for the board
        self.create_buttons()
        
        # Display instructions
        self.status_label = tk.Label(root, text="Select two cards to match a letter and word")
        self.status_label.grid(row=6, column=0, columnspan=5)

    def initialize_game_board(self):
        items = list(words.items())  # Convert dictionary into list of tuples (letter, word)
        random.shuffle(items)  # Shuffle to randomize their positions

        # Create a list containing both letters and words
        board_items = []
        for letter, word in items:
            board_items.append(letter)
            board_items.append(word)

        # Shuffle again to mix the letters and words
        random.shuffle(board_items)

        # Create a 5x5 game board
        board = []
        index = 0
        for i in range(5):
            row = []
            for j in range(5):
                row.append(board_items[index])
                index += 1
            board.append(row)

        return board

    def create_buttons(self):
        for i in range(5):
            button_row = []
            for j in range(5):
                button = tk.Button(self.root, text="?", width=10, height=3,
                                   command=lambda r=i, c=j: self.reveal_card(r, c))
                button.grid(row=i, column=j)
                button_row.append(button)
            self.buttons.append(button_row)

    def reveal_card(self, row, col):
        if self.first_selection is None:
            self.first_selection = (row, col)
            self.buttons[row][col].config(text=self.game_board[row][col], state="disabled")
        elif self.second_selection is None and self.first_selection != (row, col):
            self.second_selection = (row, col)
            self.buttons[row][col].config(text=self.game_board[row][col], state="disabled")
            
            # Check if the selected cards match (a letter and the corresponding word)
            self.root.after(1000, self.check_match)

    def check_match(self):
        row1, col1 = self.first_selection
        row2, col2 = self.second_selection

        item1 = self.game_board[row1][col1]
        item2 = self.game_board[row2][col2]
        
        if (item1 in words and item2 == words[item1]) or (item2 in words and item1 == words[item2]):
            self.status_label.config(text="It's a match!")
            self.pairs_matched += 1
            if self.pairs_matched == 13:
                self.status_label.config(text="Congratulations! You've matched all pairs!")
        else:
            self.status_label.config(text="Not a match. Try again!")
            self.buttons[row1][col1].config(text="?", state="normal")
            self.buttons[row2][col2].config(text="?", state="normal")

        self.first_selection = None
        self.second_selection = None

# Create the main window
root = tk.Tk()
game = MemoryGame(root)

# Start the GUI event loop
root.mainloop()
