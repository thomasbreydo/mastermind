#!/usr/bin/env python3

import mastermind

ALL_ALLGORITHMS = mastermind.Game.ALGORITHMS

def main():
    '''
    Ask if game should play itself.

    If yes --> guess user's code.
    If no --> play alone.
    '''
    while True:
        try:
            slots = int(input('How many slots? '))
            break
        except:
            print('The number of slots must be an integer')
    colors_input = input('What are the colors (separate with commas)? ')
    colors = list(map(lambda x: x.strip(), colors_input.split(',')))
    while True:
        algorithm = input(
            f'Algorithm ({"/".join(ALL_ALLGORITHMS)})? '
        )
        if algorithm in ALL_ALLGORITHMS:
            break
        else:
            print(f'The "{algorithm}"" algorithm is currently unsupported')
    while True:
        alone_input = input('Self game (y/n)? ').lower()
        if alone_input == 'y':
            alone = True
            break
        elif alone_input == 'n':
            alone = False
            break

    if not alone:
        game = mastermind.Game(slots, colors)
        turn = 0
        print(
'''

----------------

Welcome to MasterMind! You've asked me guess your secret code. After each
guess, I'll prompt you to enter how many black and white pegs my guess got.

Press <enter> or <return> at any time to go back.
''')
        
        # main loop
        while len(game.possibilities) > 1:
            turn += 1
            print(f'\nMy guess is {game.guess}.')
            try:
                b = int(input('How many black pegs? '))
                w = int(input('How many white pegs? '))
            except ValueError: # non-int input, treated as <return/enter>
                print('\n\nGoing back . . .\n')
                game.back()
                turn -= 1
                continue # skip trimming and just go back
            try:
                game.new_guess((b, w), algorithm)
            except: # not enough possibilities
                print("\n\nOne of your inputs was wrong. I'm going back one "
                      "move. To go back further, press <enter> or <return> "
                      "at any time.\n")
                turn -= 1
                game.back()
                continue

        print(f'\n\nDone! Your code was {game.guess}, and I guessed it in '
              f'{turn} moves.')

    else:
        gamecount = int(input('How many games? '))
        self_game = mastermind.SelfGame(slots, colors)
        df = self_game.play(gamecount, algorithm)

        # dislpay statistics
        print('\n\n-- General --')
        print(f'\nTotal games played:\n{len(df.index)}')
        print(f'\nAlgorithm used:\n{df["Algorithm"].iloc[0]}')
        print(f'\nAverage number of turns per game:\
{df.notna().sum(axis=1).mean() / 3}')
        for turn in df.columns.levels[0].drop(['Algorithm', 'Secret']):
            turndf = df[turn]
            eliminated = (turndf["Start Possibilities"] 
                        - turndf["End Possibilities"])
            print('\n')
            print('--', turn, '--')
            print(f'\nAverage time:\n{turndf["Time"].mean()}')
            print(f'\nAverage eliminated:\n{eliminated.mean()}')
            print(f'\nAverage percent eliminated:\
{100 * (eliminated / turndf["Start Possibilities"]).mean():.4}%')

if __name__ == '__main__':
    main()