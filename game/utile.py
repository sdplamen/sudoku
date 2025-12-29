def cross(A, B):
    return [a + b for a in A for b in B]


def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    return dict(zip(squares, chars))


def removeDot(dict):
    # Rimuove i punti
    for el in dict:
        if dict[el] == '.':
            dict[el] = ''
    return dict


digits = '123456789'
rows = 'ABCDEFGHI'
digits = '123456789'
cols = digits
squares = cross(rows, cols)