import tkinter as tk
from tkinter import ttk
import random
import sys
from tkinter import simpledialog


class BattleShipsGame:
    def __init__(self, ship_count, input_method, input_data):
        self.ship_count = int(ship_count)
        self.input_method = input_method
        self.input_data = input_data
        self.words = self.get_words()
        self.turn = 'blue'

        self.root = tk.Tk()
        self.root.title("Battleship Game")

        self.create_gui()

        self.root.mainloop()

    def get_words(self):
        # setup word list for premade categories
        if self.input_method == "category":
            match self.input_data:
                case "Food":
                    words_list = ["apple", "banana", "cherry", "pepper", "watermelon", "lime", "lemon"]
                case "Nature":
                    words_list = ["sand", "dirt", "water", "tree", "sea", "plains", "plants"]
                case "Colors":
                    words_list = ["red", "blue", "green", "yellow", "pink", "orange"]

        else:
            # Assuming input_data is a string containing words separated by newlines
            words_list = self.input_data.split('\n')
            random.shuffle(words_list)

        # Select random words for each team
        blue_words = words_list[:self.ship_count]
        red_words = words_list[self.ship_count:2 * self.ship_count]

        return {'blue': blue_words, 'red': red_words}

    def create_gui(self):
        self.turn_label = ttk.Label(self.root, text="Blue's Turn")
        self.turn_label.pack(pady=10)
        self.guess_entry = ttk.Entry(self.root)
        self.guess_entry.pack(pady=10)

        blue_panel = ttk.Frame(self.root)
        blue_panel.pack(side=tk.LEFT, padx=10)

        blue_label = ttk.Label(blue_panel, text="Blue Team", foreground='blue')
        blue_label.pack()

        red_panel = ttk.Frame(self.root)
        red_panel.pack(side=tk.RIGHT, padx=10)

        red_label = ttk.Label(red_panel, text="Red Team", foreground='red')
        red_label.pack()

        self.word_panels = {'blue': [], 'red': []}

        for team, panel in zip(['blue', 'red'], [blue_panel, red_panel]):
            for i in range(self.ship_count):
                word_panel = ttk.Label(panel, text="*" * len(self.words[team][i]), relief=tk.RAISED, padding=(5, 5))
                word_panel.pack(pady=5)
                self.word_panels[team].append(word_panel)

        self.selected_ship = (None, None)
        self.guess_button = ttk.Button(self.root, text="Enter Guess", command=self.submit_guess, state=tk.DISABLED)
        self.guess_button.pack(pady=10)

        self.root.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        clicked_widget = self.root.winfo_containing(event.x_root, event.y_root)

        for team, panels in self.word_panels.items():
            for i, panel in enumerate(panels):
                if clicked_widget == panel and self.turn != team:
                    # Deselect the previously selected ship
                    if self.selected_ship != (None, None):
                        prev_team, prev_index = self.selected_ship
                        self.word_panels[prev_team][prev_index].config(background="")

                    self.selected_ship = (team, i)
                    self.guess_button.config(state=tk.NORMAL)
                    panel.config(background="yellow")
                    return

    def submit_guess(self):
        if self.selected_ship == (None, None):
            return

        team, index = self.selected_ship
        word_to_guess = self.words[team][index]
        guess = self.guess_entry.get()

        if guess:
            guessed_correctly = (len(guess) == len(word_to_guess)) and (guess.lower() == word_to_guess.lower())
            partial_guess = ''.join([c if c == w else '*' for c, w in zip(guess, word_to_guess)]) + '*' * (
                    len(word_to_guess) - len(guess))

            if guessed_correctly:
                self.word_panels[team][index].config(text=word_to_guess)
            else:
                self.word_panels[team][index].config(text=partial_guess)

            # Check win condition
            if self.check_win_condition():
                self.turn_label.config(text=f"{self.turn.capitalize()} has won!")
                self.guess_button.config(state=tk.DISABLED)
            else:
                # Switch turns
                self.turn = 'red' if self.turn == 'blue' else 'blue'
                self.turn_label.config(text=f"{self.turn.capitalize()}'s Turn")

        self.selected_ship = (None, None)
        self.word_panels[team][index].config(background="")
        self.guess_button.config(state=tk.DISABLED)
        self.guess_entry.delete(0, tk.END)

    def check_win_condition(self):
        other_team = 'red' if self.turn == 'blue' else 'blue'
        return all(panel['text'] == word for panel, word in zip(self.word_panels[other_team], self.words[other_team]))


def main(ship_count, input_method, input_data):
    BattleShipsGame(ship_count, input_method, input_data)


if __name__ == "__main__":
    ship_count_arg = sys.argv[1]
    input_method_arg = sys.argv[2]
    input_data_arg = sys.argv[3]
    main(ship_count_arg, input_method_arg, input_data_arg)
