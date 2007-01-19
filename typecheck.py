# coding: utf-8
class TypecheckError(Exception):pass

def typecheck(*types, **kwtypes):

    def type_checker(func):
        'the decorator'
        all_args = func.func_code.co_varnames # all the argument names
        
        # check the type definition
        n_types = len(types)
        if n_types>len(all_args):
            raise TypecheckError, '%s() has not so meny arguments %d'%\
                    (func.__name__, n_types)
        for k in kwtypes.keys():
            if not k in all_args:
                raise TypecheckError, \
                    '%s() has not this keyword argument %r'%\
                            (func.__name__, k)

        pos_args = all_args[:-len(func.func_defaults)] # position argument names
        typecheck_map = dict( zip(pos_args[:len(types)], types) ) # map: argument name => type
        typecheck_map.update(kwtypes)

        # check the default argument's type
        defaults = zip( all_args[-len(func.func_defaults):], func.func_defaults )
        for k,v in defaults:
            t = typecheck_map.get(k)
            if t and not isinstance(v, t):
                raise TypecheckError, \
                'the default value %r of argument %r is not type %r' % \
                        (v, k, t)

        def new_func(*args, **kw):
            'the wrapper function'
            check(args, kw)
            func(*args, **kw)

        def check(args, kw):
            'do the type checking'
            flag_map = {} # record if a argument has been bound.
            # check the input position arguments
            for name, value in zip(all_args[:len(args)], args):
                t = typecheck_map.get(name)
                if t:
                    if not isinstance(value, t):
                        raise TypecheckError, 'the value %r of argument %r is not type %r' % \
                                (value, name, typecheck_map[name])
                    flag_map[name] = True # this name has been bound.
            # check the input keyword arguments
            for k,v in kw.items():
                if flag_map.get(k):
                    raise TypeError, '%s() got multiple values for keyword argument %r'%\
                            (func.__name__, k)
                t = typecheck_map.get(k)
                if t:
                    if not isinstance(v, t):
                        raise TypecheckError, 'the value %r of argument %r is not type %r' % \
                                (v, k, t)

        new_func.__name__ = new_func.func_name = func.func_name
        return new_func

    return type_checker

# test...

def print_call(func, args, kw):
    if args and kw:
        print 'call %s(%s, %s)' % \
                (func.__name__, ', '.join(map(repr,args)), 
                    ', '.join('='.join((k, repr(v))) for k, v in kw.items()))
    elif args:
        print 'call %s(%s)' % \
                (func.__name__, ', '.join(map(repr,args)))
    elif kw:
        print 'call %s(%s)' % \
                (func.__name__, 
                    ', '.join('='.join((k, repr(v))) for k, v in kw.items()))

def test_call(func, *args, **kw):
    print_call(func, args, kw)
    func(*args, **kw)

def expect_exception(exce, func, *args, **kw):
    print_call(func, args, kw)
    try:
        func(*args, **kw)
    except exce, e:
        print exce.__name__, ':', e
        print
    else:
        assert False

@typecheck(int, str, c=int)
def temp(a, b, c=1):
    pass

test_call(temp, 1, 'hello')
test_call(temp, 1, 'hello', c=4)
test_call(temp, 1, b='hello', c=4)
test_call(temp, a=1, b='hello', c=4)
print
expect_exception(TypecheckError, temp, 1, 2)
expect_exception(TypecheckError, temp, 1, 'hello', c='hello')
expect_exception(TypeError, temp, 1, c=1)

@typecheck(int, str, int)
def temp(a, b, c=1):
    pass

@typecheck(a=int, b=str, c=int)
def temp(a, b, c=1):
    pass

try:
    @typecheck(int, str, d=int)
    def temp(a, b, c=1):
        pass
except TypecheckError, e:
    print e
    print
else:
    assert False

try:
    @typecheck(int, str, c=str)
    def temp(a, b, c=1):
        pass
except TypecheckError, e:
    print e
    print
else:
    assert False

try:
    @typecheck(int, str, int, int)
    def temp(a, b, c=1):
        pass
except TypecheckError, e:
    print e
    print
else:
    assert False

print 'test success'
