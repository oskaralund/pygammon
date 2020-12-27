import unittest
import backgammon as bg

class TestBackgammon(unittest.TestCase):
    def setUp(self):
        self.start_board = [0, 2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5,
                           -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2, 0]
    def test_normal_move(self):
        new_board = bg.move(self.start_board, 1, 1, 2)
        target_board = self.start_board.copy()
        target_board[1] = 1
        target_board[3] = 1
        self.assertEqual(new_board, target_board)

    def test_capture_move(self):
        board = self.start_board.copy()
        board[1] = 1
        board[3] = 1
        target_board = board.copy()
        target_board[1] = -1
        target_board[6] = -4
        target_board[0] = 1
        new_board = bg.move(board, -1, 6, 5)
        self.assertEqual(new_board, target_board)

    def test_move_off_board(self):
        target_board = self.start_board.copy()
        target_board[19] = 4
        new_board = bg.move(self.start_board, 1, 19, 6)
        self.assertEqual(new_board, target_board)

    def test_illegal_play(self):
        legal = bg.is_legal_play(self.start_board, 1, [1,5], [[1,5],[1,1]])
        self.assertFalse(legal)

    def test_legal_play(self):
        legal = bg.is_legal_play(self.start_board, 1, [1,3], [[17,3],[19,1]])
        self.assertTrue(legal)
