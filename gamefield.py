# -*- coding: utf-8 -*-


class GameField(object):
    def __init__(self, height=15, width=15):
        self.width = width
        self.height = height
        self.mode = 1
        self.current_player = 1
        self.player_name_1 = 'Player1'
        self.player_name_2 = 'Player2'
        self.player_name_3 = 'Computer'
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
        self.current['row'] = 7
        self.current['col'] = 7
        self.mode = 1
        self.player_name_1 = 'Player1'
        self.player_name_2 = 'Player2'
        self.current_player = 1
        return 0

    def addai(self):
        """Reset the chessboard for game with AI"""
        for j in xrange(self.height):
            for i in xrange(self.width):
                self.field[i][j] = 0
        self.current['row'] = 7
        self.current['col'] = 7
        self.mode = 2
        self.player_name_1 = 'You'
        self.player_name_3 = 'Computer'
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
                        return player_id
        return 0

    def draw(self, screen):
        """Draw the Game Field"""
        import curses
        import time
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        help_string1 = '\n(W)Up        (S)Down       (A)Left       (D)Right\n'
        help_string2 = '\n(C)Set\n(R)Start 2 players mode\n(T)Restart single mode\n(Q)Quit\n'

        def draw_lines():
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if self.field[i][j] == 1: screen.addstr('X', curses.color_pair(1))
                    elif self.field[i][j] == 2 or self.field[i][j] == 3: screen.addstr('O', curses.color_pair(2))
                    elif self.current['row']==i and self.current['col']==j: screen.addstr('?')
                    elif self.field[i][j] == 0: screen.addstr(' ')
                    if (i*15+j+1)%15 == 0: screen.addstr('\n')
                    else: screen.addstr('---')
                if i in xrange(self.height-1):
                    screen.addstr('|   '*14+'|'+'\n')
        screen.clear()
        try:
            if self.is_win():
                if self.current_player == 2 or self.current_player == 3: winner_name = self.player_name_1
                else: winner_name = self.player_name_2
                screen.addstr('  Winner: %s' % winner_name + ' !!!!\n\n', curses.color_pair(4))
            else:
                if self.current_player == 2: now_name = self.player_name_2
                elif self.current_player == 3: now_name = self.player_name_3
                else: now_name = self.player_name_1
                if self.current_player != 3:
                    screen.addstr('It\'s Your Turn !!\n', curses.color_pair(self.current_player))
                    screen.addstr('Now: %s \n' % now_name, curses.color_pair(self.current_player))
                else:
                    screen.addstr('Computer is thinking...\n\n', curses.color_pair(2))
            draw_lines()
            screen.addstr(help_string1)
            screen.addstr(help_string2)
        except Exception:
            screen.clear()
            screen.addstr('Window too small... Press \'Q/q\' to return to quit', curses.color_pair(3))

    def is_step_legal(self, direction):
        after_row = self.current['row']
        after_col = self.current['col']
        if direction == 'Left': after_col-=1
        elif direction == 'Right': after_col+=1
        elif direction == 'Up': after_row-=1
        elif direction == 'Down': after_row+=1
        return (after_row in xrange(15)) and (after_col in xrange(15))

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

    def aimove(self):
        field = self.field
        # 1. winning5: 100 p
        # 2. living4: 90 p
        # 3. double dead4: 90 p
        # 4. living4 dead3: 90 p
        # 5. double living3: 80 p
        # 6. dead3 living3: 70 p
        # 7. dead4: 60 p
        # 8. living3: 50 p
        # 9. double living2: 40 p
        # 10. dead3: 30 p
        # 11. living2: 20 p
        # 12. dead2: 10 p
        # 13. single: 0 p
        points = 0

        def check_one(row, col, field):
            """Check for winning 5"""
            field[row][col] = 3
            moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
            for i in xrange(5):
                for j in xrange(5):
                    if field[i][j] == 3:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(5):
                                if field[x][y] != 3:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == 5:
                                return True
            return False

       def check_two(row, col, field):
           """Check for living 4"""
           field[row][col] = 3
           moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
           for i in xrange(5):
               for j in xrange(5):
                   if field[i][j] == 3:
                       for move in moves:
                           x, y = i, j
                           chessman_count = 0
                           for m in xrange(6):
                               if chessman_count == 0:
                                   if field[x][y] != 0:
                                       break
                               elif chessman_count>0 and chessman_count<5:
                                   if field[x][y] != 3:
                                       break
                               elif chessman_count == 5:
                                   if field[x][y] != 0:
                                       break
                               x += move[0]
                               y += move[1]
                               chessman_count += 1
                           if chessman_count == 6:
                               return True
            return False

        def check_three(row, col, field):
            """Check for double dead 4"""
            field[row][col] = 3
            moves = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
            dead_four = 0
            for i in xrange(5):
                for j in xrange(5):
                    if field[i][j] == 1:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(6):
                                if chessman_count == 0:
                                    if field[x][y] != 1:
                                        break
                                elif chessman_count>0 and chessman_count<5:
                                    if field[x][y] != 3:
                                        break
                                elif chessman_count == 5:
                                    if field[x][y] != 0:
                                        break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == 6:
                                dead_four += 1
                                if dead_four == 2:
                                    return True
            return False
