import pygame
import sys


# Hints for the words (replace with your own hints data)
hints = ["A small domesticated carnivorous mammal",
         "It is it",
         "bat"]

# Puzzle data (replace with your own crossword puzzle data)
puzzle = [
    ["c", "a", "t", None, None, None, "b"],
    [None, None, None, None, None, None, "a"],
    [None, None, None, None, None, None, "t"],
    [None, None, None, None, None, None, None],
    [None, "i", "t", None, None, None, None],
]

# Hidden words data (replace with your own words data)
words = ["cat", "it", "bat"]

# Word locations in the puzzle grid (replace with your own word locations)
word_locations = [
    {"word": "cat", "start": (0, 0), "end": (2, 0), "orientation": "horizontal",
     "hint": "A small domesticated carnivorous mammal"},
    {"word": "it", "start": (1, 4), "end": (2, 4), "orientation": "horizontal", "hint": "it is it"},
    {"word": "bat", "start": (6, 0), "end": (6, 2), "orientation": "horizontal", "hint": "it is bat"}

]


def RunCrossword(_words, _hints, _word_locations, _puzzle):
    class InputBox:
        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color_inactive = pygame.Color('lightskyblue3')
            self.color_active = pygame.Color('dodgerblue2')
            self.color = self.color_inactive
            self.text = text
            self.font = pygame.font.Font(None, 24)
            self.txt_surface = self.font.render(text, True, black)  # Set text color to black
            self.active = False

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        guess = self.text
                        self.text = ''
                        return guess
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.txt_surface = self.font.render(self.text, True, black)  # Set text color to black
            return None

        def draw(self, screen):
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)

    # Function to draw the grid
    def draw_grid():
        for y, row in enumerate(puzzle):
            for x, cell_value in enumerate(row):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if cell_value is None:
                    pygame.draw.rect(screen, black, rect)
                else:
                    pygame.draw.rect(screen, white, rect)
                    font = pygame.font.Font(None, 24)
                    number_font = pygame.font.Font(None, 16)
                    for i, word_data in enumerate(word_locations):
                        if (word_data["start"][1] <= y <= word_data["end"][1]) and (
                                word_data["start"][0] <= x <= word_data["end"][0]):
                            if revealed_words[i]:
                                if word_data["orientation"] == "horizontal":
                                    text = font.render(puzzle[y][x], True, black)
                                else:
                                    text = font.render(puzzle[y][x], True, black)
                                screen.blit(text, (x * cell_size + cell_size // 2 - text.get_width() // 2,
                                                   y * cell_size + cell_size // 2 - text.get_height() // 2))
                            if (word_data["start"][0] == x) and (word_data["start"][1] == y):
                                number_text = number_font.render(str(i + 1), True, black)
                                screen.blit(number_text, (x * cell_size + 2, y * cell_size + 2))

                pygame.draw.rect(screen, black, rect, 1)

    # Function to handle mouse events
    def on_mouse_click(pos):
        x, y = pos
        row, col = y // cell_size, x // cell_size

        if row < len(puzzle) and col < len(puzzle[row]) and puzzle[row][col] is not None:
            for i, word_data in enumerate(word_locations):
                if word_data["orientation"] == "horizontal":
                    if (word_data["start"][1] == row) and (word_data["start"][0] <= col <= word_data["end"][0]):
                        return i, word_data["word"], word_data["hint"]
                elif word_data["orientation"] == "vertical":
                    if (word_data["start"][0] == col) and (word_data["start"][1] <= row <= word_data["end"][1]):
                        return i, word_data["word"], word_data["hint"]
        return None, None, None

    # Function to handle keyboard input and check if the entered word is correct
    def handle_key_input(event, current_word, correct_word, word_index):
        if event.key == pygame.K_RETURN:
            if current_word == correct_word:
                print("Correct!")
                word_data = word_locations[word_index]
                start_x, start_y = word_data["start"]
                end_x, end_y = word_data["end"]
                if word_data["orientation"] == "horizontal":
                    for x in range(start_x, end_x + 1):
                        puzzle[start_y][x] = correct_word[x - start_x]
                    revealed_words[word_index] = True
                else:
                    for y in range(start_y, end_y + 1):
                        puzzle[y][start_x] = correct_word[y - start_y]
                    revealed_words[word_index] = True
                draw_grid()  # update the display after the word is revealed
            else:
                print("Incorrect!")
            current_word = ""
        elif event.key == pygame.K_BACKSPACE:
            current_word = current_word[:-1]
        else:
            current_word += event.unicode
        return current_word

    global revealed_words, words, hints, word_locations, puzzle
    words = _words
    hints = _hints
    word_locations = _word_locations
    puzzle = _puzzle
    revealed_words = [False] * len(words)

    # Initialize pygame
    pygame.init()

    # Screen settings
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Crossword Puzzle")

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Grid settings
    cell_size = 40
    grid_width = screen_width // cell_size
    grid_height = screen_height // cell_size



    input_box = InputBox(10, screen_height - 40, 140, 32)

    # Main game loop
    pygame.key.set_repeat(200, 50)  # Add this line after initializing pygame
    while True:
        screen.fill(white)
        draw_grid()
        input_box.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Update the input_box with the current event
            guess = input_box.handle_event(event)
            if guess is not None and selected_word is not None:
                if guess.lower() == selected_word.lower():
                    revealed_words[selected_word_index] = True
                else:
                    print("Incorrect guess:", guess)

            # Only call on_mouse_click() if the input field was not clicked
            if event.type == pygame.MOUSEBUTTONDOWN and not input_box.active:
                selected_word_index, selected_word, selected_hint = on_mouse_click(pygame.mouse.get_pos())
                print("Selected word index:", selected_word_index, "Selected word:", selected_word, "Selected hint:",
                      selected_hint)

        pygame.display.update()
