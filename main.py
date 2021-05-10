from connect_four.game_engine import C4GameEngine
from connect_four.TwoPlayerGame import TwoPlayerGame
from connect_four.Players import HumanPlayer, RandomPlayer, MinimaxPlayer
from collections import Counter
import matplotlib.pyplot as plt

def main():
    #p1 = HumanPlayer()
    p1 = RandomPlayer()
    #p2 = HumanPlayer()
    #p2 = RandomPlayer()
    p2 = MinimaxPlayer(depth=3)
    env = C4GameEngine()

    rounds = 10000
    outcomes = []
    winners = []
    round_lengths = []
    for _ in range(rounds):
        game = TwoPlayerGame(env, [p1, p2], verbose=False)
        game.play()
        outcomes.append(game.env)
        winners.append(game.winner)
        round_lengths.append(game.rounds)
    
    #for outcome in outcomes:
    #    pass
    #    print(outcome)
    
    c = Counter(winners)
    print(c.most_common())
    r = Counter(round_lengths)
    print(sorted(r.items()))
    plt.hist(round_lengths)
    plt.savefig('hist.png')

if __name__ == '__main__':
    main()