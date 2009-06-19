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

def get_range(max, a, b):
    if a>b:
        b,a = a,b
    return range(a,b+1) + range(a-1,-1,-1) + range(b+1, max)

def check(map, p1, p2):
    '''
    make sure y1<=y2
    '''
    height = len(map)
    width = len(map[0])
    def check_xline(x, y1, y2): # 横线 检查两点之间可以连接
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

    x1,y1=p1
    x2,y2=p2

    # 检查直接相连
    if x1==x2 and check_xline(x1, y1, y2):
        return [p1, p2]
    if y1==y2 and check_yline(y1, x1, x2):
        return [p1, p2]

    # 检查通过一个或两个中间点相连
    for x in get_range(height, x1, x2):
        # 两个中间点 不与目标重合 且 不为空，则检查失败
        if not ((x==x1 or map[x][y1]==0) and (x==x2 or map[x][y2]==0)):
            continue
        if check_yline(y1, x, x1) and check_yline(y2, x, x2) and check_xline(x, y1, y2):
            if x==x1:
                return [p1, (x,y2), p2]
            elif x==x2:
                return [p1, (x,y1), p2]
            else:
                return [p1, (x,y1), (x,y2), p2]
    for y in get_range(width, y1, y2):
        if not ((y==y1 or map[x1][y]==0) and (y==y2 or map[x2][y]==0)):
            continue
        if check_xline(x1, y, y1) and check_xline(x2, y, y2) and check_yline(y, x1, x2):
            if y==y1:
                return [p1, (x2,y), p2]
            elif y==y2:
                return [p1, (x1,y), p2]
            else:
                return [p1, (x1,y), (x2,y), p2]
    return False

