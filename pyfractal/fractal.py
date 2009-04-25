#!/usr/bin/python
# coding: utf-8

import math
import re
from utils import Position
from gtk_drawer import PngDrawer

class FractalStat(object):
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
    def update(self, stat):
        self.position = stat.position
        self.angle = stat.angle
    def copy(self):
        p = Position(self.position.x, self.position.y)
        return FractalStat(p, self.angle)

class Intepreter(object):
    def __init__(self, drawer, angle):
        self.drawer = drawer
        self.stat_stack = []
        self.unit_angle = angle
        self.action_map = {
            'F':self.draw_forward,
            '+':self.turn_left,
            '-':self.turn_right,
            '[':self.store_stat,
            ']':self.recover_stat,
        }

    def intepret(self, code):
        stat = FractalStat(position=Position(0.0,0.0), angle=0.0)
        self.drawer.move_to(stat.position)
        for ch in code:
            try:
                self.action_map[ch](stat)
            except KeyError:
                pass
        self.drawer.draw_end()

    def calc_position(self, stat):
        randian_angle = math.radians(stat.angle)
        stat.position.x += math.cos(randian_angle)
        stat.position.y += math.sin(randian_angle)

    def draw_forward(self, stat):
        self.calc_position(stat)
        self.drawer.line_to(stat.position)

    def move_forward(self, stat):
        self.calc_position(stat)
        self.drawer.move_to(stat.position)

    def turn_left(self, stat):
        stat.angle += self.unit_angle

    def turn_right(self, stat):
        stat.angle -= self.unit_angle

    def store_stat(self, stat):
        self.stat_stack.append(stat.copy())

    def recover_stat(self, stat):
        stat.update(self.stat_stack.pop())
        self.drawer.move_to(stat.position)

def generate_code(rules, initial, times):
    '''
    apply production rules to the initialor
    >>> rules = {
    ...  'F': 'F+F-F-F+F'
    ... }
    >>> generate_code(rules, 'F', 1)
    'F+F-F-F+F'
    >>> generate_code(rules, 'F', 2)
    'F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F'
    '''
    code = initial
    reg_str = '|'.join(rules.keys())
    reg = re.compile(reg_str)
    for _ in xrange(times):
        code = reg.sub(lambda m:rules[m.group()], code)
    return code

def draw_fractal(rules, initial, times, angle=90, intepreter=Intepreter):
    code = generate_code(rules, initial, times)
    #print code
    intepreter(PngDrawer(), angle).intepret(code)

if __name__ == '__main__':
    if 0:
        import doctest
        doctest.testmod()
    else:
        '''
        draw_fractal({
            'F': 'F+F-F-F+F'
            }, 'F', 7, 90)
        '''
        draw_fractal({
            'X': 'F-[[X]+X]+F[+FX]-X',
            'F': 'FF',
            }, 'X', 7, 25)
