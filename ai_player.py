import numpy as np

CENTER_POSITION = (1, 1)
CORNER_POSITIONS = [(0, 0), (0, 2), (2, 0), (2, 2)]


class AI:
    """ Set of rules for computer to make moves. Only plays as 'O's """

    def __init__(self):
        self.player = 2

    def make_move(self, board, game_step: int) -> None:
        """
        Makes decision for the next step.
        Tries to go for the center or any of the diagonals. If there's a row with any two nonzero symbols of the
        same kind, selects the third field of the row to win or block the opponent
        :param board: current game field as Board object
        :param game_step: current game iteration only used to make the first step
        """
        positions = board.get_board()

        def is_free(position: tuple) -> bool:
            """
            Helper func. Checks if specified field is empty (has a 0 value)
            :param position: field coordinates to check
            :return: whether position is free
            """
            return positions[position] == 0

        def empty_pos(row: np.ndarray, check_for: int) -> np.ndarray:
            """
            Helper func, checks if there are two symbols of same kind in the row and third field is free.
            :param check_for: which 2 symbols in a row to check for - 1:X, 2:O
            :param row: row of the Board to check
            :return: Board index of the free field
            """
            if (np.count_nonzero(row == check_for) == 2) and (0 in row):
                return np.where(row == 0)[0][0]

        def two_in_row(check_for: int) -> tuple | None:
            """
            Checks the whole game Board for rows with two symbols of same type
            :param check_for: which 2 symbols in a row to check for - 1:X, 2:O
            :return: Board row/column indices for the empty position
            """
            for arr in [positions, positions.T]:
                for row_n, row in enumerate(arr):
                    index = empty_pos(row, check_for=check_for)
                    if index is not None:
                        return (row_n, index) if arr is positions else (index, row_n)
            main_diagonal = np.diag(positions)
            second_diagonal = np.diag(np.fliplr(positions))
            for row in [main_diagonal, second_diagonal]:
                index = empty_pos(row, check_for=check_for)
                if index is not None:
                    if row is main_diagonal:
                        return index, index
                    else:
                        return index, (2 - index)

        if game_step == 2:
            if is_free(CENTER_POSITION):
                board.make_move(self.player, coord=CENTER_POSITION)
            else:
                board.make_move(self.player, CORNER_POSITIONS[0])
        else:
            # First check if any row can be completed with a 'O' to win
            indices = two_in_row(check_for=2)
            if indices is not None:
                i, j = indices
                board.make_move(self.player, (i, j))
            else:
                # Then check if any row can be completed to block the 'X'
                indices = two_in_row(check_for=1)
                if indices is not None:
                    i, j = indices
                    board.make_move(self.player, (i, j))
                else:
                    for pos in CORNER_POSITIONS:
                        if is_free(pos):
                            board.make_move(self.player, pos)
                            break
