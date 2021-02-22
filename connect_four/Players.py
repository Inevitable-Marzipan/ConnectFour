import random

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