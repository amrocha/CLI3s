import curses
from random import randint

SIZE = 4
GRID = [
    '+------+------+------+------+',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '+------+------+------+------+',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '+------+------+------+------+',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '+------+------+------+------+',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '|      |      |      |      |',
    '+------+------+------+------+'
    ]

ROW = [2, 6, 10, 14]
COL = [2, 9, 16, 23]
DOWN = 258
UP = 259
LEFT = 260
RIGHT = 261

next_tile = randint(1, 3)


def create_initial_grid():
    initial_grid = [
        [1, 2, 0, 0],
        [3, 1, 1, 0],
        [3, 3, 2, 2],
        [0, 0, 0, 3]
    ]
    return initial_grid


def draw_next_tile(stdscr):
    stdscr.addstr(len(GRID), 0, 'Next Tile: {}'.format(next_tile))


def draw_grid(stdscr, board):
    for i, line in enumerate(GRID):
        stdscr.addstr(i, 0, line)

    for i in xrange(0, SIZE):
        for j in xrange(0, SIZE):
            if board[i][j] > 0:
                stdscr.addstr(ROW[i], COL[j], str(board[i][j]))


def add_tile(grid, possible_positions, move):
    global next_tile
    new_tile = next_tile
    next_tile = randint(1, 3)

    position = possible_positions[randint(0, len(possible_positions) - 1)]

    if(move == LEFT):
        grid[position][SIZE-1] = new_tile
    elif(move == RIGHT):
        grid[position][0] = new_tile
    elif(move == UP):
        grid[SIZE-1][position] = new_tile
    elif(move == DOWN):
        grid[0][position] = new_tile

    return grid


# Resolves a move RIGHT in a tile array
def resolve_move(row):
    blocked = True
    new_row = [0, 0, 0, 0]
    for i in xrange(0, SIZE):
        if (blocked):
            if(i > 0):
                left_tile = row[SIZE-i-1]
                right_tile = row[SIZE-i]
                if(
                    (left_tile == 1 and right_tile == 2) or
                    (left_tile == 2 and right_tile == 1)
                ):
                    new_row[SIZE-i] = 3
                    blocked = False
                elif(
                    left_tile != 0 and
                    left_tile % 3 == 0 and
                    left_tile == right_tile
                ):
                    new_row[SIZE-i] = left_tile * 2
                    blocked = False
                elif(right_tile == 0 and left_tile != 0):
                    new_row[SIZE-i] = left_tile
                    blocked = False
                else:
                    new_row[SIZE-i] = right_tile
                    new_row[SIZE-i-1] = left_tile
        else:
            new_row[SIZE-i] = row[SIZE-i-1]

    return new_row, not blocked


def get_new_board(move, board):
    new_grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    changed_rows = []

    # the idea here is to call a function with an array and a move RIGHT
    # then depending on the move rearrange what you get back
    # and put it in the new grid
    for i in xrange(0, SIZE):
        if move == DOWN:
            new_arr, arr_changed = resolve_move([arr[i] for arr in board])
            for j in xrange(0, SIZE):
                new_grid[j][i] = new_arr[j]
        elif move == UP:
            arr = [arr[i] for arr in board]
            arr.reverse()
            new_arr, arr_changed = resolve_move(arr)
            new_arr.reverse()
            for j in xrange(0, SIZE):
                new_grid[j][i] = new_arr[j]
        elif move == RIGHT:
            new_arr, arr_changed = resolve_move(board[i])
            new_grid[i] = new_arr
        elif move == LEFT:
            arr = board[i]
            arr.reverse()
            new_arr, arr_changed = resolve_move(arr)
            new_arr.reverse()
            new_grid[i] = new_arr

        if arr_changed:
            changed_rows.append(i)

    if(len(changed_rows) > 0):
        new_grid = add_tile(new_grid, changed_rows, move)

    return new_grid


def threes_app(stdscr):
    board = create_initial_grid()
    draw_grid(stdscr, board)
    while(True):
        move = stdscr.getch()
        if unichr(move) == 'q':
            break
        board = get_new_board(move, board)
        stdscr.erase()
        draw_grid(stdscr, board)
        draw_next_tile(stdscr)

if __name__ == '__main__':
    curses.wrapper(threes_app)
