#!/usr/bin/python
from collections import defaultdict
from heapq import *
from math import sqrt
from copy import deepcopy
import pdb

def build_map(desc):
    desc.split('\n')

def vecadd((x1,y1), (x2,y2)):
    return (x1+x2, y1+y2)

class Node(object):
    def __init__(self, pos, parent, dsrc, dtarget):
        self.pos,self.parent,self.dsrc,self.dtarget = \
                pos,parent,dsrc,dtarget
        self.hvalue = dsrc+dtarget

    def __cmp__(self, node):
        return self.hvalue - node.hvalue

class Map(object):
    def __init__(self, desc):
        self.text_map = []
        lines = desc.split('\n')
        self.map = defaultdict(lambda:1)
        for y,line in enumerate(lines):
            self.text_map.append(list(line))
            for x,c in enumerate(line):
                self.map[(x,y)] = (0 if c!='1' else 1)
                if c=='2':
                    self.start = (x, y)
                elif c=='3':
                    self.target = (x, y)
        self.debug_map = deepcopy(self.text_map)

    def print_lines(self, map_):
        print '\n'.join(''.join(line) for line in map_)

    def calc_htarget(self, (x,y)):
        tx,ty = self.target
        '''
        return abs(x-tx) + abs(y-ty)
        '''
        dx,dy = abs(x-tx), abs(y-ty)
        dmax,dmin = dx>dy and (dx,dy) or (dy,dx)
        return dmax*10 + dmin*4

    def children(self, node):
        '''
        directions = [
            (0,-1),
            (1,0),
            (0,1),
            (-1,0)
        ]
        '''
        directions = [
            (-1,-1),
            (0,-1),
            (1,-1),
            (1,0),
            (1,1),
            (0,1),
            (-1,1),
            (-1,0)
        ]
        for d in directions:
            childpos = vecadd(node.pos, d)
            if self.map[childpos]==0:
                htarget = self.calc_htarget(childpos)
                yield Node(childpos,node,node.dsrc+1,htarget)

    def findpath(self):
        path = []
        target = self.target
        tovisit = [Node(self.start, None, 0, 0)]
        visited = set() # record visited positions

        while tovisit:
            node = heappop(tovisit)
            pos = node.pos

            if pos==target:
                return node

            if pos in visited:
                continue

            visited.add(pos)

            #debug
            '''
            x, y = pos
            self.debug_map[y][x] = '*'
            self.print_lines(self.debug_map)
            pdb.set_trace()
            '''

            for child in self.children(node):
                if child.pos not in visited:
                    heappush(tovisit, child)

if __name__ == '__main__':
    graph_desc = '''
0000000000000000000100000
0000000000000000000103010
0000000000000000000111110
0000000000000000000100000
0000000001111110000100000
0000000001000110111100000
0000000001012100010000000
0000000001011100010000000
0000000001000001010000000
0000000001111111010000000
0000000000000000010000000
0000000000000000000000000
    '''
    map = Map(graph_desc)
    node = map.findpath()
    while node:
        x,y = node.pos
        map.text_map[y][x] = '*'
        node = node.parent
    map.print_lines(map.text_map)


