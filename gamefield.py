# -*- coding: utf-8 -*-


class GameField(object):
    def __init__(self, height=15, width=15):
        self.width = width
        self.height = height
        self.mode = 1
        self.point = 0
        self.concede = 0
        self.current_player = 1
        self.player_name_1 = 'Player1'
        self.player_name_2 = 'Player2'
        self.player_name_3 = 'Computer'
        self.field = [[0 for i in xrange(width)] for j in xrange(height)]
        self.current = {'row':7, 'col':7}
        self.winner = 0
        self.reset()


    def show(self):
        """Show the chessboard"""
        print('    0  1  2  3  4  5  6  7  8  9 10 11 12 13 14')
        for i in xrange(self.height):
            if i < 10:
                print('{i}  '.format(i=i)),
            else:
                print('{i} '.format(i=i)),
            for j in xrange(self.width):
                print('{p} '.format(p=self.field[i][j])),
                if j == 14: print('')

    def get(self, row, col):
        """Return state of selected point"""
        if (row in xrange(self.height) and col in xrange(self.width)):
            return self.field[row][col]
        else:
            return 0

    def reset(self):
        """Reset the chessboard for next round"""
        for i in xrange(self.height):
            for j in xrange(self.width):
                self.field[i][j] = 0
        self.current['row'] = 7
        self.current['col'] = 7
        self.mode = 1
        self.player_name_1 = 'Player1'
        self.player_name_2 = 'Player2'
        self.current_player = 1
        self.point = 0
        self.concede = 0
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
        self.point = 0
        self.concede = 0
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
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_RED)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        help_string1 = '\n(W)Up        (S)Down       (A)Left       (D)Right\n'
        help_string2 = '\n(C)Set[Double click in single mode]\n(R)Start 2 players mode\n(T)Restart single mode\n(Q)Quit\n'

        def draw_lines():
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if self.field[i][j] == 1: screen.addstr('X', curses.color_pair(1))
                    elif self.field[i][j] == 2 or self.field[i][j] == 3: screen.addstr('O', curses.color_pair(2))
                    elif self.current['row']==i and self.current['col']==j: screen.addstr('?', curses.color_pair(3))
                    elif self.field[i][j] == 0: screen.addstr(' ')
                    if (i*15+j+1)%15 == 0: screen.addstr('\n')
                    else: screen.addstr('---')
                if i in xrange(self.height-1):
                    screen.addstr('|   '*14+'|'+'\n')

        screen.clear()
        try:
            if self.is_win():
                if self.mode == 1:
                    if self.current_player == 1: winner_name = self.player_name_1
                    else: winner_name = self.player_name_2
                elif self.mode == 2:
                    if self.current_player == 3: winner_name = self.player_name_3
                    else: winner_name = self.player_name_1
                screen.addstr('  Winner: %s' % winner_name + ' !!!!\n\n', curses.color_pair(4))
            elif self.concede == 1:
                screen.addstr('  Computer has conceded and left.. You are the winner.!! \n\n', curses.color_pair(4))
            else:
                if self.current_player == 2: now_name = self.player_name_2
                elif self.current_player == 3: now_name = self.player_name_3
                else: now_name = self.player_name_1
                if self.current_player != 3:
                    screen.addstr('It\'s Your Turn !!\n', curses.color_pair(self.current_player))
                    screen.addstr('Now: %s \n' % now_name, curses.color_pair(self.current_player))
                else:
                    screen.addstr('Computer is thinking...\nPress \'C\' to push it!!\n', curses.color_pair(2))
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
        """
        1.  [x]winning5: 100 p
        2.  [x]living4: 90 p
        3.  [ ]double dead4: 90 p
        4.  [x]living4 dead3: 90 p
        5.  [ ]double living3: 80 p
        6.  [x]dead3 living3: 70 p
        7.  [x]dead4: 60 p
        8.  [x]living3: 50 p
        9.  [ ]dead3 living2: 40 p
        10. [ ]double living2: 40 p
        11. [x]dead3: 30 p
        12. [x]living2: 20 p
        13. [x]dead2: 10 p
        14. [-]single: 0 p
        """
        def check_living(field, num):
            """Calculate the living chessmen"""
            moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
            living_count = 0
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 0:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(num+2):
                                if m == 0 or m == num+1: s = 0
                                elif m > 0 and m < num+1: s = 3
                                try:
                                    if field[x][y] != s:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == num+2:
                                living_count += 1
            return living_count

        def check_dead(field, num):
            """Calculate the dead chessmen"""
            moves = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
            dead_count = 0
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 1:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(num+2):
                                if m == 0: s = 1
                                elif m > 0 and m < (num+1): s = 3
                                elif m == (num+1): s = 0
                                try:
                                    if field[x][y] != s:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == (num+2):
                                dead_count += 1
            return dead_count

        def check_cut(field, num):
            """Calculate the cut chessmen"""
            moves = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
            cut_count = 0
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 3:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(num+2):
                                if m == 0: s = 3
                                elif m > 0 and m < (num+1): s = 1
                                elif m == (num+1): s = 0
                                try:
                                    if field[x][y] != s:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == (num+2):
                                cut_count += 1
            return cut_count

        def check_destroy(field, num):
            """Calculate the destroy chessmen"""
            moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
            destroy_count = 0
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 3:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(num+2):
                                if m == 0 or m == num+1: s = 3
                                elif m > 0 and m < num+1: s = 1
                                try:
                                    if field[x][y] != s:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == num+2:
                                destroy_count += 1
            return destroy_count

        def special_1(field):
            """check ? x x o x ? situation """
            moves = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 0:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(6):
                                if m == 0 or m == 5: s = 0
                                elif m == 2: s = 3
                                else: s = 1
                                try:
                                    if field[x][y] != s:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == 6:
                                return True
            return False

        def special_2(field):
            """Check  x x o x x  situation"""
            moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 1:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(5):
                                if m == 2: s = 3
                                else: s = 1
                                try:
                                    if field[x][y] != s:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == 5:
                                return True
            return False

        def special_3(field):
            """check  x x x o x  situation """
            moves = [(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1)]
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 0:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(5):
                                if m == 1: s = 3
                                else: s = 1
                                try:
                                    if field[x][y] != s:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == 5:
                                return True
            return False

        def check_winning(field):
            """Check for winning 5"""
            moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
            for i in xrange(self.height):
                for j in xrange(self.width):
                    if field[i][j] == 3:
                        for move in moves:
                            x, y = i, j
                            chessman_count = 0
                            for m in xrange(5):
                                try:
                                    if field[x][y] != 3:
                                        break
                                except IndexError:
                                    break
                                x += move[0]
                                y += move[1]
                                chessman_count += 1
                            if chessman_count == 5:
                                return True
            return False

        move = {'row': -1, 'col': -1}
        point = 0
        for i in xrange(self.height):
            for j in xrange(self.width):
                if self.field[i][j] == 0:
                    self.field[i][j] = 3
                    ipoint = 0
                    l4_count = check_living(self.field, 4)
                    l3_count = check_living(self.field, 3)
                    l2_count = check_living(self.field, 2)
                    l1_count = check_living(self.field, 1)
                    d4_count = check_dead(self.field, 4)
                    d3_count = check_dead(self.field, 3)
                    d2_count = check_dead(self.field, 2)
                    d1_count = check_dead(self.field, 1)
                    de4_count = check_destroy(self.field, 4)
                    de3_count = check_destroy(self.field, 3)
                    de2_count = check_destroy(self.field, 2)
                    de1_count = check_destroy(self.field, 1)
                    c4_count = check_cut(self.field, 4)
                    c3_count = check_cut(self.field, 3)
                    c2_count = check_cut(self.field, 2)
                    c1_count = check_cut(self.field, 1)

                    # Winning
                    if check_winning(self.field):
                        ipoint += 999999

                    # Special Checks
                    if special_1(self.field): ipoint += 90
                    if special_2(self.field): ipoint += 500
                    if special_3(self.field): ipoint += 500

                    # Defence Points
                    ipoint += de4_count*500
                    ipoint += de3_count*100
                    ipoint += de2_count*35
                    ipoint += de1_count*8

                    ipoint += c4_count*100
                    ipoint += c3_count*90
                    ipoint += c2_count*30
                    ipoint += c1_count*1

                    # Offence Points
                    ipoint += l4_count*110
                    ipoint += l3_count*50
                    ipoint += l2_count*20
                    ipoint += l1_count*0.5

                    ipoint += d4_count*45
                    ipoint += d3_count*20
                    ipoint += d2_count*10
                    ipoint += d1_count*0.1

                    if ipoint > point:
                        move['row'] = i
                        move['col'] = j
                        point = ipoint
                    self.field[i][j] = 0
        #print point, move['row'], move['col']
        if point > 0:
            self.field[move['row']][move['col']] = 3
            return True
        else:
            return False
