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
        return (None, env.score())
    if maximizing_player:
        value = -1000000
        best_move = None
        for move in env.allowed_moves:
            env_copy = copy.deepcopy(env)
            search_val = minimax(env_copy.play_move(move), depth - 1, False)[1]
            if search_val > value:
                value = search_val
                best_move = move
        return best_move, value
    else:
        value = 1000000
        best_move = None
        for move in env.allowed_moves:
            env_copy = copy.deepcopy(env)
            search_val = minimax(env_copy.play_move(move), depth - 1, True)[1]
            if search_val < value:
                value = search_val
                best_move = move
        return best_move, value

def negamax(env, depth):
    if (depth == 0) or (env.done):
        return (None, env.score())
    value = -1000000
    best_move = None
    for move in env.allowed_moves:
        env_copy = copy.deepcopy(env)
        search_val = -negamax(env_copy.play_move(move), depth - 1)[1]
        if search_val > value:
            value = search_val
            best_move = move
    return best_move, value

class MinimaxPlayer(Player):
    def __init__(self, depth=1):
        self.depth = depth

    def get_move(self, env):
        root_env = env
        env = copy.deepcopy(root_env)
        move, _ = negamax(env, self.depth)

        return move
