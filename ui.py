import pdb
import curses
from curses.textpad import rectangle
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

            row = i if i < 5 else i + 2
            col = j if j < 6 else j + 2
            board_win.addstr(row, col, tile)

    if board[0] == 1:
        board_win.addstr(5, 6, "w")
    if board[0] > 1:
        board_win.addstr(5, 6, "w{}".format(board[0]))

    if board[25] == -1:
        board_win.addstr(6, 6, "b")
    if board[25] < -1:
        board_win.addstr(6, 6, "b{}".format(abs(board[25])))


def main(stdscr):
    rows, cols = stdscr.getmaxyx()

    prows = 40
    pcols = 40
    play_area = curses.newwin(
        prows, pcols, int(rows / 2 - prows / 2), int(cols / 2 - pcols / 2)
    )
    board_win = play_area.derwin(13, 15, int(prows / 2) - 5, int(pcols / 2) - 6)
    upper_indicators_win = play_area.derwin(1, 15, int( prows / 2 ) - 6, int(pcols / 2) - 6)
    lower_indicators_win = play_area.derwin(1, 15, int( prows / 2 ) + 7, int( pcols / 2 ) - 6)
    die1_win = play_area.derwin(6, 6, int( prows / 2 ) - 4, int( pcols / 2 ) - 14)
    die2_win = play_area.derwin(6, 6, int( prows / 2 ) + 3, int( pcols / 2 ) - 14)
    end_turn_win = play_area.derwin(1, 15, int( prows / 2 ) - 7, int( pcols / 2 ) - 5)
    active_player_win = play_area.derwin(1, 15, int( prows / 2 ) + 9, int( pcols / 2 ) - 5)

    game = bg.Game()
    game.roll_dice()

    die_strings = [
        "     \n  o  \n     ",
        "    o\n     \no    ",
        "    o\n  o  \no    ",
        "o   o\n     \no   o",
        "o   o\n  o  \no   o",
        "o   o\no   o\no   o",
    ]

    while True:
        y, x = board_win.getyx()
        play_area.clear()
        draw_board(board_win, game.board)
        die1_win.addstr(0, 0, die_strings[game.dice[0] - 1])
        die2_win.addstr(0, 0, die_strings[game.dice[1] - 1])
        player = "White" if game.active_player == 1 else "Black"
        active_player_win.addstr(0, 0, player + "'s turn.")

        # Determine selected point
        selected_point = -1

        if y > 6 and x < 6:
            selected_point = 13 + x
        if y > 6 and x > 7:
            selected_point = 13 + x - 2
        if y < 5 and x < 6:
            selected_point = 12 - x
        if y < 5 and x > 7:
            selected_point = 12 - x + 2
        if 6 <= x <= 7 and game.active_player == 1:
            selected_point = 0
        if 6 <= x <= 7 and game.active_player == -1:
            selected_point = 25

        # Draw indicators
        legal_targets = game.get_legal_targets(selected_point)

        for l in legal_targets:
            if l <= 6:
                target = 14 - l
                upper_indicators_win.addstr(0, target, "x")
            if 6 < l <= 12:
                target = 12 - l
                upper_indicators_win.addstr(0, target, "x")
            if 12 < l <= 18:
                target = l - 13
                lower_indicators_win.addstr(0, target, "x")
            if l > 18:
                target = l - 11
                lower_indicators_win.addstr(0, target, "x")

        # Draw end turn dialog if turn endable
        if game.turn_endable():
            end_turn_win.addstr(0, 0, "(E)nd turn?")

        play_area.refresh()

        board_win.move(y, x)
        key = board_win.getkey()

        # Handle movement
        if key == "l" or key == "C":
            board_win.move(y, min(x + 1, 13))
        if key == "j" or key == "B":
            board_win.move(min(y + 1, 11), x)
        if key == "k" or key == "A":
            board_win.move(max(y - 1, 0), x)
        if key == "h" or key == "D":
            board_win.move(y, max(x - 1, 0))

        # Handle action
        if key == " ":
            game.max_move(selected_point)
        if key == "u":
            game.undo()
        if key == "e":
            game.end_turn()


curses.wrapper(main)
