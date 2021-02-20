from .errors import InvalidMoveError

class C4GameEngine:
    ROWS = 6
    COLUMNS = 7
    EMPTY_SPACE = '_'
    PLAYER_ONE = 'O'
    PLAYER_TWO = 'X'
    IN_A_ROW = 4
    PLAYERS = [PLAYER_ONE, PLAYER_TWO]

    def __init__(self):
        self.board_state = [[self.EMPTY_SPACE for _ in range(7)] for _ in range(6)]
        self.player = self.PLAYER_ONE
        self.column_heights = {n: self.ROWS - 1 for n in range(self.COLUMNS)}
        self.moves = 0

    def get_state(self):
        return self.board_state

    def change_player(self):
        self.player = self.PLAYER_TWO if (self.player == self.PLAYER_ONE) else self.PLAYER_ONE

    def change_column_height(self, column):
        self.column_heights[column] -= 1

    def play_move(self, column):
        if not self.is_move_valid(column):
            raise InvalidMoveError (f"Column {column} already full")

        self.board_state[self.column_heights[column]][column] = self.player
        self.change_player()
        self.change_column_height(column)
        self.moves += 1

    def is_move_valid(self, column):
        if column > self.COLUMNS - 1:
            return False
        validity = self.column_heights[column] >= 0
        return validity

    def check_horizontal(self, player):
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        win_condition = [player for _ in range(in_a_row)]
        for row in board:
            for offset in range(self.COLUMNS - in_a_row + 1):
                row_extract = row[offset: offset + in_a_row]
                if  row_extract == win_condition:
                    return True
        return False

    def check_vertical(self, player):
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        win_condition = [player for _ in range(in_a_row)]
        for col in range(self.COLUMNS):
            for offset in range(self.ROWS - in_a_row + 1):
                col_extract = [board[r][col] for r in range(offset, offset + in_a_row)]
                if col_extract == win_condition:
                    return True
        return False

    def check_negative_diag(self, player):
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        win_condition = [player for _ in range(in_a_row)]
        for col_offset in range(self.COLUMNS - in_a_row + 1):
            for row_offset in range(self.ROWS - in_a_row + 1):
                extract = [board[row_offset + v][col_offset + v] for v in range(in_a_row)]
                if extract == win_condition:
                    return True
        return False

    def check_positive_diag(self, player):
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        win_condition = [player for _ in range(in_a_row)]
        for col_offset in range(self.COLUMNS - in_a_row + 1):
            for row_offset in range(self.ROWS - in_a_row + 1):
                row_start = self.ROWS - 1 - row_offset
                extract = [board[row_start - v][col_offset + v] for v in range(in_a_row)]
                if extract == win_condition:
                    return True
        return False

    def winning_state(self, player):
        return any([self.check_horizontal(player),
                    self.check_vertical(player),
                    self.check_negative_diag(player),
                    self.check_positive_diag(player)])
    


    def __str__(self):
        board = self.get_state()
        output = ''
        for row in board:
            output += '|'.join(row)
            output += '\n'
        return output

    def reset(self):
        self.__init__()
