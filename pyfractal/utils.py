# coding: utf-8

class Position(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    def __str__(self):
        return 'Position %f %f'%(self.x, self.y)

