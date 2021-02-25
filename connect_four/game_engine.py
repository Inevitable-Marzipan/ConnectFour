from .errors import InvalidMoveError

class C4GameEngine:
    ROWS = 6
    COLUMNS = 7
    EMPTY = '_'
    PLAYER_ONE = 'O'
    PLAYER_TWO = 'X'
    IN_A_ROW = 4
    PLAYERS = [PLAYER_ONE, PLAYER_TWO]

    def __init__(self):
        self.board_state = [[self.EMPTY for _ in range(7)] for _ in range(6)]
        self.player = self.PLAYER_ONE
        self.column_heights = {n: self.ROWS - 1 for n in range(self.COLUMNS)}
        self.moves = 0
        self.allowed_moves = set(range(self.COLUMNS))
        self.done = False

    def get_state(self):
        return self.board_state

    def change_player(self):
        self.player = self.PLAYER_TWO if (self.player == self.PLAYER_ONE) else self.PLAYER_ONE

    def change_column_height(self, column):
        self.column_heights[column] -= 1
        if self.column_heights[column] < 0:
            self.allowed_moves.remove(column)

    def play_move(self, column):
        if not self.is_move_valid(column):
            raise InvalidMoveError (f"Column {column} already full")

        self.board_state[self.column_heights[column]][column] = self.player
        self.change_column_height(column)
        self.moves += 1
        won = self.winning_state(self.player)
        self.done = won or (self.moves == self.COLUMNS * self.ROWS)
        self.change_player()
        return self

    def is_move_valid(self, column):
        if column > self.COLUMNS - 1:
            return False
        return column in self.allowed_moves

    def get_horizontal(self):
        arrs = []
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        for row in board:
            for offset in range(self.COLUMNS - in_a_row + 1):
                row_extract = row[offset: offset + in_a_row]
                arrs.append(row_extract)
        return arrs

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

    def get_vertical(self):
        arrs = []
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        for col in range(self.COLUMNS):
            for offset in range(self.ROWS - in_a_row + 1):
                col_extract = [board[r][col] for r in range(offset, offset + in_a_row)]
                arrs.append(col_extract)
        return arrs

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

    def get_negative_diag(self):
        arrs = []
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        for col_offset in range(self.COLUMNS - in_a_row + 1):
            for row_offset in range(self.ROWS - in_a_row + 1):
                extract = [board[row_offset + v][col_offset + v] for v in range(in_a_row)]
                arrs.append(extract)
        return arrs

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

    def get_positive_diag(self):
        arrs = []
        in_a_row = self.IN_A_ROW
        board = self.get_state()
        for col_offset in range(self.COLUMNS - in_a_row + 1):
            for row_offset in range(self.ROWS - in_a_row + 1):
                row_start = self.ROWS - 1 - row_offset
                extract = [board[row_start - v][col_offset + v] for v in range(in_a_row)]
                arrs.append(extract)
        return arrs

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

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_ONE
        if piece == self.PLAYER_ONE:
            opp_piece = self.PLAYER_TWO

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 4:
            score -= 100
        elif window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 10

        return score

    def score(self):

        score = 0

        centre_col = self.COLUMNS // 2
        board = self.get_state()
        center_array = [board[r][centre_col] for r in range(self.ROWS)]
        center_count = center_array.count(self.player)
        score += center_count * 3

        horizontal = self.get_horizontal()
        vertical = self.get_vertical()
        negative_diag = self.get_negative_diag()
        positive_diag = self.get_positive_diag()

        score += sum([self.evaluate_window(window, self.player) for window in horizontal])
        score += sum([self.evaluate_window(window, self.player) for window in vertical])
        score += sum([self.evaluate_window(window, self.player) for window in negative_diag])
        score += sum([self.evaluate_window(window, self.player) for window in positive_diag])

        return score
