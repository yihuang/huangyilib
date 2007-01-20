# -*- coding: utf-8 -*-
'''
感觉楼主的这篇和上次用 python 实现 define 的那篇帖子，想说的都是
一个东西，就是静态语言中的 const，第一次初始化后不能修改的东西。

说起来，python 对象中其实是有这样的东西，就是 imutable object 。
不过常量针对的是名字而非对象，所以在 python 中常量的准确定义应该
是：在第一次绑定后不能重新绑定其他对象的名字。

遗憾的是 python 中没有这样的东西。

其实和类型检查、访问控制等东西一样，静态语言中常量是通过编译器在
编译时进行检查，而 python 就算实现那也只能是在运行时进行计算，势
必损耗性能，我想这也是 python 中没有这样的东西的原因。

但是正如 python 中的访问控制是通过对名字的约定来做的一样，其实常
量也比较适合这样做。

如果实在要用动态语言模拟 const，那么关键在于对名字的绑定进行控制。

下面总结一下各种做法：
'''

def a_const_value():
    '''
    方法1是通过使用函数替代对名字的直接访问，好像是比较傻的方法。
    不过 ruby 中函数调用可以省略括号就有点像了

    >>> a_const_value()
    'const'
    '''
    return 'const'

class Temp(object):
    '''
    class 中通过 property 可以做得更漂亮：

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

class ConstError(Exception):
    pass

class Consts(object):
    '''
    方法2是将常量名字放入一个 class 中统一进行管理：

    >>> consts = Consts()
    >>> consts.a = 2
    >>> consts.a
    2
    >>> consts.a = 3
    Traceback (most recent call last):
        ...
    ConstError: can't rebind const name

    不过需要注意的是，仍然可以通过 __dict__ 直接访问常量：
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
    或者让 class 自己指定那些是常量：

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

    使用这种方式，也可以直接通过 __dict__ 对常量进行修改：
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
