#!/usr/bin/env python
# coding: utf-8
'''
===========================
Tower Defense (Stage I) 
===========================

˼·���ȰѴ�����¥����ȥ��Ȼ��������ȱ�����ͼ�����ܷ���ͨ��

����������Ubuntu8.10 Python2.5

���Ҫ��
=========

ʹ�ö�ά�б��ʾ��ͼ��

ʹ��Ԫ�� tuple ��ʾ�ڵ����ꡣ

ʹ����������㷨������ͼ��

����ϵͳ
=========

���Ͻ�Ϊԭ�㣬��ֱ����Ϊ X �ᣬˮƽ����Ϊ Y �ᣨ������ϵͳ�����������������壩��

�����ļ���ʽ
=============

��һ���ǿո�ָ����������֣��ֱ�Ϊ�߶�M�Ϳ��N��
����M���Ƕ�ά��ͼ���ݣ��ַ�'-'��ʾ�յأ��ַ�'*'��ʾ��¥���ַ����Կո�ָ���
���һ���ǿո�ָ����������֣�ΪĿ����¥�����ꡣ

����ʾ���� ::

    3 3
    - * -
    - * *
    - - -
    2 0

ʹ�÷���
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
    
�������ʹ�������в���ָ����������ļ���Ĭ��ʹ�ñ�׼���������

����ֱ��ִ�г��򽻻�ʽ�����������ݣ�ע��Ҫ���� Ctrl+D(linux) ���� Ctrl+Z(windows) �������룩�� ::

    $ ./solution.py
    3 4
    - - - -
    - * - -
    - * - -
    0 1
    0 1 No

Ҳ���Ƚ���������д���ļ���ָ�������ļ�����ִ�С� ::

    $ ./solution.py -f input_file
    0 1 No

ִ�в���
=========

* ���� -t �� --test ����ִ���ĵ����ԡ�
* ./test_solution.py ִ�е�Ԫ���ԡ�

ChangeLog
==========

version 1.1 (2009�� 04�� 13�� ����һ 22:52:19 CST)
---------------------------------------------------

1. ���������в���
2. �����ĵ����Ժ͵�Ԫ����
3. logһЩ������Ϣ�����㶨λ���⡣
4. ����ִ��ģʽ����ͨ������ָ����������ļ�
5. ���Ӷ�����Ĵ�����

TODO: ʹ�� c ���±�����ͼ���� _traverse.c ���ṩ�����㷨��ִ�����ܡ�

'''
import logging

RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
UP = (-1, 0)

class TowerDefenseException(BaseException):
    pass

def get_input(infile):
    '''
    ���������ļ���������ͼ������������¥����ȥ

    �����������ļ�����
    �������ͼ����Ҫ�ִ��Ŀ��ڵ����꣬������¥����

    ʾ����

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
    # ��ͼ���
    M, N = map(int, line.split())
    # ������ͼ
    graph = [[0 for j in range(N)] for i in range(M)]
    for i in range(M):
        flags = it.next().split()
        if len(flags)<N:
            raise TowerDefenseException('invalid input format')
        for j in range(N):
            if flags[j]=='*':
                graph[i][j] = 1
    # ����Ŀ����¥
    tower_x, tower_y = map(int, it.next().split())
    if tower_x>=M or tower_y>=N:
        raise TowerDefenseException('invalid input format')
    graph[tower_x][tower_y] = 1
    return graph, (M-1, N-1), (tower_x, tower_y)

def get_next_positions(position, direction):
    '''
    ��ȡ���ڽڵ�����
    position: ��ǰλ��
    direction: ��ǰ����
    >>> get_next_positions((0, 0), UP)
    '''
    x, y = position

    direction_idx_map = {(0, 1):0, 
        (1, 0):1,
        (0, -1):2,
        (-1, 0):3}

    # �ĳ����ȵ�ǰ���򣬲�����ʱ�뷽����б���
    base = [(x, y+1), (x-1, y), (x, y-1), (x+1,y)] # ��������
    result_map = [
        [base[3],base[2],base[1],base[0]], # ��
        [base[2],base[1],base[0],base[3]], # ��
        [base[1],base[0],base[3],base[2]], # ��
        [base[0],base[3],base[2],base[1]]  # ��
    ]
    '''
    result_map = [
        [base[0],base[1],base[2],base[3]], # ��
        [base[1],base[2],base[3],base[0]], # ��
        [base[2],base[3],base[0],base[1]], # ��
        [base[3],base[0],base[1],base[2]]  # ��
    ]
    '''
    return result_map[ (direction_idx_map[direction]) ]

def calc_direction(p1, p2):
    '''
    �������������λ�ã���p1��p2�ķ���
    '''
    direction = [p2[0]-p1[0], p2[1]-p1[1]]
    if direction[0]!=0 and direction[1]!=0:
        direction[0] = 0
    if direction[0]>1:direction[0]=1
    if direction[0]<-1:direction[0]=-1
    if direction[1]>1:direction[1]=1
    if direction[1]<-1:direction[1]=-1
    return tuple(direction)

def traverse(graph, size, start, target):
    '''
    ʹ��ѭ���Ե�ͼ����������ȱ���

    ���룺��ͼ����ͼ��С����ִ��Ŀ��ڵ�����
    ���أ�boolֵ����ʾ����ʼ�ڵ㵽Ŀ��ڵ��ܷ���ͨ

    ʾ����
    >>> traverse([[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]], (3, 4), (0, 0), (2, 3))
    True
    >>> traverse([[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]], (3, 4), (0, 0), (2, 3))
    False
    '''
    # �����ʽڵ�ջ
    visit_queue = [start]
    position = None
    # ��¼�ѷ��ʽڵ�����
    visited = {}

    def test_position(position):
        '''
        ���Ըýڵ��Ƿ�Ҫ��������ʽڵ�ջ
        '''
        x, y = position
        M,N = size
        return position not in visited and M>x>=0 and N>y>=0 and graph[x][y]==0

    while visit_queue:
        #logging.info('current visit_queue:' + str(visit_queue))
        last_position = position
        position = visit_queue.pop()
        if position in visited:
            #logging.info('already visite:' + str(position))
            continue
        if last_position:
            current_direction = calc_direction(last_position, position)
        else:
            current_direction = RIGHT # ��ʼ��������
        visited[position] = 1
        #logging.info('visit:' + str(position))
        #print 'visit', position
        if position==target:
            return True
        # �������ڽڵ㲢��������ʽڵ�ջ�С�
        next_positions = get_next_positions(position, current_direction)
        next_positions = filter(test_position, next_positions)
        #logging.info('enqueue:' + str(next_positions))
        visit_queue += next_positions
    return False

def main(infile, outfile):
    '''
    ����������������
    '''
    # ��ȡ��������
    try:
        graph, target_position, tower_position = get_input(infile)
    except StopIteration, ex:
        raise TowerDefenseException('invalid input format')
    logging.info('parsed input graph:'+str(graph))
    # ������ȱ�����ͼ
    connected = traverse(graph, (len(graph), len(graph[0])), (0, 0), target_position)
    # ������
    print >>outfile, tower_position[0], tower_position[1], connected and 'Yes' or 'No'

if __name__ == '__main__':
    import sys, optparse
    # ��������������
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

    '''
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(funcName)s(%(filename)s:%(lineno)d) %(message)s',
            filename=options.logfilename,
            filemode='a')
    '''

    if options.test:
        # ִ���ĵ�����
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
        except IOError, ex: # ���ļ�ʧ��
            print ex
        try:
            main(infile, outfile)
        except TowerDefenseException, ex:
            print ex
        infile.close()
        outfile.close()
