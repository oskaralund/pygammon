"""
A backgammon board is represented by a list of length 26. For example

  board = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5,
           -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]

is the starting position. The 0th and the 25th elements represents the bars.
"""

import itertools as it
import random
import pdb


def get_new_board():
    return [
        0,
        2,
        0,
        0,
        0,
        0,
        -5,
        0,
        -3,
        0,
        0,
        0,
        5,
        -5,
        0,
        0,
        0,
        3,
        0,
        5,
        0,
        0,
        0,
        0,
        -2,
        0,
    ]


def draw(board):
    """
    Prints an ascii representation of a Backgammon board.
    """

    assert len(board) == 26, "A Backgammon board must be of length 26."

    player_symbol = "w"
    opponent_symbol = "b"
    empty_symbol = "|"
    board_string = ""
    max_stack = max([abs(b) for b in board])

    for k in range(max_stack):
        for i, b in enumerate(board[12:0:-1]):
            if i == 6:
                board_string += " "
            if b > 0 and abs(b) > k:
                board_string += player_symbol
            elif b < 0 and abs(b) > k:
                board_string += opponent_symbol
            else:
                board_string += empty_symbol
        board_string += "\n"

    board_string += "\n"

    for k in range(max_stack):
        for i, b in enumerate(board[13:25]):
            if i == 6:
                board_string += " "
            if b > 0 and abs(b) + k > max_stack - 1:
                board_string += player_symbol
            elif b < 0 and abs(b) + k > max_stack - 1:
                board_string += opponent_symbol
            else:
                board_string += empty_symbol
        board_string += "\n"

    return board_string


def winner(board):
    """
    Check if a Backgammon board has a winner.

    Returns:
        1 if the Player has won.
        -1 if the Opponent has won.
        0 if there is no winner yet.
    """

    assert len(board) == 26, "A Backgammon board must be of length 26."

    if all([b <= 0 for b in board]):
        return 1
    elif all([b >= 0 for b in board]):
        return -1
    else:
        return 0


def num_possible_moves(board, player, dice):
    """
    Compute the maximum number of moves possible (0-4).

    Input:
        board - an iterable representing a Backgammon board at the start of a turn.
        player - 1 for player, -1 for opponent.
        dice - a list [d1,d2] representing the state of the dice.

    Returns:
        An integer between 0 and 4.
    """

    max_moves = 0

    # Not a double roll
    if dice[0] != dice[1]:
        for i, d1 in it.product(range(26), dice):
            if is_legal_move(board, player, i, d1):
                max_moves = 1
                new_board = move(board, player, i, d1)
                d2 = dice[0] if dice[0] != d1 else dice[1]
                for j in range(26):
                    if is_legal_move(new_board, player, j, d2):
                        max_moves = 2
                        break

    # Double roll
    if dice[0] == dice[1]:
        d = dice[0]
        new_board = board.copy()
        for _ in range(4):
            for i in range(26):
                if is_legal_move(new_board, player, i, d):
                    max_moves += 1
                    new_board = move(board, player, i, d)
                    break

    return max_moves


def is_legal_move(board, player, point, distance):
    """
    Check if an isolated move is legal. Does not take into account the
    current dice.

    Input:
        board - an iterable representing a Backgammon board.
        player - 1 for player, -1 for opponent.
        point - point you want to move from (1-24).
        distance - distance you want to move.

    Returns:
        True if legal.
        False if not legal.
    """
    assert player == 1 or player == -1, "player must be 1 or -1."

    end_point = point + distance * player

    # Is distance is within legal range?
    if not 1 <= distance <= 6:
        return False

    # Is there a checker to move at the point?
    if player == -1 and board[point] >= 0:
        return False

    if player == 1 and board[point] <= 0:
        return False

    # Are we trying to move a checker while captured?
    if player == 1 and point != 0 and board[0] > 0:
        return False

    # Are they trying to move a checker while captured?
    if player == -1 and point != 25 and board[25] < 0:
        return False

    # Are we trying to move off the board?
    if end_point > 24:
        # Illegal if not all checkers on home board
        if any([b > 0 for b in board[0:19]]):
            return False
        # Illegal if checkers does not bear off exactly and has checkers behind
        elif any([b > 0 for b in board[19:point]]):
            return False

    if end_point < 1:  # Are they trying to move off the board?
        # Illegal if not all checkers on home board
        if any([b < 0 for b in board[7:]]):
            return False
        # Legal if all checkers on home board and checker bears off exactly
        elif end_point == 0:
            return True
        # Illegal if checkers does not bear off exactly and has checkers behind
        elif any([b < 0 for b in board[point + 1 : 7]]):
            return False

    # Check if point is occupied
    if player == 1 and board[end_point] < -1:
        return False
    if player == -1 and board[end_point] > 1:
        return False

    return True


def has_legal_move(board, player, distance):
    """
    Check if a particular distance can be legally moved with some checker.

    Input:
        board - an iterable representing a Backgammon board.
        player - 1 for player, -1 for opponent.
        distance - a distance to move.

    Returns:
        True if the distance can be moved legally.
        False if the distance cannot be moved legally.
    """

    for i, _ in enumerate(board):
        if is_legal_move(board, player, i, distance):
            pass


def is_legal_play(board, player, dice, play):
    """
    Check if a play is legal.

    Input:
        board - an iterable representing a Backgammon board.
        player - 1 for player, -1 for opponent.
        dice - a list [d1,d2] representing the state of the dice.
        play - a list of moves [point, distance] defining the play.

    Returns:
        True if the play is legal (i.e. the turn can be ended).
        False if the play is illegal (i.e. the turn cannot be ended).
    """

    required_number_of_moves = num_possible_moves(board, player, dice)

    # Fewer than required number of moves
    if len(play) < required_number_of_moves:
        return False

    new_board = board.copy()
    for p in play:
        if is_legal_move(new_board, player, p[0], p[1]):
            new_board = move(new_board, player, p[0], p[1])
        else:
            return False

    return True


def move(board, player, point, distance):
    """
    Move a checker on a Backgammon board.

    Input:
        board - an iterable representing a Backgammon board.
        player - 1 for player, -1 for opponent.
        point - point to move from (1-24).
        distance - distance to move.

    Returns:
        A new board with the move performed.
    """
    assert player == 1 or player == -1, "player must be 1 or -1."

    new_board = board.copy()

    end_point = point + player * distance

    # Normal non-capturing move inside board
    if 0 < end_point < 24 and board[end_point] + player != 0:
        new_board[point] -= player
        new_board[end_point] += player

    # Capture move
    if 0 < end_point < 24 and board[end_point] + player == 0:
        new_board[point] -= player
        new_board[end_point] = player
        bar_point = 0 if player == -1 else 25
        new_board[bar_point] -= player

    # Move off the board
    if not 0 < end_point < 24:
        new_board[point] -= player

    return new_board


def legal_targets(board, player, point, distances):
    """
    Return legal target points, i.e. possible points to move to given a starting point and a list of distances.

    Input:
        board - an iterable representing a Backgammon board.
        player - 1 for player, -1 for opponent.
        point - point to move from (1-24).
        distances - possible distances to move.

    Returns:
        A list of legal target points.
    """
    targets = [
        point + player * d for d in distances if is_legal_move(board, player, point, d)
    ]

    for i in range(len(targets)):
        targets[i] = 0 if targets[i] < 1 else targets[i]
        targets[i] = 25 if targets[i] > 24 else targets[i]

    return targets


class Game:
    """
    A class representing a Backgammon game.
    """

    def __init__(self):
        self.board = get_new_board()
        self.board_at_turn_start = self.board.copy()
        self.dice = [1, 1]
        self.active_player = 1
        self.history = []
        self.moves = []
        self.current_play = []

    def roll_dice(self):
        self.dice = [random.randint(1, 6), random.randint(1, 6)]
        if self.dice[0] == self.dice[1]:
            self.moves = [self.dice[0]] * 4
        else:
            self.moves = self.dice.copy()

    def move(self, point, distance):
        if distance in self.moves and is_legal_move(
            self.board, self.active_player, point, distance
        ):
            self.board = move(self.board, self.active_player, point, distance)
            self.moves.remove(distance)
            self.current_play.append([point, distance])

    def max_move(self, point):
        if self.moves == []:
            return

        if is_legal_move(self.board, self.active_player, point, max(self.moves)):
            self.move(point, max(self.moves))
        elif is_legal_move(self.board, self.active_player, point, min(self.moves)):
            self.move(point, min(self.moves))

    def min_move(self, point):
        if self.moves == []:
            return

        if is_legal_move(self.board, self.active_player, point, min(self.moves)):
            self.move(point, min(self.moves))
        elif is_legal_move(self.board, self.active_player, point, max(self.moves)):
            self.move(point, max(self.moves))

    def end_turn(self):
        if self.turn_endable():
            self.history.append((self.active_player, self.current_play))
            self.active_player *= -1
            self.current_play = []
            self.board_at_turn_start = self.board.copy()
            self.roll_dice()

    def turn_endable(self):
        if is_legal_play(
            self.board_at_turn_start,
            self.active_player,
            self.dice,
            self.current_play,
        ):
            return True

    def undo(self):
        if self.current_play == []:
            return

        m = self.current_play.pop()
        self.moves.append(m[1])
        self.board = self.board_at_turn_start.copy()
        for p in self.current_play:
            self.board = move(self.board, self.active_player, p[0], p[1])

    def get_legal_targets(self, point):
        return legal_targets(self.board, self.active_player, point, self.moves)


if __name__ == "__main__":
    board = get_new_board()

    board = move(board, 1, 1, 1)
    print(draw(board))
