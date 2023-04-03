import random
import itertools


class CrosswordGenerator:
    def __init__(self, words, grid_size, hint_list):
        self.words = words
        self.grid_size = grid_size
        self.hints = hint_list
        self.word_locations = []
        self.grid = [[None] * grid_size for _ in range(grid_size)]

    def is_valid_intersection(self, x, y, letter, direction):
        adjacent_cells = {
            'horizontal': [(x, y - 1), (x, y + 1)],
            'vertical': [(x - 1, y), (x + 1, y)],
        }

        # Check for invalid adjacent cells in the word's direction
        for adj_x, adj_y in adjacent_cells[direction]:
            if 0 <= adj_x < self.grid_size and 0 <= adj_y < self.grid_size:
                if self.grid[adj_y][adj_x] not in (None, letter):
                    return False

        # Check for invalid adjacent cells in the opposite direction
        opp_direction = 'vertical' if direction == 'horizontal' else 'horizontal'
        opp_adjacent_cells = adjacent_cells[opp_direction]
        for i in range(-1, 2):
            if direction == 'horizontal':
                adj_x, adj_y = x + i, y
            else:
                adj_x, adj_y = x, y + i

            if 0 <= adj_x < self.grid_size and 0 <= adj_y < self.grid_size:
                if self.grid[adj_y][adj_x] not in (None, letter) and (adj_x, adj_y) not in opp_adjacent_cells:
                    return False

        return True

    def find_intersections(self, word):
        intersections = []
        for other_word in self.words:
            if word != other_word:
                common_letters = set(word) & set(other_word)
                for letter in common_letters:
                    word_indices = [i for i, c in enumerate(word) if c == letter]
                    other_word_indices = [i for i, c in enumerate(other_word) if c == letter]
                    for w_idx, o_idx in itertools.product(word_indices, other_word_indices):
                        intersections.append((word, other_word, letter, w_idx, o_idx))
        return intersections

    def place_word(self, word, x, y, direction):
        if direction == 'horizontal':
            for i, letter in enumerate(word):
                self.grid[y][x + i] = letter
        elif direction == 'vertical':
            for i, letter in enumerate(word):
                self.grid[y + i][x] = letter

    def can_place_word(self, word, x, y, direction):
        if direction == 'horizontal':
            if x < 0 or x + len(word) > self.grid_size:
                return False
            for i, letter in enumerate(word):
                if 0 <= x + i < self.grid_size and 0 <= y < self.grid_size:
                    if self.grid[y][x + i] not in (None, letter):
                        return False
                    if not self.is_valid_intersection(x + i, y, letter, direction):
                        return False
                else:
                    return False
        elif direction == 'vertical':
            if y < 0 or y + len(word) > self.grid_size:
                return False
            for i, letter in enumerate(word):
                if 0 <= x < self.grid_size and 0 <= y + i < self.grid_size:
                    if self.grid[y + i][x] not in (None, letter):
                        return False
                    if not self.is_valid_intersection(x, y + i, letter, direction):
                        return False
                else:
                    return False
        return True

    def generate_crossword(self):
        placed_words = {}
        word_locations = []  # Store word location information

        # Sort the words by length
        sorted_words = sorted(self.words, key=len, reverse=True)

        # Place the first word in the center of the grid
        first_word = sorted_words[0]
        first_x = (self.grid_size - len(first_word)) // 2
        first_y = self.grid_size // 2
        self.place_word(first_word, first_x, first_y, 'horizontal')
        placed_words[first_word] = {'horizontal': (first_x, first_y)}

        first_word_index = self.words.index(first_word)
        first_word_hint = self.hints[first_word_index]

        word_locations.append({"word": first_word, "start": (first_x, first_y),
                               "end": (first_x + len(first_word) - 1, first_y),
                               "orientation": "horizontal",
                               "hint": first_word_hint})  # Add the hint for the word

        # Iterate through the remaining words and attempt to place them
        for word in sorted_words[1:]:
            intersections = self.find_intersections(word)
            intersections.sort(key=lambda x: x[1] in placed_words, reverse=True)

            word_placed = False
            for _, other_word, _, word_idx, other_word_idx in intersections:
                if other_word in placed_words:
                    x, y = None, None
                    direction = 'horizontal'
                    if 'horizontal' in placed_words[other_word]:
                        x = placed_words[other_word]['horizontal'][0] - word_idx
                        y = placed_words[other_word]['horizontal'][1] + other_word_idx
                        direction = 'vertical'
                    elif 'vertical' in placed_words[other_word]:
                        x = placed_words[other_word]['vertical'][0] + other_word_idx
                        y = placed_words[other_word]['vertical'][1] - word_idx
                        direction = 'horizontal'

                    if self.can_place_word(word, x, y, direction):
                        self.place_word(word, x, y, direction)
                        if word not in placed_words:
                            placed_words[word] = {}
                        placed_words[word][direction] = (x, y)
                        word_placed = True

                        start_coords = (x, y)
                        end_coords = (x + len(word) - 1, y) if direction == "horizontal" else (x, y + len(word) - 1)

                        word_index = self.words.index(word)
                        word_hint = self.hints[word_index]

                        word_locations.append({"word": word, "start": start_coords,
                                               "end": end_coords,
                                               "orientation": direction,
                                               "hint": word_hint})  # Add the hint for the word
                        break

            if not word_placed:
                print(f"Unable to place word: {word}")



    def print_grid(self):
        for row in self.grid:
            print(' '.join('.' if cell is None else cell for cell in row))


def GetCrossword(_word_list, _grid_size, _hint_list):
    crossword = CrosswordGenerator(_word_list, _grid_size, _hint_list)
    crossword.generate_crossword()
    return crossword.grid, crossword.word_locations

#crossword = CrosswordGenerator(['aa', 'b'], 10, ['aa', 'c'])
#crossword.generate_crossword()
#crossword.word_locations
