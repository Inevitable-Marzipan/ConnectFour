import random
import copy

class Player:
    def get_move(self, env):
        raise NotImplementedError

class HumanPlayer(Player):
    def get_move(self, env):
        allowed_moves = env.allowed_moves
        while True:
            move = input('Input Player Move: ')
            try:
                move = int(move)
            except ValueError:
                continue
            if move in allowed_moves:
                break
        return move

class RandomPlayer(Player):
    def get_move(self, env):
        allowed_moves = env.allowed_moves
        move = random.choice(list(allowed_moves))
        return move

def minimax(env, depth, maximizing_player):
    if (depth == 0) or (env.done):
        return env.score()
    if maximizing_player:
        value = -1000000
        for move in env.allowed_moves:
            env_copy = copy.deepcopy(env)
            search_val = minimax(env_copy.play_move(move), depth - 1, False)
            value = max(value, search_val)
        return value
    else:
        value = 1000000
        for move in env.allowed_moves:
            env_copy = copy.deepcopy(env)
            search_val = minimax(env_copy.play_move(move), depth - 1, True)
            value = max(value, search_val)
        return value

class MinimaxPlayer(Player):
    def __init__(self, depth=1):
        self.depth = depth

    def get_move(self, env):
        best_move = None
        best_value = 10000000
        for move in env.allowed_moves:
            env = copy.deepcopy(env)
            move_value = minimax(env.play_move(move), self.depth -1, False)
            if move_value < best_value:
                best_move = move
                best_value = move_value
        return best_move
