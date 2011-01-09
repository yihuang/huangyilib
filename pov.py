#!/usr/bin/env python
import sys, os

class File:
    def __init__(self,fnam="out.pov",*items):
        self.file = open(fnam,"w")
        self.__indent = 0
        self.write(*items)
    def include(self,name):
        self.writeln( '#include "%s"'%name )
        self.writeln()
    def indent(self):
        self.__indent += 1
    def dedent(self):
        self.__indent -= 1
        assert self.__indent >= 0
    def block_begin(self):
        self.writeln( "{" )
        self.indent()
    def block_end(self):
        self.dedent()
        self.writeln( "}" )
        if self.__indent == 0:
            # blank line if this is a top level end
            self.writeln( )
    def write(self,*items):
        for item in items:
            if type(item) == str:
                self.include(item)
            else:
                item.write(self)
    def writeln(self,s=""):
        #print "    "*self.__indent+s
        self.file.write("    "*self.__indent+s+os.linesep)
class Vector:
    def __init__(self,*args):
        if len(args) == 1:
            self.v = args[0]
        else:
            self.v = args
    def __str__(self):
        return "<%s>" % ", ".join(map(str, self.v))
    def __repr__(self):
        return "Vector(%s)"%self.v
    def __mul__(self,other):
        return Vector( [r*other for r in self.v] )
    def __rmul__(self,other):
        return Vector( [other*r for r in self.v] )

class Item(object):
    def __init__(self,name,args=[],opts=[],**kwargs):
        self.name = name
        args=list(args)
        for i in range(len(args)):
            if instance(args, (tuple, list)):
                args[i] = Vector(args[i])
        self.args = args
        self.opts = opts
        self.kwargs=kwargs
    def append(self, item):
        self.opts.append( item )
    def write(self, file):
        file.writeln( self.name )
        file.block_begin()
        if self.args:
            file.writeln( ", ".join([str(arg) for arg in self.args]) )
        for opt in self.opts:
            if hasattr(opt,"write"):
                opt.write(file)
            else:
                file.writeln( str(opt) )
        for key,val in self.kwargs.items():
            if isinstance(val, (tuple, list)):
                val = Vector(*val)
                file.writeln( "%s %s"%(key,val) )
            else:
                file.writeln( "%s %s"%(key,val) )
        file.block_end()
    def __setattr__(self,name,val):
        self.__dict__[name]=val
        if name not in ["kwargs","args","opts","name"]:
            self.__dict__["kwargs"][name]=val
    def __setitem__(self,i,val):
        if i < len(self.args):
            self.args[i] = val
        else:
            i += len(args)
            if i < len(self.opts):
                self.opts[i] = val
    def __getitem__(self,i,val):
        if i < len(self.args):
            return self.args[i]
        else:
            i += len(args)
            if i < len(self.opts):
                return self.opts[i]

def init_fn(name, nargs=0):
    def __init__(self,*opts,**kwargs):
        args = opts[:nargs]
        opts = opts[nargs:]
        return Item.__init__(self,name,args,opts,**kwargs)
    return __init__

g = globals()
for name in [
    'texture',
    'pigment',
    'finish',
    'normal',
    'camera',
    'object',
    'background',
    ('light_source', 1),
    ('box', 2),
    ('cylinder', 3),
    ('plane', 2),
    ('torus', 2),
    ('cone', 4),
    ('sphere', 2),
    'union',
    'intersection',
    'difference',
    'merge',
]:
    if isinstance(name, tuple):
        name, nargs = name
    else:
        nargs = 0
    def init(self,*opts,**kwargs):
        Item.__init__(self,name,(),opts,**kwargs)
    klass = ''.join(map(str.title, name.split('_')))
    g[klass] = type(klass, (Item,), {
        '__init__': init_fn(name, nargs)
    })

def tutorial31():
    " from the povray tutorial sec. 3.1"
    file=File("demo.pov","colors.inc","stones.inc")
    cam = Camera(location=(0,2,-3),look_at=(0,1,2))
    sphere = Sphere( (0,1,2), 2, Texture(Pigment(color="Yellow")))
    light = LightSource( (2,4,-3), color="White")
    file.write( cam, sphere, light )

def spiral():
    from math import sqrt,sin,cos,pi
    " Fibonacci spiral "
    gamma = (sqrt(5)-1)/2
    file = File()
    Camera(location=(0,0,-128), look_at=(0,0,0)).write(file)
    LightSource((100,100,-100), color=(1,1,1)).write(file)
    LightSource((150,150,-100), color=(0,0,0.3)).write(file)
    LightSource((-150,150,-100), color=(0,0.3,0)).write(file)
    LightSource((150,-150,-100), color=(0.3,0,0)).write(file)
    theta = 0.0
    for i in range(200):
        r = i * 0.5
        color = 1,1,1
        v = [ r*sin(theta), r*cos(theta), 0 ]
        Sphere( v, 0.7*sqrt(i),
            Texture(
                Finish(
                    ambient = 0.0,
                    diffuse = 0.0,
                    reflection = 0.85,
                    specular = 1
                ),
                Pigment(color=color))
        ).write(file)
        theta += gamma * 2 * pi

if __name__ == '__main__':
    tutorial31()
