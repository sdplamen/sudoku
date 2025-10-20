import copy, random, sys

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

            # Execute the move
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
        for i in range(GRID_SIZE): 
            row_numbers = self.grid[i]
            col_numbers = [self.grid[r][i] for r in range(GRID_SIZE)]

            if not self._is_valid_set(row_numbers) or not self._is_valid_set(col_numbers): 
                return False

        for box_start_r in (0, 3, 6): 
            for box_start_c in (0, 3, 6): 
                box_numbers = []
                for r_offset in range(BOX_SIZE): 
                    for c_offset in range(BOX_SIZE): 
                        box_numbers.append(self.grid[box_start_r + r_offset][box_start_c + c_offset])

                if not self._is_valid_set(box_numbers): 
                    return False

        return True

def load_puzzles(filepath='sudokupuzzles.txt'): 
    try: 
        with open(filepath) as puzzle_file: 
            puzzles = [p.strip() for p in puzzle_file if p.strip()]
        return puzzles
    except FileNotFoundError: 
        print(f"Error: Puzzle file '{filepath}' not found.")
        sys.exit()


def print_welcome_message(): 
    print(
        '''\nSudoku Puzzle, by Al Sweigart (modified)
        Sudoku is a number placement logic puzzle game. A Sudoku grid is a 9x9
        grid of numbers. Try to place numbers in the grid such that every row,
        column, and 3x3 box has the numbers 1 through 9 once and only once.
        ''')
    input('Press Enter to begin...')


def get_action_input(): 
    while True: 
        print('\nEnter a move (e.g., "B4 9"), or type one of the commands:')
        print('  Commands: RESET, NEW, UNDO, ORIGINAL, or QUIT')
        action = input('> ').upper().strip()

        if not action: 
            continue

        parts = action.split()

        if action[0] in ('R', 'N', 'U', 'O', 'Q'): 
            return action, None, None, None

        if len(parts) == 2: 
            space, number = parts
            if len(space) == 2: 
                column, row = space

                if column in COL_LABELS: 
                    if row.isdigit() and 1 <= int(row) <= 9: 
                        if number.isdigit() and 1 <= int(number) <= 9: 
                            return action, column, row, number
                        else: 
                            print(f'Please select a number from 1 to 9, not {number}.')
                    else: 
                        print(f'There is no row {row}. Rows are 1-9.')
                else: 
                    print(f'There is no column {column}. Columns are A-I.')
        else: 
            print('Invalid input format. Try "C5 8" or a command.')

        print()

if __name__ == '__main__': 
    print_welcome_message()

    puzzles = load_puzzles()
    if not puzzles: 
        print("No puzzles loaded. Exiting.")
        sys.exit()

    grid = SudokuGrid(random.choice(puzzles))

    while True: 
        grid.display()

        if grid.is_solved(): 
            print('\n🎉 Congratulations! You solved the puzzle! 🎉')
            print('Thanks for playing!')
            sys.exit()

        action, column, row, number = get_action_input()

        if action.startswith('R'): 
            grid.reset_grid()
            print('Grid reset to original state.')
            continue

        elif action.startswith('N'): 
            grid = SudokuGrid(random.choice(puzzles))
            print('Starting a new puzzle!')
            continue

        elif action.startswith('U'): 
            grid.undo()
            print('Last move undone.')
            continue

        elif action.startswith('O'): 
            original_grid = SudokuGrid(grid.original_setup_str)
            print('\nThe original grid looked like this:')
            original_grid.display()
            input('Press Enter to continue...')
            continue

        elif action.startswith('Q'): 
            print('Thanks for playing!')
            sys.exit()

        if column and row and number: 
            if not grid.make_move(column, row, number): 
                print('\n⚠️ You cannot overwrite a number from the original puzzle setup.')
                print('Type ORIGINAL to view the original grid.')
                input('Press Enter to continue...')