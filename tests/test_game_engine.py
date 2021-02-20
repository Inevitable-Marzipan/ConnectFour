import pytest
from connect_four.game_engine import C4GameEngine
from connect_four.errors import InvalidMoveError

COLUMNS = C4GameEngine.COLUMNS
ROWS = C4GameEngine.ROWS

def test_C4GameEngine_initial_state():
    eng = C4GameEngine()
    eng_state = eng.get_state()
    empty_space = C4GameEngine.EMPTY_SPACE

    initial_board = [[empty_space for _ in range(COLUMNS)] for _ in range(ROWS)]

    assert eng_state == initial_board

@pytest.mark.parametrize("first_move", range(COLUMNS))
def test_C4GameEngine_first_move(first_move):
    eng = C4GameEngine()
    eng.play_move(first_move)

    bottom_row = [C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)]
    bottom_row[first_move] = C4GameEngine.PLAYER_ONE
    rest_of_board = [[C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)] for _ in range(ROWS - 1)]
    expected_state = rest_of_board + [bottom_row]

    assert eng.get_state() == expected_state

def test_C4GameEngine_change_player_one_move():
    eng = C4GameEngine()
    eng.play_move(0)
    current_player = eng.player

    expected_player = C4GameEngine.PLAYER_TWO

    assert current_player == expected_player

def test_C4GameEngine_change_player_two_moves():
    eng = C4GameEngine()
    eng.play_move(0)
    eng.play_move(1)
    current_player = eng.player

    expected_player = C4GameEngine.PLAYER_ONE

    assert current_player == expected_player

@pytest.mark.parametrize("column", range(C4GameEngine.COLUMNS))
def test_C4GameEngine_two_moves_same_position(column):
    eng = C4GameEngine()
    eng.play_move(column)
    eng.play_move(column)
    board_state = eng.get_state()


    bottom_row = [C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)]
    bottom_row[column] = C4GameEngine.PLAYER_ONE
    next_up_row = [C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)]
    next_up_row[column] = C4GameEngine.PLAYER_TWO
    rest_of_board = [[C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)] for _ in range(ROWS - 2)]
    expected_state = rest_of_board + [next_up_row] + [bottom_row]

    assert board_state == expected_state

@pytest.mark.parametrize("row", range(ROWS - 1))
@pytest.mark.parametrize("column", range(C4GameEngine.COLUMNS))
def test_C4GameEngine_check_valid_move_column_not_full(row, column):
    eng = C4GameEngine()
    for _ in range(row):
        eng.play_move(column)
    is_move_valid = eng.is_move_valid(column)

    expected_validity = True

    assert is_move_valid == expected_validity

@pytest.mark.parametrize("column", range(COLUMNS))
def test_C4GameEngine_check_valid_move_column_full(column):
    eng = C4GameEngine()
    for _ in range(C4GameEngine.ROWS):
        eng.play_move(column)
    is_move_valid = eng.is_move_valid(column)

    expected_validity = False

    assert is_move_valid == expected_validity

def test_C4GameEngine_check_valid_move_invalid_column():
    eng = C4GameEngine()
    is_move_valid = eng.is_move_valid(COLUMNS)

    expected_validity = False

    assert is_move_valid == expected_validity

@pytest.mark.parametrize("column", range(COLUMNS))
def test_C4GameEngine_raise_error_invalid_move(column):
    eng = C4GameEngine()
    for _ in range(C4GameEngine.ROWS):
        eng.play_move(column)

    with pytest.raises(InvalidMoveError):
        eng.play_move(column)

def test_C4GameEngine_reset_player():
    eng = C4GameEngine()
    eng.play_move(0)
    eng.reset()
    player = eng.player

    expected_player = C4GameEngine.PLAYER_ONE

    assert player == expected_player

def test_C4GameEngine_reset_board():
    eng = C4GameEngine()
    eng.play_move(0)
    eng.reset()
    board_state = eng.get_state()

    expected_state = [[C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)] for _ in range(ROWS)]

    assert board_state == expected_state

@pytest.mark.parametrize("column", range(COLUMNS))
def test_C4GameEngine_reset_column_hieghts(column):
    eng = C4GameEngine()
    eng.play_move(column)
    eng.reset()
    column_heights = eng.column_heights

    expected_column_heights = {n: ROWS - 1 for n in range(COLUMNS)}

    assert column_heights == expected_column_heights

@pytest.mark.parametrize("player", [C4GameEngine.PLAYER_ONE, C4GameEngine.PLAYER_TWO])
def test_C4GameEngine_empty_board_winning_state(player):
    eng = C4GameEngine()

    assert eng.winning_state(player) == False

@pytest.mark.parametrize("player", [C4GameEngine.PLAYER_ONE, C4GameEngine.PLAYER_TWO])
@pytest.mark.parametrize("row", range(ROWS))
@pytest.mark.parametrize("offset", range(COLUMNS - C4GameEngine.IN_A_ROW + 1))
def test_C4GameEngine_winning_horizontal_states(player, row, offset):
    eng = C4GameEngine()
    in_a_row = C4GameEngine.IN_A_ROW

    winning_row = [C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)]
    winning_row[offset: offset + in_a_row] = [player for _ in range(in_a_row)]
    winning_board = [[C4GameEngine.EMPTY_SPACE for _ in range(COLUMNS)] for _ in range(ROWS)]
    winning_board[row] = winning_row
    eng.board_state = winning_board

    assert eng.winning_state(player)

@pytest.mark.parametrize("player", [C4GameEngine.PLAYER_ONE, C4GameEngine.PLAYER_TWO])
@pytest.mark.parametrize("column", range(COLUMNS))
@pytest.mark.parametrize("offset", range(ROWS - C4GameEngine.IN_A_ROW + 1))
def test_C4GameEngine_winning_vertical_states(player, column, offset):
    eng = C4GameEngine()
    in_a_row = C4GameEngine.IN_A_ROW
    empty_space = C4GameEngine.EMPTY_SPACE

    winning_board = [[empty_space for _ in range(COLUMNS)] for _ in range(ROWS)]
    for row in range(offset, offset + in_a_row):
        winning_board[row][column] = player
    eng.board_state = winning_board

    assert eng.winning_state(player) == True

@pytest.mark.parametrize("player", [C4GameEngine.PLAYER_ONE, C4GameEngine.PLAYER_TWO])
@pytest.mark.parametrize("col_offset", range(COLUMNS - C4GameEngine.IN_A_ROW + 1))
@pytest.mark.parametrize("row_offset", range(ROWS - C4GameEngine.IN_A_ROW + 1))
def test_C4GameEngine_winning_negative_diagonal_states(player, col_offset, row_offset):
    eng = C4GameEngine()
    in_a_row = C4GameEngine.IN_A_ROW
    empty_space = C4GameEngine.EMPTY_SPACE

    winning_board = [[empty_space for _ in range(COLUMNS)] for _ in range(ROWS)]
    for val in range(in_a_row):
        winning_board[row_offset + val][col_offset + val] = player
    eng.board_state = winning_board

    assert eng.winning_state(player) == True

#@pytest.mark.skip()
@pytest.mark.parametrize("player", [C4GameEngine.PLAYER_ONE, C4GameEngine.PLAYER_TWO])
@pytest.mark.parametrize("col_offset", range(COLUMNS - C4GameEngine.IN_A_ROW + 1))
@pytest.mark.parametrize("row_offset", range(ROWS - C4GameEngine.IN_A_ROW + 1))
def test_C4GameEngine_winning_positive_diagonal_states(player, col_offset, row_offset):
    eng = C4GameEngine()
    in_a_row = C4GameEngine.IN_A_ROW
    empty_space = C4GameEngine.EMPTY_SPACE

    winning_board = [[empty_space for _ in range(COLUMNS)] for _ in range(ROWS)]
    for val in range(in_a_row):
        col_idx = col_offset + val
        row_idx = (ROWS - 1) - val - row_offset
        winning_board[row_idx][col_idx] = player
    eng.board_state = winning_board

    assert eng.winning_state(player) == True

@pytest.mark.skip()
def test_C4GameEngine_winning_state(player):
    eng = C4GameEngine()

    eng.board_state = []

    assert eng.winning_state(player) == True
