#!/usr/bin/env python
# coding: utf-8
import pygtk
pygtk.require('2.0')
import math, cairo, gtk, gobject,random
import time

class Board(gtk.DrawingArea):
    def __init__(self):
        super(Board, self).__init__()
        gtk.idle_add(self.start)
    def start(self):
        begin = time.time()
        for i in range(100000):
            cr = self.window.cairo_create()
            cr.set_operator(cairo.OPERATOR_XOR)
            cr.set_source_rgba(0,0,0,random.random())
            cr.move_to(random.randint(0,200), random.randint(0,200))
            cr.line_to(random.randint(0,200), random.randint(0,200))
            cr.stroke()
        end = time.time()
        print end-begin

def run(Klass):
    win = gtk.Window()
    win.connect('delete-event', gtk.main_quit)
    widget = Klass()
    widget.show()
    win.add(widget)
    win.present()
    gtk.main()

if __name__ == '__main__':
    run(Board)
