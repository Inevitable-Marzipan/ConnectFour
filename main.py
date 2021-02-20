from connect_four.game_engine import C4GameEngine

def main():
    eng = C4GameEngine()
    print(*eng.get_state(), sep='\n')
    #print(eng)
    print('\n')
    player1 = eng.PLAYER_ONE
    player2 = eng.PLAYER_TWO
    while not any([eng.winning_state(player1), eng.winning_state(player2)]):
        valid = False
        while not valid:
            move = input('Which column to play: ')
            move = int(move)
            if eng.is_move_valid(move):
                valid = True

        eng.play_move(move)
        print('\n')
        print(*eng.get_state(), sep='\n')
        #print(eng)
        print('\n')

    print('Player Won')

if __name__ == '__main__':
    main()
