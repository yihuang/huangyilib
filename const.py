# -*- coding: utf-8 -*-
'''
�о�¥������ƪ���ϴ��� python ʵ�� define ����ƪ���ӣ���˵�Ķ���
һ�����������Ǿ�̬�����е� const����һ�γ�ʼ�������޸ĵĶ�����

˵������python ��������ʵ���������Ķ��������� imutable object ��
����������Ե������ֶ��Ƕ��������� python �г�����׼ȷ����Ӧ��
�ǣ��ڵ�һ�ΰ󶨺������°�������������֡�

�ź����� python ��û�������Ķ�����

��ʵ�����ͼ�顢���ʿ��Ƶȶ���һ������̬�����г�����ͨ����������
����ʱ���м�飬�� python ����ʵ����Ҳֻ����������ʱ���м��㣬��
��������ܣ�������Ҳ�� python ��û�������Ķ�����ԭ��

�������� python �еķ��ʿ�����ͨ�������ֵ�Լ��������һ������ʵ��
��Ҳ�Ƚ��ʺ���������

���ʵ��Ҫ�ö�̬����ģ�� const����ô�ؼ����ڶ����ֵİ󶨽��п��ơ�
'''

def a_const_value():
    '''
    ����1��ͨ��������������ֵ�ֱ�ӷ���
    >>> a_const_value()
    'const'
    '''
    return 'const'

class Temp(object):
    '''
    class ��ͨ�� property �������ø����ţ�
    >>> t = Temp()
    >>> t.a_const_value
    'const'
    >>> t.a_const_value = 'another value'
    Traceback (most recent call last):
        ...
    AttributeError: can't set attribute
    '''
    @property
    def a_const_value(self):
        return 'const'

'''
�������ַ�ʽ�����ǿ���ͨ������ consts.__dict__ ���� t.__consts__ ֱ�Ӵ�ȡ�������֡������վ����ǵÿ�Լ����
'''

class ConstError(Exception):
    pass

class Consts(object):
    '''
    ����2���Խ��������ַ���һ�� class ��ͳһ���й���

    >>> consts = Consts()
    >>> consts.a = 2
    >>> consts.a
    2
    >>> consts.a = 3
    Traceback (most recent call last):
        ...
    ConstError: can't rebind const name

    ������Ҫע����ǣ���Ȼ����ͨ�� __dict__ ֱ�ӷ��ʳ�����
    >>> consts.__dict__['a'] = 3
    >>> consts.a
    3
    '''
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ConstError, 'can\'t rebind const name'
        else:
            self.__dict__[name] = value

class ConstBase(object):
    '''
    ������ class �Լ�ָ����Щ�ǳ�����

    >>> class Temp(ConstBase):
    ...     __consts__ = {'a':None, 'b':2}
    ...     def __init__(self, a):
    ...         self.a = a
    ...
    >>> t = Temp(2)
    >>> t.a
    2
    >>> t.b
    2
    >>> t.a = 3
    Traceback (most recent call last):
        ...
    ConstError: can't rebind const name
    >>> t.b = 3
    Traceback (most recent call last):
        ...
    ConstError: can't rebind const name
    >>> t.c = 5
    >>> t.c
    5

    ʹ�����ַ�ʽ��Ҳ����ֱ��ͨ�� __dict__ �Գ��������޸ģ�
    >>> t.__dict__['a']= 3
    >>> t.a
    3
    '''
    __consts__ = {}
    def __setattr__(self, name, value):
        if name in self.__consts__:
            if self.__consts__[name] == None:
                self.__consts__[name] = value
            else:
                raise ConstError, 'can\'t rebind const name'
        else:
            super(ConstBase, self).__setattr__(name, value)
    def __getattr__(self, name):
        if name in self.__consts__:
            return self.__consts__[name]
        else:
            return super(ConstBase, self).__getattr__(name, value)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
