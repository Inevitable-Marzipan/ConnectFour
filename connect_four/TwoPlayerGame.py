import copy

class TwoPlayerGame:
    def __init__(self, env, players, first_player=0, **kwargs):
        self.players = players
        self.player_idx = first_player
        self.env = copy.deepcopy(env)
        self.rounds = 0
        self.done = False
        self.winner = None
        verbose = kwargs.get('verbose', False)
        self.print = print if verbose else lambda *a, **k: None

    def play_turn(self):
        current_state = self.env
        move = self.players[self.player_idx].get_move(current_state)
        self.env.play_move(move)
        self.done = self.env.done
        self.winner = self.player_idx
        self._switch_player()

    def play(self, rounds=1000):

        for rnd in range(rounds):
            self.print(self.env)
            if self.done:
                self.rounds = rnd
                break
            self.play_turn()
        self.print('Player Won')

    def _switch_player(self):
        self.player_idx = 1 if (self.player_idx == 0) else 0
