#!/usr/bin/env python
# coding: utf-8
'''
思路
=====

先把目标塔楼建上去，然后深度优先遍历树，看能否联通。
'''

def get_input(infile):
    it = iter(infile)
    line = it.next()
    M, N = map(int, line.split())
    graph = [[0 for j in range(N)] for i in range(M)]
    for i in range(M):
        flags = it.next().split()
        for j in range(N):
            if flags[j]=='*':
                graph[i][j] = 1
    tower_x, tower_y = map(int, it.next().split())
    graph[tower_x][tower_y] = 1
    return graph, (M-1, N-1), (tower_x, tower_y)

def get_next_poses(pos):
    x, y = pos
    # 优先右下角方向
    return [(x, y+1), (x+1,y), (x, y-1), (x-1, y)]

def traverse(env):
    graph, size, target = env
    visit_queue = [(0,0)]
    visited = {}
    while visit_queue:
        #print 'visit_queue', visit_queue
        pos = visit_queue.pop(0)
        visited[pos] = 1
        #print 'visited', pos
        if pos==target:
            return True

        def test_pos(pos):
            x, y = pos
            M,N = size
            return pos not in visited and M>x>=0 and N>y>=0 and graph[x][y]==0

        next_poses = filter(test_pos, get_next_poses(pos))
        visit_queue = next_poses+visit_queue
    return False

def main(infile, outfile):
    graph, target_position, tower_position = get_input(infile)
    #print graph
    # env: (graph, graph_size, target)
    env = (graph, (len(graph), len(graph[0])), target_position) 
    result = traverse(env)
    outfile.write('%d %d %s'%(tower_position[0], tower_position[1], result and 'Yes' or 'No'))

def test():
    import sys
    from StringIO import StringIO
    test_cases = [
        ['''3 4 
- - - - 
- * - - 
- * - - 
0 1''', '0 1 No'],
        ['''3 4 
- - - - 
- * - * 
- * - - 
1 0''', '1 0 Yes'],
        ['''3 4 
- - - - 
- * - * 
- * - - 
1 2''', '1 2 No'],
        ['''1 4 
- - - - 
0 1''', '0 1 No'],
        ['''5 4 
- - - - 
* * * - 
- - - - 
- - * * 
- - - - 
3 1''', '3 1 Yes'],
        ['''5 4 
- - - - 
* * * - 
- - - - 
- * * * 
- - - - 
3 0''', '3 0 No']
    ]
    for input, output in test_cases:
        infile = StringIO(input)
        outfile = StringIO()
        main(infile, outfile)
        assert outfile.getvalue()==output, outfile.getvalue()
        print 'success'

if __name__ == '__main__':
    if 0:
        test()
    else:
        import sys
        main(sys.stdin, sys.stdout)
