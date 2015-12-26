import curses

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


def draw_grid(stdscr):
    for i, line in enumerate(GRID):
        stdscr.addstr(i, 0, line)


def threes_app(stdscr):
    draw_grid(stdscr)
    stdscr.getch()
    stdscr.erase()
    stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(threes_app)
