# !/usr/bin/env python
# -*- coding: utf-8 -*-


import curses
from collections import defaultdict
from gamefield import GameField


actions = ['Up', 'Left', 'Down', 'Right', 'Confirm', 'Restart', 'AddAI', 'Quit']
letters = 'WASDCRTQ'
letter_codes = [ord(ch) for ch in letters+letters.lower()]
actions_dict = dict(zip(letter_codes, actions*2))


def get_user_action(keyboard):
    """Get User's Input From the Console"""
    # Illegal input
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def main(stdscr):
    def init():
        game_field.reset()
        return 'Game'

    def addai():
        game_field.addai()
        return 'Game'

    def not_game(state):
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'] = 'Restart'
        responses['AddAI'] = 'AddAI'
        responses['Quit'] = 'Quit'
        return responses[action]

    def game():
        import time
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'AddAI':
            return 'AddAI'
        if action == 'Quit':
            return 'Quit'
        if game_field.current_player == 3:
            game_field.aimove()
            if game_field.is_win():
                return 'Win'
            game_field.current_player = 1
            return 'Game'
        if action == 'Confirm':
            if game_field.field[game_field.current['row']][game_field.current['col']] == 0:
                game_field.field[game_field.current['row']][game_field.current['col']] = game_field.current_player
                if game_field.is_win():
                    return 'Win'
                if game_field.mode == 1:
                    if game_field.current_player == 1: game_field.current_player = 2
                    else: game_field.current_player = 1
                elif game_field.mode == 2:
                    game_field.current_player = 3
            return 'Game'
        if game_field.move(action):
            game_field.draw(stdscr)
            return 'Game'

    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Game': game,
            'Confirm': game,
            'AddAI': addai
            }
    state = 'Init'

    game_field = GameField()
    state = 'Init'

    while state != 'Quit':
        try:
            state = state_actions[state]()
        except KeyError:
            pass

curses.wrapper(main)
