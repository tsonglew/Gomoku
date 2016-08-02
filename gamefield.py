# -*- coding: utf-8 -*-


class GameField(object):
    def __init__(self, height=15, width=15):
        self.width = width
        self.height = height
        self.field = [[0 for i in xrange(width)] for j in xrange(height)]
        self.five_in_a_row = {}
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
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '(C)onfirm   (R)estart   (Q)uit'
        if winner:
            win_string = winner.capitalize() + ' Wins!'
        else:
            win_string = 'ERROR: No Winner!!!'

        def draw_lines():
            cross = '*---' * 14 + '*'
            down = '|  ' * 14 + '|'
            screen.addstr(cross + '\n')
            for i in xrange(self.width-1):
                screen.addstr(down + '\n')
                screen.addstr(cross + '\n')

        def is_step_legal(row=-1, col=-1):
            if game_field.field[row][col] == 0:
                return True
