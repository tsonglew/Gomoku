# !/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
from collections import defaultdict
from gamefield import GameField


actions = ['Up', 'Left', 'Down', 'Right', 'Confirm', 'Restart', 'Quit']
letters = 'WASDCRQ'
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

    def not_game(state):
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'] = 'Restart'
        responses['Quit'] = 'Quit'
        return responses[action]

    def game():
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Quit':
            return 'Quit'
        if action == 'Confirm':
            game_field.field[game_field.current['row']][game_field.current['col']] = game_field.current_player
            if game_field.current_player == 1: game_field.current_player = 2
            else: game_field.current_player = 1
        if game_field.move(action):
            game_field.draw(stdscr)
            if game_field.is_win():
                return 'Win'
        return 'Game'

    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Game': game,
            'Confirm': game
            }
    state = 'Init'

    game_field = GameField()
    state = 'Init'

    while state != 'Quit':
        state = state_actions[state]()

curses.wrapper(main)
