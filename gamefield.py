# -*- coding: utf-8 -*-


class GameField(object):
    def __init__(self, height=15, width=15):

        self.width = width
        self.height = height
        self.player1_steps = 0
        self.player2_steps = 0
        self.field = [[0 for i in xrange(width)] for j in xrange(height)]
        self.five_in_a_row = {}
        self.current = (7, 7)
        self.winner = 0
        self.reset()

    def get(self, row, col):
        """Return state of the chessboard"""
        if (row in xrange(self.height) and col in xrange(self.width)):
            return self.field[row][col]
        else:
            return 0

    def reset(self):
        """Reset the chessboard for next round"""
        for j in xrange(self.height):
            for i in xrange(self.width):
                self.field[i][j] = 0
        self.player1_steps = 0
        self.player2_steps = 0
        return 0

    def is_win(self):
        field = self.field
        # Four diffrent directions to check
        moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
        for i in xrange(self.height):
            for j in xrange(self.width):
                # No chessman on this point
                if field[i][j] == 0:
                    continue
                player_id = field[i][j]
                for move in moves:
                    x, y = i, j
                    chessman_count = 0
                    for m in xrange(5):
                        if self.get(x, y) != player_id:
                            break
                        x += move[0]
                        y += move[1]
                        count += 1
                    if count == 5:
                        p, q = i, j
                        for n in xrange(5):
                            self.five_in_a_row[(p, q)] = 1
                            p += d[0]
                            q += d[1]
                        return player_id
        return 0

    def draw(self, screen, winner=None):
        """Draw the Game Field"""
        import curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        help_string1 = '\n(W)Up (S)Down (A)Left (D)Right\n'
        help_string2 = '\n(C)onfirm   (R)estart   (Q)uit\n'
        self.field[7][7] = 1
        self.field[7][6] = 1
        self.field[7][5] = 1
        self.field[7][8] = 1
        self.field[7][9] = 1
        self.field[6][7] = 1
        self.field[9][7] = 1
        self.field[4][3] = 1
        self.field[5][6] = 1
        self.field[6][5] = 1
        self.field[3][7] = 1
        self.field[2][7] = 1
        self.field[2][3] = 2
        self.field[8][10] = 2
        self.field[6][5] = 2
        self.field[5][4] = 2
        self.field[3][6] = 2
        self.field[5][5] = 2
        self.field[2][4] = 2
        self.field[2][11] = 2
        self.field[7][10] = 2
        self.field[8][10] = 2
        self.field[6][10] = 2
        self.player1_steps = 11
        self.player2_steps = 10
        self.winner = 'Player1'
        if winner:
            win_string = winner.capitalize() + ' Wins!'
        else:
            win_string = '\nERROR: No Winner!!!\n'

        def draw_lines():
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if self.field[i][j] == 0: screen.addstr(' ')
                    elif self.field[i][j] == 1: screen.addstr('X', curses.color_pair(1))
                    elif self.field[i][j] == 2: screen.addstr('O', curses.color_pair(2))
                    else: screen.addstr('?')
                    if (i*15+j+1)%15 == 0: screen.addstr('\n')
                    else: screen.addstr('---')
                if i in xrange(self.height-1):
                    screen.addstr('|   '*14+'|'+'\n')

        screen.clear()
        screen.addstr('Player1: %d steps ' % self.player1_steps, curses.color_pair(1))
        screen.addstr(' '*3)
        screen.addstr('Player2: %d steps ' % self.player2_steps, curses.color_pair(2))
        if self.winner != 0:
            screen.addstr('  Winner: ' +  self.winner + ' !!!!')
        screen.addstr('\n')
        draw_lines()
        screen.addstr(help_string1)
        screen.addstr(help_string2)

    def is_step_legal(row=-1, col=-1):
        if row not in xrange(15) or col not in xrange(15):
            return False
        if self.field[row][col] == 0:
            return True

