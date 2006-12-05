#coding:utf-8
from collections import deque

'''
http://www.stackless.com/
'''

debuglevel = 0

readys = deque() # ��������

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
        self.senders = deque() # ���Ͷ��� Ԫ�أ�(tasklet, obj)
        self.receivers = deque() # ���ն��� Ԫ�أ�tasklet

    def send(self, sender, obj):
        '''��channel�з������ݣ����û�ý����ߣ����ø�tasklet�ȴ�'''
        if debuglevel:
            print 'tasklet:',sender,'send data:',obj,';receivers:',len(self.receivers)
        if self.receivers:
            receiver = self.receivers.popleft()
            ready(sender, None)
            run(receiver, obj)
        else:
            self.senders.append( (sender, obj) )

    def receive(self, receiver):
        ''' ��channel�н������ݣ����û�÷����ߣ����ø�tasklet�ȴ�'''
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
        '''�� genarator �ӵ���������'''
        ready(self.func(*arg, **kw), None)

def run(task, obj):
    ''' ִ��task '''
    try:
        result = task.send(obj)
    except StopIteration:
        pass
    else:
        if isinstance(result, command):
            # ��tasklet��ִ�� "ϵͳ����" �Ļ���
            # �û�����: yield command(func, ... )
            result(task)
        else:
            ready(task, None) # �ӵ��������ж�β���ȴ�����ִ��

def ready(task, obj):
    ''' ����������� �ȴ����� '''
    readys.append( (task, obj) )

def schedule():
    ''' ���Ⱦ��������е� tasklet '''
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