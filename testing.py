from connect_four.game_engine import C4GameEngine
from connect_four.TwoPlayerGame import TwoPlayerGame
from connect_four.Players import HumanPlayer, RandomPlayer, MinimaxPlayer
import copy

def minimax(env, depth, maximizingPlayer):
    if (depth == 0) or (env.done):
        return env.score()
    elif maximizingPlayer:
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

def main():
    p1 = HumanPlayer()
    #p1 = RandomPlayer()
    #p2 = HumanPlayer()
    #p2 = RandomPlayer()
    p2 = MinimaxPlayer(depth=3)
    env = C4GameEngine()
    game = TwoPlayerGame(env, [p1, p2], verbose=True)
    game.play()


if __name__ == '__main__':
    main()