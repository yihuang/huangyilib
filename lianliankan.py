# coding: utf-8

def trace(func):
    def new_func(*args):
        result = func(*args)
        print func.__name__, args, result
        return result
    return new_func

def unsigned_range(a, b):
    if a<b:
        return range(a+1, b)
    else:
        return range(b+1, a)

def unsigned_range1(a, b):
    if a<b:
        return range(a, b+1)
    else:
        return range(b, a+1)

def check(map, p1, p2):
    '''
    make sure y1<=y2
    '''
    height = len(map)
    width = len(map[0])
    def check_xline(x, y1, y2): # 横线
        if abs(y1-y2)<2:
            return True
        for i in unsigned_range(y1, y2):
            if map[x][i]!=0:
                return False
        return True
    def check_yline(y, x1, x2): # 竖线
        if abs(x1-x2)<2:
            return True
        for i in unsigned_range(x1, x2):
            if map[i][y]!=0:
                return False
        return True

    '''
    assert(check_xline(0, 0, 4)==False)
    assert(check_xline(5, 1, 4)==True)
    assert(check_xline(1, 3, 4)==True)
    assert(check_yline(3, 1, 3)==False)
    assert(check_yline(3, 1, 2)==True)
    assert(check_yline(2, 1, 5)==True)
    assert(check_yline(4, 0, 2)==False)
    '''

    x1,y1=p1
    x2,y2=p2
    if x1==x2 and check_xline(x1, y1, y2):
        return [p1, p2]
    if y1==y2 and check_yline(y1, x1, x2):
        return [p1, p2]

    for x in range(0,height):
        y = y1
        if check_yline(y, x, x1) and check_yline(y2, x, x2) and check_xline(x, y1, y2):
            if x==x1:
                return [p1, (x,y2), p2]
            elif x==x2:
                return [p1, (x,y1), p2]
            else:
                return [p1, (x,y1), (x,y2), p2]
    for y in range(0, width):
        x = x1
        if check_xline(x, y, y1) and check_xline(x2, y, y2) and check_yline(y, x1, x2):
            if y==y1:
                return [p1, (x2,y), p2]
            elif y==y2:
                return [p1, (x1,y), p2]
            else:
                return [p1, (x1,y), (x2,y), p2]
    return False

test_case = [
    [0,0,0,2,0,0,0],
    [0,0,0,2,1,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,2,2,0,0],
    [0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0]
]

assert( check(test_case, (5,1),(1,4)) == [(5, 1), (5, 5), (1, 5), (1, 4)] )

test_case = [
    [0,0,0,2,0,0,0],
    [0,0,0,2,1,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,2,0,0,0],
    [0,0,0,2,0,0,0],
    [0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0]
]

assert( check(test_case, (5,1),(1,4)) == [(5, 1), (5, 4), (1, 4)] )
