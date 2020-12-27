import pdb
import curses
import backgammon as bg


def board_to_matrix(board):
    """
    Returns a 11x13 matrix representing the state of the board.
    """
    M = [[0 for _ in range(12)] for _ in range(10)]

    for k in range(5):
        for i, b in enumerate(board[12:0:-1]):
            if b > 0 and abs(b) > k:
                M[k][i] = 1 if k < 5 else b - 4
            elif b < 0 and abs(b) > k:
                M[k][i] = -1 if k < 5 else b + 4
            else:
                M[k][i] = 0

    for k in range(5):
        for i, b in enumerate(board[13:25]):
            if b > 0 and abs(b) + k > 4:
                M[5 + k][i] = 1 if k > 0 else b - 4
            elif b < 0 and abs(b) + k > 4:
                M[5 + k][i] = -1 if k > 0 else b + 4
            else:
                M[5 + k][i] = 0

    return M


def draw_board(board_win, board):
    y, x = board_win.getyx()
    M = board_to_matrix(board)

    for i in range(10):
        for j in range(12):
            tile = "|"
            if M[i][j] == 1:
                tile = "w"
            if M[i][j] == -1:
                tile = "b"
            if abs(M[i][j]) > 1:
                tile = str(abs(M[i][j]))

            row = i if i < 5 else i + 1
            col = j if j < 6 else j + 1
            board_win.addstr(row, col, tile)

    board_win.move(y, x)


def main(stdscr):
    rows, cols = stdscr.getmaxyx()
    board_win = curses.newwin(13, 15, int(rows / 2) - 5, int(cols / 2) - 6)
    upper_indicators_win = curses.newwin(1, 15, int(rows / 2) - 6, int(cols / 2) - 6)
    lower_indicators_win = curses.newwin(1, 15, int(rows / 2) + 6, int(cols / 2) - 6)
    game = bg.Game()
    game.roll_dice()
    draw_board(board_win, game.board)

    while True:
        upper_indicators_win.clear()
        lower_indicators_win.clear()
        key = board_win.getkey()

        # Handle movement
        y, x = board_win.getyx()
        if key == "l" or key == "C":
            board_win.move(y, min(x + 1, 12))
        if key == "j" or key == "B":
            board_win.move(min(y + 1, 10), x)
        if key == "k" or key == "A":
            board_win.move(max(y - 1, 0), x)
        if key == "h" or key == "D":
            board_win.move(y, max(x - 1, 0))
        y, x = board_win.getyx()

        # Determine selected point
        selected_point = -1

        if y > 5 and x < 6:
            selected_point = 13 + x
        if y > 5 and x > 6:
            selected_point = 13 + x - 1
        if y < 5 and x < 6:
            selected_point = 12 - x
        if y < 5 and x > 6:
            selected_point = 12 - x + 1

        # Handle action
        if key == " ":
            game.max_move(selected_point)
        if key == "u":
            game.undo()
        if key == "e":
            game.end_turn()

        # Draw indicators
        legal_targets = game.get_legal_targets(selected_point)

        for l in legal_targets:
            if l <= 6:
                target = 13-l
                upper_indicators_win.addstr(0,target,"x")
            if 6 < l <= 12:
                target = 12-l
                upper_indicators_win.addstr(0,target,"x")
            if 12 < l <= 18:
                target = l-13
                lower_indicators_win.addstr(0,target,"x")
            if l > 18:
                target = l-12
                lower_indicators_win.addstr(0,target,"x")
        upper_indicators_win.refresh()
        lower_indicators_win.refresh()


        draw_board(board_win, game.board)
        stdscr.refresh()
        board_win.refresh()


curses.wrapper(main)
