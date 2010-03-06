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
        self.pos,self.parent,self.dtarget,self.dsrc = \
                pos,parent,dtarget,dsrc

    def set_dsrc(self, value):
        self._dsrc = value
        self.hvalue = value+self.dtarget

    def get_dsrc(self):
        return self._dsrc

    dsrc = property(get_dsrc, set_dsrc)

    def __cmp__(self, node):
        return self.hvalue - node.hvalue

def findnode(l, pos):
    for node in l:
        if node.pos==pos:
            return node
    return None

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
        self.dtarget = {}
        self.calc_all_dtarget()
        self.debug_map = deepcopy(self.text_map)

    def print_lines(self, map_):
        print '\n'.join(''.join(line) for line in map_)

    def calc_dtarget(self, (x,y)):
        tx,ty = self.target
        '''
        return abs(x-tx) + abs(y-ty)
        '''
        dx,dy = abs(x-tx), abs(y-ty)
        dmax,dmin = dx>dy and (dx,dy) or (dy,dx)
        return dmax*10 + dmin*4
    def calc_all_dtarget(self):
        for pos, value in self.map.items():
            if value==0:
                self.dtarget[pos] = self.calc_dtarget(pos)

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
        (x,y) = node.pos
        for dx,dy in directions:
            childpos = (x+dx, y+dy)
            if self.map[childpos]==0:
                yield childpos,node.dsrc+1

    def findpath(self):
        startnode = Node(self.start, None, 0, 0)
        target = self.target
        openset = [startnode]   # node list
        closeset = set()        # position set
        while openset:
            node = heappop(openset)
            if node.pos == target:
                return node
            closeset.add(node.pos)

            #debug
            '''
            x, y = pos
            self.debug_map[y][x] = '*'
            self.print_lines(self.debug_map)
            pdb.set_trace()
            '''

            for childpos, dsrc in self.children(node):
                if childpos in closeset:
                    continue
                opennode = findnode(openset, childpos)
                if opennode and dsrc>=opennode.dsrc:
                    continue
                elif not opennode:
                    child = Node(childpos, node, dsrc, self.dtarget[childpos])
                    heappush(openset, child)
                else:
                    opennode.dsrc = dsrc
                    opennode.parent = node
                    heapify(openset)

    def findpath1(self):
        startnode = Node(self.start, None, 0, 0)
        target = self.target
        openset = [startnode]   # node list
        closeset = set()        # position set
        while openset:
            node = heappop(openset)
            pos = node.pos
            if pos in closeset:
                continue
            if pos == target:
                return node
            closeset.add(pos)

            #debug
            '''
            x, y = pos
            self.debug_map[y][x] = '*'
            self.print_lines(self.debug_map)
            pdb.set_trace()
            '''

            for childpos, dsrc in self.children(node):
                if childpos in closeset:
                    continue
                child = Node(childpos, node, dsrc, self.dtarget[childpos])
                heappush(openset, child)

if __name__ == '__main__':
    graph_desc = '''
0000000000000000000100000
0111111111111111110103010
0100000000000000000111110
0101111111111111111100010
0101000000000000000100010
0101000001000110111100010
0101000001012100010000010
0101000001011100010000010
0101000001000001010000010
0100000001111111010000010
0111111111111111111111110
0000000000000000000000000
    '''
    map = Map(graph_desc)

    for i in range(1000):
        node = map.findpath()

    while node:
        x,y = node.pos
        map.text_map[y][x] = '*'
        node = node.parent
    map.print_lines(map.text_map)


