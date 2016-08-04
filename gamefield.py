# -*- coding: utf-8 -*-


class GameField(object):
    def __init__(self, height=15, width=15):
        self.width = width
        self.height = height
        self.player1_steps = 0
        self.player2_steps = 0
        self.current_player = 1
        self.field = [[0 for i in xrange(width)] for j in xrange(height)]
        self.current = {'row':7, 'col':7}
        self.winner = 0
        self.reset()

    def get(self, row, col):
        """Return state of selected point"""
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
        self.current['row'] = 7
        self.current['col'] = 7
        self.current_player = 1
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
                        chessman_count += 1
                    if chessman_count == 5:
                        p, q = i, j
                        for n in xrange(5):
                            p += move[0]
                            q += move[1]
                        return player_id
        return 0

    def draw(self, screen):
        """Draw the Game Field"""
        import curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        help_string1 = '\n(W)Up (S)Down (A)Left (D)Right\n'
        help_string2 = '\n(C)onfirm   (R)estart   (Q)uit\n'

        def draw_lines():
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if self.field[i][j] == 1: screen.addstr('X', curses.color_pair(1))
                    elif self.field[i][j] == 2: screen.addstr('O', curses.color_pair(2))
                    elif self.current['row']==i and self.current['col']==j: screen.addstr('?')
                    elif self.field[i][j] == 0: screen.addstr(' ')
                    if (i*15+j+1)%15 == 0: screen.addstr('\n')
                    else: screen.addstr('---')
                if i in xrange(self.height-1):
                    screen.addstr('|   '*14+'|'+'\n')
        screen.clear()
        try:
            if self.is_win():
                if self.current_player == 1: self.current_player+=1
                else: self.current_player-=1
                screen.addstr('  Winner: Player%d' % self.current_player + ' !!!!', curses.color_pair(1))
            else:
                screen.addstr('   It\'s Your Turn !!', curses.color_pair(2))
            screen.addstr('\n')
            screen.addstr('Now: Player%d \n' % self.current_player)
            draw_lines()
            screen.addstr(help_string1)
            screen.addstr(help_string2)
        except Exception:
            screen.clear()
            screen.addstr('Screen is to small! Press \'Q/q\' to return to your teminal', curses.color_pair(1))

    def is_step_legal(self, direction):
        after_row = self.current['row']
        after_col = self.current['col']
        if direction == 'Left': after_col-=1
        elif direction == 'Right': after_col+=1
        elif direction == 'Up': after_row-=1
        elif direction == 'Down': after_row+=1
        return  after_row in xrange(15) and after_col in xrange(15)

    def move(self, direction):
        moves = ['Left', 'Right', 'Up', 'Down']
        def do_move(direction):
            if direction == 'Left': self.current['col']-=1
            elif direction == 'Right': self.current['col']+=1
            elif direction == 'Up': self.current['row']-=1
            elif direction == 'Down': self.current['row']+=1

        if direction in moves:
            if self.is_step_legal(direction):
                do_move(direction)
                return True
            else:
                return False
