# -*- coding: utf-8 -*-
from .utile import grid_values, cross


def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values


def assign(values, s, d):
    others_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in others_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False

    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values


def search(values):
    if not values:
        return False
    if all(len(values[s]) == 1 for s in values):
        return values
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])


def some(seq):
    for e in seq:
        if e:
            return e
    return False

def is_valid_input(grid_dict):
    for unit in unitlist:
        nums = [grid_dict[s] for s in unit if grid_dict[s] in '123456789']
        if len(nums) != len(set(nums)):
            return False
    return True

def solve(grid):
    return search(parse_grid(grid))


def display(values):
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
    print('')


rows = 'ABCDEFGHI'
digits = '123456789'
cols = digits
squares = cross(rows, cols)

unit_c = [cross(rows, c) for c in cols]
unit_r = [cross(r, cols) for r in rows]
unit_sq = [cross(r, c) for r in ['ABC', 'DEF', 'GHI'] for c in ['123', '456', '789']]
unitlist = unit_c + unit_r + unit_sq

units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)

'''
# ------------------------------------------------------------------------------------------------------------------- #

def redefine_dictionary(sudoku_dict):
    new_digits = [int(digit) - 1 for digit in digits]
    map_letter = dict(zip(rows, new_digits))
    new_keys = {x: (map_letter[x[0]], int(x[1]) - 1) for x in sudoku_dict.keys()}
    return {new_keys[x]: int(sudoku_dict[x]) for x in sudoku_dict.keys()
            if sudoku_dict[x] != '.' and sudoku_dict[x] != '0'}


# ------------------------------------------------------------------------------------------------------------------- #
# Convert input and output in JSON format

def create_json_dictinary(dict):
    return json.dumps(dict)

# ------------------------------------------------------------------------------------------------------------------- #


# display((solve(grid1)))
# display((solve(grid2)))
# display((solve(grid3)))
# display((solve(grid4)))
# display((solve(test)))

# start = redefine_dictionary(grid_values(hard6))
# end = redefine_dictionary(solve(hard6))
'''

if __name__ == '__main__':
    print('Welcome2 to Sudoku!')
    print('')
    grid1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    grid3 = '2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3'
    grid4 = '38..........4..785..9.2.3...6..9....8..3.2..9....4..7...1.7.5..495..6..........92'
    hard = '2..94.1.5.6.7...9.....65..8..6.2.....2.....3.....7.6..9..65.....3...1.7.1.5.37..6'
    hard2 = '24..83.7.....2....8..96..3.6......53..3...7..19......2.3..16..7....4.....8.53..19'
    hard3 = '3..5...2.........3..........1...5...2...3...6...1...7..........5.........6...4..2'
    test1 = '16...43.7...1....43...87...6.24.9.7...9...4...3.7.52.6...36...57....1...8.35...61'
    hard4 = '....67..........86.29....4...7.9.8......3...7..1..2.9..1...9..2...6..35.37.8.....'
    hard5 = '3..4..6..7...9...38..3......3.521..........9..2..3..4..48..2.....6...1.......74..'
    hard6 = '.5...8.2.4.3...7.1....5....1...4......9.7.6......2...8....3....2.6...9.5.7.1...4.'
    corriere_23_03_2020 = '..8.7....36.9....1.9.1.83...7.......28.....57.......2...37.2.9.4....1.38....9.1..'
    start = grid_values(corriere_23_03_2020)
    end = solve(corriere_23_03_2020)
    #print(start)
    #print(end)
    display(start)
    display(end)

'''app = wx.App(0)
frame_start = wx.Frame(None, -1, 'Sudoku')
frame_end = wx.Frame(None, -1, 'Sudoku Solved')
GridSudoku(frame_start, start)
GridSudoku(frame_end, end)
app.MainLoop()'''