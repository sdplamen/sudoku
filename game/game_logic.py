import copy

EMPTY_SPACE = '0'
DISPLAY_EMPTY = '.'
GRID_SIZE = 9
BOX_SIZE = 3
ALL_NUMBERS = set('123456789')
COL_LABELS = 'ABCDEFGHI'


class SudokuGrid:
    def __init__(self, puzzle_string):
        processed_string = puzzle_string.replace(DISPLAY_EMPTY, '0').strip()
        if len(processed_string) != GRID_SIZE * GRID_SIZE:
            raise ValueError('Puzzle string must be 81 characters long.')
        self.original_setup_str = processed_string
        self.grid = []
        self.reset_grid()
        self.moves_history = []

    def reset_grid(self):
        self.grid = []
        for r in range(GRID_SIZE):
            start = r * GRID_SIZE
            row = list(self.original_setup_str[start:  start + GRID_SIZE])
            self.grid.append(row)

        self.moves_history = []

    def make_move(self, col_char, row_num, number):
        try:
            col = COL_LABELS.index(col_char)
            row = int(row_num) - 1
            number_str = str(number)

            if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
                return False
            if self.original_setup_str[row * GRID_SIZE + col] != '0':
                return False

            if number_str not in ALL_NUMBERS:
                return False

            self.grid[row][col] = number_str
            self.moves_history.append(copy.deepcopy(self.grid))
            return True
        except ValueError:
            return False

    def undo(self):
        if not self.moves_history:
            return

        self.moves_history.pop()

        if not self.moves_history:
            self.reset_grid()
        else:
            self.grid = copy.deepcopy(self.moves_history[-1])

    def display(self):
        print('   ' + ' '.join(COL_LABELS[:3]) + '   ' +
              ' '.join(COL_LABELS[3: 6]) + '   ' +
              ' '.join(COL_LABELS[6: ]))

        for r in range(GRID_SIZE):
            row_output = []
            for c in range(GRID_SIZE):
                value = self.grid[r][c]
                row_output.append(value if value != '0' else DISPLAY_EMPTY)

                if c == 2 or c == 5:
                    row_output.append('|')

            print(f'{r + 1}  {" ".join(row_output)}')

            if r == 2 or r == 5:
                print('   ' + '------+-------+------')

    def _is_valid_set(self, numbers):
        return set(numbers) == ALL_NUMBERS

    def is_solved(self):
        for i in range(GRID_SIZE) :
            row_numbers = self.grid[i]
            col_numbers = [self.grid[r][i] for r in range(GRID_SIZE)]

            if not self._is_valid_set(row_numbers) or not self._is_valid_set(col_numbers) :
                return False

        for box_start_r in (0, 3, 6) :
            for box_start_c in (0, 3, 6) :
                box_numbers = []
                for r_offset in range(BOX_SIZE) :
                    for c_offset in range(BOX_SIZE) :
                        box_numbers.append(self.grid[box_start_r + r_offset][box_start_c + c_offset])

                if not self._is_valid_set(box_numbers) :
                    return False

        return True

def load_puzzles(filepath='puzzles/sudokupuzzles.txt'):
    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_filepath = os.path.join(base_dir, 'puzzles', 'sudokupuzzles.txt')

    try:
        with open(full_filepath) as puzzle_file:
            puzzles = [p.strip() for p in puzzle_file if p.strip()]
        return puzzles
    except FileNotFoundError:
        raise FileNotFoundError(f"Puzzle file not found at: {full_filepath}")