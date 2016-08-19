# coding: utf-8
from . import app
from flask import render_template, request
import json



@app.route('/field/')
def field():
    field = [[0 for m in xrange(15)] for n in xrange(15)]
    string = request.args.get('field')
    for i in string:
        for row in xrange(15):
            for col in xrange(15):
                field[row][col] = int(string[row*15+col])

    def check_living(field, num):
        """Calculate the living chessmen"""
        moves = [(1, -1), (1, 0), (1, 1), (0, 1)]
        living_count = 0
        for i in xrange(15):
            for j in xrange(15):
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
        for i in xrange(15):
            for j in xrange(15):
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
        for i in xrange(15):
            for j in xrange(15):
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
        for i in xrange(15):
            for j in xrange(15):
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
        for i in xrange(15):
            for j in xrange(15):
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
        for i in xrange(15):
            for j in xrange(15):
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
        for i in xrange(15):
            for j in xrange(15):
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
        for i in xrange(15):
            for j in xrange(15):
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
    for i in xrange(15):
        for j in xrange(15):
            if field[i][j] == 0:
                field[i][j] = 3
                ipoint = 0
                # Winning
                if check_winning(field):
                    return True

                l4_count = check_living(field, 4)
                l3_count = check_living(field, 3)
                l2_count = check_living(field, 2)
                l1_count = check_living(field, 1)
                d4_count = check_dead(field, 4)
                d3_count = check_dead(field, 3)
                d2_count = check_dead(field, 2)
                d1_count = check_dead(field, 1)
                de4_count = check_destroy(field, 4)
                de3_count = check_destroy(field, 3)
                de2_count = check_destroy(field, 2)
                de1_count = check_destroy(field, 1)
                c4_count = check_cut(field, 4)
                c3_count = check_cut(field, 3)
                c2_count = check_cut(field, 2)
                c1_count = check_cut(field, 1)



                # Special Checks
                if special_1(field): ipoint += 90
                if special_2(field): ipoint += 500
                if special_3(field): ipoint += 500

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
                ipoint += l4_count*140
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
                field[i][j] = 0
    return json.dumps(move)
