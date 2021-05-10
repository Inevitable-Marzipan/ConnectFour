from connect_four.game_engine import C4GameEngine
board = [
['_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_'],
['_', '_', '_', '_', '_', '_', '_'],
['X', '_', '_', '_', '_', '_', '_'],
['X', '_', '_', '_', '_', '_', '_'],
['O', 'O', 'O', '_', '_', '_', '_']]

eng = C4GameEngine()
eng.board_state = board
print(eng.score())
eng.change_player()
print(eng.score())