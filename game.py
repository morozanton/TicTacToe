import numpy as np
from abc import ABC, abstractmethod
from ai_player import AI


class Board:
    """A game field represented by  3x3 numpy array"""

    def __init__(self):
        self.border = '|---|---|---|'
        self.line = '|   |   |   |'
        self.board = np.zeros((3, 3), dtype=int)

    def get_board(self):
        return self.board

    @staticmethod
    def translate_coord(coord: int) -> tuple:
        """
        Translates one-dimensional board coordinates into two-dimensional array indices
        :param coord: Field number 1-9
        :return: two array indices
        """
        row = (coord - 1) // 3
        col = (coord - 1) % 3
        return row, col

    @staticmethod
    def translate_sym(inp: int) -> str:
        """
        Translates ints to symbols to represent the game in console
        :param inp: board value to translate
        :return: translated symbol
        """
        translations = {0: ' ', 1: 'X', 2: 'O'}
        return translations.get(inp)

    def draw_board(self, draw_numbers=False) -> None:
        """
        Prints game field
        :param draw_numbers: draw field numbers (1-9) for player reference
        """
        for row_n, row in enumerate(self.board):
            print(self.border)
            for count, el in enumerate(row):
                if draw_numbers:
                    sym = (count + 1) + (row_n * 3)
                else:
                    sym = self.translate_sym(el)
                if count == 1:
                    print(f' {sym} ', end='')
                else:
                    print(f'| {sym} |', end='')
            print()
        print(self.border)

    def make_move(self, player: int, coord: tuple) -> None:
        """
        Changes board array values to specified player symbol at specified coordinates
        :param player: 1 = 'X', 2 = 'O'
        :param coord: np array indices for the move
        """
        row, col = coord
        if self.board[row][col] == 0:
            self.board[row][col] = player
        else:
            raise Exception('Position taken')


class Game(ABC):
    """Abstract class to initialize game field and check for winner"""

    def __init__(self):
        self.board = Board()
        self.board.draw_board(draw_numbers=True)
        self.player = 2
        self.game_step = 0

    def next_player(self) -> int:
        """Switches current player from 'X' to 'O' and tracks the number of game steps"""
        self.game_step += 1
        self.player = 2 if self.player == 1 else 1
        return self.player

    def game_over(self) -> bool:
        """
        Checks if all positions are taken (a draw) or
        symbols of  any row|column or diagonal of board are the same
        """
        def check_row(r) -> bool:
            """
            Helper func that check if all symbols in any 1x3 array are the same
            :param r: one-dimensional input array
            """
            if np.all(r == self.player):
                print(f'Player {self.player} wins')
                return True

        values = self.board.get_board()
        if np.all(values != 0):
            print("It's a draw!")
            return True

        for arr in [values, values.T]:
            for row in arr:
                if check_row(row):
                    return True

        for row in [np.diag(values), np.diag(np.fliplr(values))]:
            if check_row(row):
                return True

    @abstractmethod
    def game_loop(self):
        """Abstract class method to implement game logic in child classes"""
        pass


class MultiplayerGame(Game):
    """Implements game logic for player input both for one-player and two-player games"""

    def __init__(self):
        super().__init__()

    def player_move(self, sym: str) -> None:
        """
        Receives player input to change the game field
        :param sym: player symbol ('X' or 'O') for text output
        """
        while True:
            try:
                move = int(input(f'Player {sym} - enter position (1-9): '))
                coord = self.board.translate_coord(move)
                self.board.make_move(player=self.player, coord=coord)
                break
            except Exception:
                print('Selected position is not empty')

    def game_loop(self) -> None:
        """
        Main game loop for two-player game
        """
        while not self.game_over():
            player_sym = self.board.translate_sym(self.next_player())
            self.player_move(player_sym)
            self.board.draw_board()


class AiGame(MultiplayerGame, Game):
    """Implements the logic for player vs AI game"""

    def __init__(self):
        super().__init__()
        self.ai_player = AI()

    def game_loop(self) -> None:
        """Main game loop for player vs AI game"""
        while not self.game_over():
            player_sym = self.board.translate_sym(self.next_player())
            player = self.player
            if player == 1:
                self.player_move(sym=player_sym)
            else:
                self.ai_player.make_move(board=self.board, game_step=self.game_step)
                self.board.draw_board()
