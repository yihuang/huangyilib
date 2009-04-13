#!/usr/bin/env python
# coding: utf-8
'''
设计
=====

先把待建塔楼建上去，然后深度优先遍历地图，看能否联通。

坐标系统
=========

左上角为原点，垂直方向为 X 轴，水平方向为 Y 轴（该坐标系统由问题描述中所定义）。

单词缩写
=========

* pos => position
* infile => input file
* outfile => output file

输入文件格式
=============

第一行是空格分隔的两个数字，分别为高度M和宽度N，
随后的M行是二维地图数据，字符'-'表示空地，字符'*'表示塔楼，字符间以空格分隔，
最后一行是空格分隔的两个数字，为目标塔楼的坐标。

输入示例： ::

    3 3
    - * -
    - * *
    - - -
    2 0

使用方法
=========

程序使用标准输入读取输入数据，标准输出输出信息。

可以直接执行程序交互式输入样本输入（注意要输入 Ctrl+Z 结束输入）， ::

    $ python solution.py
    3 4
    - - - -
    - * - -
    - * - -
    0 1
    ^Z
    0 1 No

也可先将问题描述写入文件，通过输入重定向执行程序。 ::

    $ python solution.py < input_file
    0 1 No

执行测试
=========

* 传递 doctest 作为参数执行文档测试。
* 执行 test_solution.py 执行单元测试。
'''

def get_input(infile):
    '''
    解析输入文件，构建地图，并将待建塔楼先建上去

    参数：输入文件对象
    输出：地图，需要抵达的目标位置，待建塔楼坐标

    示例：

    >>> from StringIO import StringIO
    >>> test_file = StringIO(\'\'\'3 4
    ... - - - -
    ... - * - -
    ... - * - -
    ... 0 1\'\'\')
    >>> graph, target_position, tower_position = get_input(test_file)
    >>> target_position
    (2, 3)
    >>> tower_position
    (0, 1)
    >>> graph
    [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
    '''
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
    # 建立目标塔楼
    graph[tower_x][tower_y] = 1
    return graph, (M-1, N-1), (tower_x, tower_y)

def get_next_poses(pos):
    '''
    获取相邻节点位置
    '''
    x, y = pos
    # 优先右下角方向
    return [(x-1, y), (x, y-1), (x+1,y), (x, y+1)]

def traverse(graph, size, start, target):
    '''
    使用循环对地图进行深度优先遍历

    输入：地图，地图大小，需抵达的目标位置
    返回：bool值，表示从起始位置到目标位置能否联通

    示例：
    >>> traverse([[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]], (3, 4), (0, 0), (2, 3))
    True
    >>> traverse([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]], (3, 4), (0, 0), (2, 3))
    False
    '''
    # 待访问节点栈
    visit_queue = [start]
    # 记录已访问节点位置
    visited = {}

    def test_pos(pos):
        '''
        测试该位置是否要加入待访问节点队列
        '''
        x, y = pos
        M,N = size
        return pos not in visited and M>x>=0 and N>y>=0 and graph[x][y]==0

    while visit_queue:
        #print 'visit_queue', visit_queue
        pos = visit_queue.pop()
        visited[pos] = 1
        #print 'visited', pos
        if pos==target:
            return True
        next_poses = filter(test_pos, get_next_poses(pos))
        visit_queue += next_poses
    return False

def main(infile, outfile):
    '''
    解决该问题的主函数
    '''
    # 读取问题输入
    graph, target_position, tower_position = get_input(infile)
    #print graph
    # 深度优先遍历地图
    result = traverse(graph, (len(graph), len(graph[0])), (0, 0), target_position)
    # 输出结果
    outfile.write('%d %d %s'%(tower_position[0], tower_position[1], result and 'Yes' or 'No'))

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='doctest':
        import doctest
        doctest.testmod()
    else: 
        main(sys.stdin, sys.stdout)
