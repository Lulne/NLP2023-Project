import sys
import pygame
import random
import string
import re


def create_check_button(screen, text):
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, 1, (10, 10, 10))
    text_rect = text_surface.get_rect(centerx=screen.get_width() // 2, centery=screen.get_height() - 20)
    button_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10)
    return button_rect, text_surface, text_rect


class WordSearch:
    def __init__(self, difficulty, input_method, input_data):
        self.difficulty = difficulty
        self.input_method = input_method
        self.input_data = input_data
        self.selected = []
        self.found_words = []
        self.completed_words = []
        self.correct_cells = set()

        self.words = []
        self.hints = []

        if self.input_method == "category":
            match self.input_data:
                case "Food":
                    self.words = ["apple", "banana", "cherry", "pepper", "watermelon", "lime", "lemon"]
                    self.hints = ["A popular red or green fruit, often associated with teachers",
                                  "A long, yellow tropical fruit, commonly used in smoothies",
                                  "A small, round, red stone fruit with a sweet taste",
                                  "A versatile vegetable that can be sweet or spicy, often used in cooking",
                                  "A large, green fruit with a refreshing taste and striped skin",
                                  "A small, green citrus fruit, often used in cocktails and Mexican cuisine",
                                  "A yellow citrus fruit, commonly used for its juice and zest in cooking and baking"]
                case "Nature":
                    self.words = ["sand", "dirt", "water", "tree", "sea", "plains", "plants"]
                    self.hints = ["A granular material commonly found on beaches and deserts",
                                  "Loose, unconsolidated soil often used in gardening and landscaping",
                                  "A colorless, odorless, and tasteless liquid essential for life on Earth",
                                  "A large, perennial plant with a trunk that supports branches and leaves",
                                  "A vast expanse of saltwater that covers about 71% of the Earth's surface",
                                  "Flat, expansive areas of land with few trees, often used for agriculture",
                                  "Multicellular, photosynthesizing organisms that form the base of many ecosystems"]
                case "Colors":
                    self.words = ["red", "blue", "green", "yellow", "pink", "orange"]
                    self.hints = ["The color of fire trucks and stop signs, often associated with passion",
                                  "A cool, calming color found in the sky and the ocean",
                                  "The color of grass and leaves, often associated with nature and growth",
                                  "A bright, cheerful color, associated with the sun and flowers like daffodils",
                                  "A delicate, light color often associated with romance and softness",
                                  "A vibrant color, the result of mixing red and yellow, associated with citrus fruits and sunsets"]
        else:
            for line in self.input_data.splitlines():
                word, hint = line.strip().split(',', 1)
                self.words.append(word.strip())
                self.hints.append(hint.strip())

        self.found_words = [False] * len(self.words)

    def is_game_won(self):
        return all(word == '' for word in self.words)

    def is_adjacent(self, row1, col1, row_col_tuple):
        row2, col2 = row_col_tuple
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1

    def check_word(self, screen):
        selected_word = ''.join([self.grid[row][col] for row, col in self.selected])
        if selected_word in self.words:
            word_index = self.words.index(selected_word)
            for row, col in self.selected:
                self.correct_cells.add((row, col))
            self.words[word_index] = ''
        self.selected = []
        self.draw_hints()

    def handle_click(self, pos):
        row, col = self.get_grid_position_from_mouse_position(pos)
        cell = (row, col)

        if not self.selected:
            if cell not in self.correct_cells:
                self.selected.append(cell)
        else:
            last_row, last_col = self.selected[-1]
            row_diff = abs(row - last_row)
            col_diff = abs(col - last_col)

            if ((row_diff == 1 and col_diff <= 1) or (col_diff == 1 and row_diff <= 1) or (
                    row_diff == 0 and col_diff == 1) or (
                        col_diff == 0 and row_diff == 1)) and cell not in self.selected and cell not in self.correct_cells:
                self.selected.append(cell)

    def generate_grid(self):
        grid_size = int(self.difficulty.split("x")[0])
        self.grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

        # Set the word list based on the input_data
        # self.words = re.split(r'[\s\n]+', self.input_data)
        # print(f"new words: {self.words}")

        for word in self.words:
            # print(word)
            placed = False
            while not placed:
                row, col = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
                direction = random.choice([(0, 1), (1, 0), (1, 1), (1, -1)])

                if self.can_place_word(row, col, word, direction):
                    for idx, letter in enumerate(word):
                        self.grid[row + idx * direction[0]][col + idx * direction[1]] = letter
                    placed = True

        for row in range(grid_size):
            for col in range(grid_size):
                if self.grid[row][col] == ' ':
                    self.grid[row][col] = random.choice(string.ascii_lowercase)

    def can_place_word(self, row, col, word, direction):
        grid_size = len(self.grid)
        for idx, letter in enumerate(word):
            r, c = row + idx * direction[0], col + idx * direction[1]
            if r < 0 or r >= grid_size or c < 0 or c >= grid_size:
                return False
            if self.grid[r][c] not in (' ', letter):
                return False
        return True

    def get_grid_position_from_mouse_position(self, pos):
        grid_size = int(self.difficulty.split("x")[0])
        cell_size = min(800 // grid_size, 600 // grid_size)
        col, row = pos[0] // cell_size, pos[1] // cell_size
        return row, col

    def draw_button(self, screen):
        button_width, button_height = 120, 40
        grid_size = int(self.difficulty.split("x")[0])
        cell_size = min(800 // grid_size, 600 // grid_size)
        button_x, button_y = (cell_size * grid_size - button_width) // 2, cell_size * grid_size + 20

        pygame.draw.rect(screen, (102, 153, 255), (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 24)
        text = font.render("Check Word", 1, (255, 255, 255))
        textpos = text.get_rect(centerx=button_x + button_width // 2, centery=button_y + button_height // 2)
        screen.blit(text, textpos)

    def draw_grid(self, screen):
        grid_size = len(self.grid)
        cell_size = min(800 // grid_size, 600 // grid_size)

        for row in range(grid_size):
            for col in range(grid_size):
                letter = self.grid[row][col]
                font = pygame.font.Font(None, 36)
                text = font.render(letter, 1, (10, 10, 10))
                textpos = text.get_rect(centerx=(col * cell_size + cell_size // 2),
                                        centery=(row * cell_size + cell_size // 2))

                # Check if the cell is selected or found, and set the appropriate background color
                if (row, col) in self.selected:
                    pygame.draw.rect(screen, (204, 204, 255), (col * cell_size, row * cell_size, cell_size, cell_size))
                elif (row, col) in self.found_words:
                    pygame.draw.rect(screen, (204, 255, 204), (col * cell_size, row * cell_size, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (col * cell_size, row * cell_size, cell_size, cell_size))

                screen.blit(text, textpos)
                pygame.draw.rect(screen, (10, 10, 10), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

    def draw_hints(self, screen):
        font = pygame.font.Font(None, 24)
        y_position = len(self.grid) * min(800 // len(self.grid), 600 // len(self.grid)) + 10
        for idx, hint in enumerate(self.hints):
            if self.words[idx] in self.completed_words:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

            text = font.render(hint, 1, color)
            textpos = text.get_rect(left=10, top=y_position)
            screen.blit(text, textpos)
            y_position += 30

    def start(self):
        pygame.init()

        grid_size = int(self.difficulty.split("x")[0])
        cell_size = min(800 // grid_size, 600 // grid_size)
        width, height = cell_size * grid_size, cell_size * grid_size + 60
        screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Word Search")
        clock = pygame.time.Clock()

        check_button, check_button_text, check_button_text_rect = create_check_button(screen, "Check Word")

        self.generate_grid()

        running = True
        while running:
            # TODO check for win
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if check_button.collidepoint(event.pos):
                        selected_word = ''.join([self.grid[row][col] for row, col in self.selected])
                        if selected_word in self.words:
                            self.found_words.extend(self.selected)
                            self.completed_words.append(selected_word)
                            self.selected = []
                        else:
                            self.selected = []
                    else:
                        row, col = self.get_grid_position_from_mouse_position(event.pos)
                        if (row, col) not in self.selected:
                            self.selected.append((row, col))
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                elif event.type == pygame.MOUSEMOTION:
                    pass

            screen.fill((255, 255, 255))
            self.draw_grid(screen)
            self.draw_hints(screen)

            # Draw the check button
            pygame.draw.rect(screen, (200, 200, 200), check_button)
            pygame.draw.rect(screen, (10, 10, 10), check_button, 2)
            screen.blit(check_button_text, check_button_text_rect)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    difficulty_arg = sys.argv[1]
    input_method_arg = sys.argv[2]
    input_data_arg = sys.argv[3]

    game = WordSearch(difficulty_arg, input_method_arg, input_data_arg)
    game.start()
