#coding:utf-8
from collections import deque

'''
http://www.stackless.com/
'''

debuglevel = 0

readys = deque() # 就绪队列

class command(object):
    def __init__(self, func, *args, **kw):
        self.func = func
        self.args = args
        self.kw = kw

    def __call__(self, task):
        return self.func(task, *self.args, **self.kw)

class channel(object):
    ''' http://www.stackless.com/wiki/Channels '''
    def __init__(self):
        self.senders = deque() # 发送队列 元素：(tasklet, obj)
        self.receivers = deque() # 接收队列 元素：tasklet

    def send(self, sender, obj):
        '''向channel中发送数据，如果没用接受者，则让该tasklet等待'''
        if debuglevel:
            print 'tasklet:',sender,'send data:',obj,';receivers:',len(self.receivers)
        if self.receivers:
            receiver = self.receivers.popleft()
            ready(sender, None)
            run(receiver, obj)
        else:
            self.senders.append( (sender, obj) )

    def receive(self, receiver):
        ''' 从channel中接收数据，如果没用发送者，则让该tasklet等待'''
        if debuglevel:
            print 'tasklet:',receiver,'receive data ;senders:',len(self.senders)
        if self.senders:
            sender, obj = self.senders.popleft()
            ready(receiver,obj)
            run(sender, None)
        else:
            self.receivers.append(receiver)

class tasklet(object):
    '''http://www.stackless.com/wiki/Tasklets'''
    def __init__(self, func):
        self.func = func

    def __call__(self, *arg, **kw):
        '''将 genarator 加到就绪队列'''
        ready(self.func(*arg, **kw), None)

def run(task, obj):
    ''' 执行task '''
    try:
        result = task.send(obj)
    except StopIteration:
        pass
    else:
        if isinstance(result, command):
            # 给tasklet以执行 "系统命令" 的机会
            # 用户代码: yield command(func, ... )
            result(task)
        else:
            ready(task, None) # 加到就绪队列队尾，等待调度执行

def ready(task, obj):
    ''' 加入就绪队列 等待调度 '''
    readys.append( (task, obj) )

def schedule():
    ''' 调度就绪队列中的 tasklet '''
    while readys:
        task, obj = readys.popleft()
        run(task, obj)

# ============ test ===========

def simple_task(a):
    while True:
        print a
        yield None

def receiver(id, c):
    value = yield command(c.receive)
    print id,'receive', value
    while value:
        value = yield command(c.receive)
        print id,'received', value

def sender(id, c):
    value = 20
    while value:
        print id,'send',value
        yield command(c.send, value)
        value -= 1

def test_simple():
    tasklet(simple_task)(0)
    tasklet(simple_task)(10)
    tasklet(simple_task)(100)

def test_channel():
    c = channel()
    tasklet(receiver)('receiver1', c)
    tasklet(receiver)('receiver2', c)
    tasklet(sender)('sender1', c)
    c1 = channel()
    tasklet(receiver)('receiver3', c1)
    tasklet(sender)('sender2', c1)

if __name__=='__main__':
    #test_simple()
    test_channel()
    schedule()