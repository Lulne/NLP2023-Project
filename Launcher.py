import tkinter as tk
from tkinter import ttk, filedialog
import subprocess

selected_file_path = ""
def on_option_change(*args):
    option = selected_option.get()
    for widget in options_frame.winfo_children():
        widget.grid_forget()

    if option == 'Crossword':
        display_crossword_options()
    elif option == 'Word Search':
        display_word_search_options()
    elif option == 'Battleship':
        display_battleship_options()

    if option != 'Word Search':
        start_button_ws.grid_forget()
    if option != 'Crossword':
        start_button.grid_forget()
    if option != 'Battleship':
        start_button_bs.grid_forget()

def on_user_input_option_change(*args):
    user_input_option = user_input_options.get()
    category_dropdown.grid_forget()
    user_text_entry.grid_forget()
    file_upload_button.grid_forget()
    text_entry_label.grid_forget()

    if user_input_option == 'Predefined Category':
        category_dropdown.grid(row=2, column=0, pady=5)
    elif user_input_option == 'User Input':
        text_entry_label.grid(row=2, column=0, pady=5)
        user_text_entry.grid(row=3, column=0, pady=5)
    elif user_input_option == 'File Upload':
        file_upload_button.grid(row=2, column=0, pady=5)


def on_user_input_option_change_ws(*args):
    user_input_option_ws = user_input_options_ws.get()
    category_dropdown_ws.grid_forget()
    user_text_entry_ws.grid_forget()
    text_entry_label_ws.grid_forget()
    start_button.grid_forget()

    if user_input_option_ws == 'Predefined Category':
        category_dropdown_ws.grid(row=3, column=0, pady=5)
    elif user_input_option_ws == 'User Input':
        text_entry_label_ws.grid(row=3, column=0, pady=5)
        user_text_entry_ws.grid(row=4, column=0, pady=5)

    start_button.grid(row=5, column=0, pady=5)

def display_crossword_options():
    user_input_options.grid(row=0, column=0, pady=5)
    grid_size_dropdown.grid(row=1, column=0, pady=5)
    on_user_input_option_change()
    start_button.grid(row=4, column=0, pady=5)

def display_word_search_options():
    word_search_mode.grid(row=0, column=0, pady=5)
    on_word_search_mode_change()
    start_button_ws.grid(row=4, column=0, pady=5)

def display_battleship_options():
    ship_count_label.grid(row=0, column=0, pady=5)
    ship_count_dropdown.grid(row=1, column=0, pady=5)
    user_input_options_bs.grid(row=2, column=0, pady=5)
    on_user_input_option_change_bs()
    start_button_bs.grid(row=5, column=0, pady=5)

def on_word_search_mode_change(*args):
    word_search_mode_option = word_search_mode.get()
    difficulty_dropdown.grid_forget()
    category_dropdown_ws.grid_forget()
    file_upload_button_ws.grid_forget()
    user_input_options_ws.grid_forget()
    user_text_entry_ws.grid_forget()
    text_entry_label_ws.grid_forget()
    start_button.grid_forget()

    if word_search_mode_option == 'Generate':
        difficulty_dropdown.grid(row=1, column=0, pady=5)
        user_input_options_ws.grid(row=2, column=0, pady=5)
        on_user_input_option_change_ws()
    elif word_search_mode_option == 'Upload':
        file_upload_button_ws.grid(row=1, column=0, pady=5)
        start_button_ws.grid(row=2, column=0, pady=5)

def on_user_input_option_change_bs(*args):
    user_input_option_bs = user_input_options_bs.get()
    category_dropdown_bs.grid_forget()
    user_text_entry_bs.grid_forget()
    text_entry_label_bs.grid_forget()
    file_upload_button_bs.grid_forget()

    if user_input_option_bs == 'Predefined Category':
        category_dropdown_bs.grid(row=3, column=0, pady=5)
    elif user_input_option_bs == 'User Input':
        text_entry_label_bs.grid(row=3, column=0, pady=5)
        user_text_entry_bs.grid(row=4, column=0, pady=5)
    elif user_input_option_bs == 'File Upload':
        file_upload_button_bs.grid(row=3, column=0, pady=5)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    print(file_path)
def open_file_bs():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    print(selected_file_path)

def open_file_ws():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    print(selected_file_path)
def insert_newline(event):
    user_text_entry.insert(tk.INSERT, '\n')


def start_word_search_game():
    word_search_mode_option = word_search_mode.get()
    user_input_option_ws = user_input_options_ws.get()

    if word_search_mode_option == 'Generate':
        if user_input_option_ws == 'User Input':
            input_method = 'user_input'
            input_data = user_text_entry_ws.get(1.0, tk.END).strip()
        else:  # Predefined Category
            input_method = 'category'
            input_data = category_dropdown_ws.get()
    else:  # Upload mode
        input_method = 'file_upload'
        with open(selected_file_path, 'r') as file:
            input_data = file.read()

    difficulty = difficulty_dropdown.get()
    subprocess.run(['python', 'WordSearch.py', difficulty, input_method, input_data], check=True)

def start_battleship_game():
    global game_started
    game_started = True
    ship_count = ship_count_dropdown.get()
    user_input_option_bs = user_input_options_bs.get()

    if user_input_option_bs == 'User Input':
        input_method = 'user_input'
        input_data = user_text_entry_bs.get(1.0, tk.END).strip()
    elif user_input_option_bs == 'File Upload':
        input_method = 'file_upload'
        with open(selected_file_path, 'r') as file:
            input_data = file.read()
    else:  # Predefined Category
        input_method = 'category'
        input_data = category_dropdown_bs.get()

    subprocess.Popen(['python', 'BattleShips.py', ship_count, input_method, input_data])

    # Close the launcher GUI
    root.destroy()

root = tk.Tk()
root.title("Game Selection")

selected_option = tk.StringVar(value="Crossword")

main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, padx=10, pady=10)

options_frame = ttk.Frame(root)
options_frame.grid(row=0, column=1, padx=10, pady=10)

game_options = ['Crossword', 'Word Search', 'Battleship']
for index, option in enumerate(game_options):
    ttk.Radiobutton(main_frame, text=option, variable=selected_option, value=option, command=on_option_change).grid(row=index, column=0, sticky=tk.W, pady=5)

user_input_options = ttk.Combobox(options_frame, values=["User Input", "Predefined Category", "File Upload"], state="readonly", width=20)
user_input_options.current(0)
user_input_options.bind("<<ComboboxSelected>>", on_user_input_option_change)

user_input_options_ws = ttk.Combobox(options_frame, values=["User Input", "Predefined Category"], state="readonly", width=20)
user_input_options_ws.current(0)
user_input_options_ws.bind("<<ComboboxSelected>>", on_user_input_option_change_ws)

text_entry_label_ws = ttk.Label(options_frame, text="Word input format: word, hint")
user_text_entry_ws = tk.Text(options_frame, width=30, height=10, wrap=tk.WORD)
user_text_entry_ws.bind('<space>', insert_newline)

grid_size_dropdown = ttk.Combobox(options_frame, values=[f"{x}x{x}" for x in range(5, 21)], state="readonly", width=20)
grid_size_dropdown.current(0)

category_dropdown = ttk.Combobox(options_frame, values=["Food", "Nature", "Colors"], state="readonly", width=20)
category_dropdown.current(0)

text_entry_label = ttk.Label(options_frame, text="Text entry: format as word, hint")
user_text_entry = tk.Text(options_frame, width=30, height=10, wrap=tk.WORD)
user_text_entry.bind('<space>', insert_newline)

file_upload_button = ttk.Button(options_frame, text="Upload .txt File", command=open_file)
file_upload_button_bs = ttk.Button(options_frame, text="Upload .txt File", command=open_file_bs)

start_button = ttk.Button(options_frame, text="Start", command=lambda: print("Game started"))
start_button_bs = ttk.Button(options_frame, text="Start", command=start_battleship_game)
start_button_ws = ttk.Button(options_frame, text="Start", command=start_word_search_game)

word_search_mode = ttk.Combobox(options_frame, values=["Generate", "Upload"], state="readonly", width=20)
word_search_mode.current(0)
word_search_mode.bind("<<ComboboxSelected>>", on_word_search_mode_change)

difficulty_dropdown = ttk.Combobox(options_frame, values=["10x10", "25x25", "50x50", "100x100"], state="readonly", width=20)
difficulty_dropdown.current(0)

category_dropdown_ws = ttk.Combobox(options_frame, values=["Food", "Nature", "Colors"], state="readonly", width=20)
category_dropdown_ws.current(0)

num_words_dropdown = ttk.Combobox(options_frame, values=list(range(1, 51)), state="readonly", width=20)
num_words_dropdown.current(4)

file_upload_button_ws = ttk.Button(options_frame, text="Upload .txt File", command=open_file_ws)

ship_count_label = ttk.Label(options_frame, text="Ship Count")
ship_count_dropdown = ttk.Combobox(options_frame, values=list(range(1, 6)), state="readonly", width=20)
ship_count_dropdown.current(0)

user_input_options_bs = ttk.Combobox(options_frame, values=["User Input", "Predefined Category", "File Upload"], state="readonly", width=20)
user_input_options_bs.current(0)
user_input_options_bs.bind("<<ComboboxSelected>>", on_user_input_option_change_bs)

category_dropdown_bs = ttk.Combobox(options_frame, values=["Food", "Nature", "Colors"], state="readonly", width=20)
category_dropdown_bs.current(0)

text_entry_label_bs = ttk.Label(options_frame, text="Word input format: one word per line")
user_text_entry_bs = tk.Text(options_frame, width=30, height=10, wrap=tk.WORD)
user_text_entry_bs.bind('<space>', insert_newline)

on_option_change()
root.mainloop()