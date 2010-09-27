#!/usr/bin/env python
# coding: utf-8
from heapq import heapify, heappop

def index_slice(l, indexes):
    return [l[idx] for idx in indexes]

class Sudoku(object):
    area_indexes = [
        [0,1,2,9,10,11,18,19,20],
        [3,4,5,12,13,14,21,22,23],
        [6,7,8,15,16,17,24,25,26],
        [27,28,29,36,37,38,45,46,47],
        [30,31,32,39,40,41,48,49,50],
        [33,34,35,42,43,44,51,52,53],
        [54,55,56,63,64,65,72,73,74],
        [57,58,59,66,67,68,75,76,77],
        [60,61,62,69,70,71,78,79,80]
    ]
    fullset = set(range(1,10))

    def __init__(self, init):
        '''
        init: [int] 初始盘面
          y
        x   0 1 2 3 4 5 6 7 8
          0-0 1 2 3 4 5 6 7 8
          1-9
          2-18
          3-27
          4-36
          5-45
          6-54
          7-63
          8-72
        '''
        self.board = init
        self.candidates = [[] for i in range(9*9)]

    def __getitem__(self, pos):
        x, y = pos
        idx = self.index( (x, y) )
        return self.board[idx]
    def __setitem__(self, pos, value):
        print 'set', pos, value
        idx = self.index(pos)
        self.board[idx] = value
        self.candidates[idx].clear()
        # influence row col area
        for func in [self.row, self.col, self.area]:
            for idx, num in func(pos, True):
                if num==0:
                    self.candidates[idx].discard(value)

    def index(self, (x, y)):
        return y*9+x

    def pos(self, idx):
        y, x = divmod(idx, 9)
        return x, y
    def row(self, (x, y), index=False):
        start = y*9
        data = self.board[start:start+9]
        if not index:
            return data
        else:
            indexes = range(start, start+9)
            return zip(indexes, data)
    def col(self, (x, y), index=False):
        start = x
        data = self.board[x::9]
        if not index:
            return data
        else:
            indexes = range(x, len(self.board), 9)
            return zip(indexes, data)
    def areaindex(self, (x, y)):
        xi, yi = x/3, y/3
        return yi*3+xi
    def area(self, pos, index=False):
        indexes = self.area_indexes[self.areaindex(pos)]
        data = index_slice(self.board, indexes)
        if not index:
            return data
        else:
            return zip(indexes, data)
    def get_candidates(self, pos):
        exceptions = set(self.row(pos)+self.col(pos)+self.area(pos))
        return self.fullset-exceptions
    def get_min_candidate(self):
        sort_data = [(len(data), idx) for idx, data in enumerate(self.candidates)
                if data]
        if not sort_data:
            return -1, None
        heapify(sort_data)
        _, idx = heappop(sort_data)
        return idx, self.candidates[idx]
    def generate_candidates(self):
        for idx, num in enumerate(self.board):
            if num==0:
                result = self.get_candidates(self.pos(idx))
                self.candidates[idx] = result
            else:
                self.candidates[idx] = set()
    def solve(self):
        '''
        算法：
        遍历所有空位，记录候选，取候选数最少的位置进行猜测。
        '''
        self.generate_candidates()
        while True:
            idx, data = self.get_min_candidate()
            if idx<0:
                break
            if len(data)>1:
                raise Exception(u'暂不能解决不确定性数独')
            # set
            self[self.pos(idx)] = list(data)[0]
    def validate(self):
        for x in range(9):
            data = filter(lambda o:o>0, self.col((x, 0)))
            assert len(set(data))==len(data), 'col%d'%x
        for y in range(9):
            data = filter(lambda o:o>0, self.row((0, y)))
            assert len(set(data))==len(data), 'row%d'%y
        for area in range(9):
            indexes = self.area_indexes[area]
            data = filter(lambda o:o>0, index_slice(self.board, indexes))
            assert len(set(data))==len(data), 'area%d'%area
        print 'valid'
    def __str__(self):
        buf = []
        for i in range(9):
            start = i*9
            buf.append(' '.join(map(str, self.board[start:start+9])))
        return '\n'.join(buf)

if __name__ == '__main__':
    problem = '''\
700300020\
840260005\
052019087\
000900032\
401000706\
920006000\
290680170\
100024068\
070003004'''
    board = map(int, problem)
    sudoku = Sudoku(board)
    sudoku.validate()
    print sudoku
    sudoku.solve()
    sudoku.validate()
    print sudoku
