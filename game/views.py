from django.shortcuts import render, redirect
from .game_logic import SudokuGrid, load_puzzles, COL_LABELS, DISPLAY_EMPTY
import random

# Create your views here.
GAME_SESSION_KEY = 'sudoku_game'

def get_or_create_grid(request):
    if GAME_SESSION_KEY not in request.session:
        try:
            puzzles = load_puzzles()
        except FileNotFoundError as e:
            return None, str(e)

        puzzle_string = random.choice(puzzles)
        grid = SudokuGrid(puzzle_string)

        request.session[GAME_SESSION_KEY] = grid.original_setup_str

    original_setup = request.session.get(GAME_SESSION_KEY)
    grid = SudokuGrid(original_setup)

    active_grid_data = request.session.get('active_grid_data')
    if active_grid_data:
        grid.grid = active_grid_data

    return grid, None


def sudoku_view(request):
    if 'sudoku_setup' not in request.session:
        return new_game(request)

    original_setup_str = request.session['sudoku_setup']
    active_grid_data = request.session['sudoku_active_grid']
    grid_obj = SudokuGrid(original_setup_str)
    grid_obj.grid = active_grid_data

    message = request.session.pop('message', '')

    if request.method == 'POST':
        action = request.POST.get('action', '').upper()

        if action in ('RESET', 'NEW', 'UNDO', 'ORIGINAL', 'QUIT'):
            if action == 'RESET':
                grid_obj.reset_grid()
                request.session['message'] = "Grid has been reset."
            elif action == 'NEW':
                return redirect('sudoku_new')
            elif action == 'UNDO':
                request.session['message'] = "UNDO command is not yet fully implemented for session state."

        else:
            try:
                space, number = action.split()
                column, row = space

                if column not in COL_LABELS or not (1 <= int(row) <= 9) or not (1 <= int(number) <= 9):
                    request.session['message'] = "Invalid move format or value."
                elif grid_obj.make_move(column, row, number) == False:
                    request.session['message'] = "Cannot overwrite an original number."
                else:
                    request.session['message'] = f"Moved {number} to {column}{row}."
            except:
                request.session['message'] = "Invalid input. Please use format like B4 9 or a command."

        request.session['sudoku_active_grid'] = grid_obj.grid
        return redirect('sudoku_board')

    is_solved = grid_obj.is_solved()
    if is_solved:
        message = "Congratulations! You solved the puzzle!"

    context = {
        'grid_data': grid_obj.grid,
        'col_labels': COL_LABELS,
        'row_labels': range(1, 10),
        'display_empty': DISPLAY_EMPTY,
        'is_solved': is_solved,
        'message': message,
    }
    return render(request, 'index.html', context)


def new_game(request):
    # try:
    puzzles = load_puzzles()
    if not puzzles :
        raise ValueError("Puzzle file is empty or contains no valid puzzles.")

    puzzle_string = random.choice(puzzles)

    # except (FileNotFoundError, ValueError) as e:
    #     return render(request, 'game/sudoku_error.html', {'error_message' :str(e)})

    new_grid = SudokuGrid(puzzle_string)

    request.session['sudoku_setup'] = new_grid.original_setup_str
    request.session['sudoku_active_grid'] = new_grid.grid
    request.session['message'] = "New game started!"

    return redirect('sudoku_board')