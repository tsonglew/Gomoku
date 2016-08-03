# -*- coding: utf-8 -*-


class Player(object):
    def __init__(self, name='player'):
        self.name = name
        self.steps = 0

    def add_step(self):
        self.steps += 1
        return '%d' % self.steps
