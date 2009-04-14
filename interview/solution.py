#!/usr/bin/env python
# coding: utf-8
'''
===========================
Tower Defense (Stage I) 
===========================

思路：先把待建塔楼建上去，然后深度优先遍历地图，看能否联通。

开发环境：Ubuntu8.10 Python2.5

设计要点
=========

使用二维列表表示地图。

使用元组 tuple 表示节点坐标。

使用深度优先算法遍历地图。

坐标系统
=========

左上角为原点，垂直方向为 X 轴，水平方向为 Y 轴（该坐标系统由问题描述中所定义）。

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

::

    $ ./solution.py -h
    Usage: solution.py [-f] [-o] [-t]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  input file, default stdin
      -o OUTPUT, --output=OUTPUT
                            output file, default stdout
      -t, --test            run doc test
      -l LOGFILENAME, --log=LOGFILENAME
                            specify log file name, default ./solution.log
    
程序可以使用命令行参数指定输入输出文件，默认使用标准输入输出。

可以直接执行程序交互式输入样本数据（注意要输入 Ctrl+D(linux) 或者 Ctrl+Z(windows) 结束输入）， ::

    $ ./solution.py
    3 4
    - - - -
    - * - -
    - * - -
    0 1
    0 1 No

也可先将问题描述写入文件，指定输入文件名来执行。 ::

    $ ./solution.py -f input_file
    0 1 No

执行测试
=========

* 传递 -t 或 --test 参数执行文档测试。
* ./test_solution.py 执行单元测试。

ChangeLog
==========

version 1.1 (2009年 04月 13日 星期一 22:52:19 CST)
---------------------------------------------------

1. 加入命令行参数
2. 加入文档测试和单元测试
3. log一些调试信息，方便定位问题。
4. 增加执行模式，可通过参数指定输入输出文件
5. 增加对输入的错误检查

'''
import logging

class TowerDefenseException(BaseException):
    pass

def get_input(infile):
    '''
    解析输入文件，构建地图，并将待建塔楼建上去

    参数：输入文件对象
    输出：地图，需要抵达的目标节点坐标，待建塔楼坐标

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
    # 地图规格
    M, N = map(int, line.split())
    # 构建地图
    graph = [[0 for j in range(N)] for i in range(M)]
    for i in range(M):
        flags = it.next().split()
        if len(flags)<N:
            raise TowerDefenseException('invalid input format')
        for j in range(N):
            if flags[j]=='*':
                graph[i][j] = 1
    # 建立目标塔楼
    tower_x, tower_y = map(int, it.next().split())
    if tower_x>=M or tower_y>=N:
        raise TowerDefenseException('invalid input format')
    graph[tower_x][tower_y] = 1
    return graph, (M-1, N-1), (tower_x, tower_y)

def get_next_positions(position):
    '''
    获取相邻节点坐标
    '''
    x, y = position
    # 优先右下角方向
    return [(x-1, y), (x, y-1), (x+1,y), (x, y+1)]

def traverse(graph, size, start, target):
    '''
    使用循环对地图进行深度优先遍历

    输入：地图，地图大小，需抵达的目标节点坐标
    返回：bool值，表示从起始节点到目标节点能否联通

    示例：
    >>> traverse([[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]], (3, 4), (0, 0), (2, 3))
    True
    >>> traverse([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]], (3, 4), (0, 0), (2, 3))
    False
    '''
    # 待访问节点栈
    visit_queue = [start]
    # 记录已访问节点坐标
    visited = {}

    def test_position(position):
        '''
        测试该节点是否要加入待访问节点队列
        '''
        x, y = position
        M,N = size
        return position not in visited and M>x>=0 and N>y>=0 and graph[x][y]==0

    while visit_queue:
        logging.info('current visit_queue:' + str(visit_queue))
        position = visit_queue.pop()
        visited[position] = 1
        logging.info('visit:' + str(position))
        if position==target:
            return True
        # 产生相邻节点并加入待访问节点队列中。
        next_positions = filter(test_position, get_next_positions(position))
        logging.info('enqueue:' + str(next_positions))
        visit_queue += next_positions
    return False

def main(infile, outfile):
    '''
    解决该问题的主函数
    '''
    # 读取问题输入
    try:
        graph, target_position, tower_position = get_input(infile)
    except StopIteration, ex:
        raise TowerDefenseException('invalid input format')
    logging.info('parsed input graph:'+str(graph))
    # 深度优先遍历地图
    connected = traverse(graph, (len(graph), len(graph[0])), (0, 0), target_position)
    # 输出结果
    print >>outfile, tower_position[0], tower_position[1], connected and 'Yes' or 'No'

if __name__ == '__main__':
    import sys, optparse
    # 解析命令行输入
    parser = optparse.OptionParser(usage='%prog [-f] [-o] [-t]', version='%prog 1.1')
    parser.add_option("-f", "--file",
            help="input file, default stdin", default=sys.stdin)
    parser.add_option("-o", "--output",
            help="output file, default stdout", default=sys.stdout)
    parser.add_option("-t", "--test", action="store_true", dest="test",
            help="run doc test")
    parser.add_option("-l", "--log", dest="logfilename",
            help="specify log file name, default ./solution.log", default="./solution.log")
    (options, args) = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(funcName)s(%(filename)s:%(lineno)d) %(message)s',
            filename=options.logfilename,
            filemode='a')

    if options.test:
        # 执行文档测试
        import doctest
        doctest.testmod(verbose=True)
    else: 
        infile = options.file
        outfile = options.output
        try:
            if isinstance(options.file, str):
                infile = open(infile)
            if isinstance(options.output, str):
                outfile = open(outfile, 'w')
        except IOError, ex: # 打开文件失败
            print ex
        try:
            main(infile, outfile)
        except TowerDefenseException, ex:
            print ex
        infile.close()
        outfile.close()
