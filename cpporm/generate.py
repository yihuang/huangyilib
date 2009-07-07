#!/usr/bin/env python
from mako.template import Template
from config import cfg
def to_classname(name):
    return ''.join(map(str.title, name.split('_')))

tpl = Template(filename='table.cpp.tpl')
cfg.Tbl = to_classname(cfg.tbl)
print >>open('table.cpp','w'), tpl.render(**cfg)
