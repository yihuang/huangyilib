#!/usr/bin/env python
# coding: utf-8
import pygtk
pygtk.require('2.0')
import math, cairo, gtk, gobject

class Board(gtk.DrawingArea):
    #__gsignals__ = {
    #    'expose-event':'override',
    #}

    def __init__(self):
        super(Board, self).__init__()
        self.connect('motion_notify_event', self.motion_notify_event)
        self.set_events(
                gtk.gdk.BUTTON_PRESS_MASK
                | gtk.gdk.POINTER_MOTION_MASK
                | gtk.gdk.POINTER_MOTION_HINT_MASK
                )
        self.points = []

    #def do_expose_event(self, event):
    #    cr = self.window.cairo_create()
    #    cr.rectangle(event.area.x, event.area.y,
    #            event.area.width, event.area.height)
    #    cr.clip()
    #    self.draw(cr, *self.window.get_size())

    def motion_notify_event(self, sender, event):
        if event.is_hint:
            x,y,state = event.window.get_pointer()
        else:
            x,y,state = event.x,event.y,event.state
        if state&gtk.gdk.BUTTON1_MASK:
            self.stroke( (x, y) )

    def line(self, p1, p2, alpha):
        cr = self.window.cairo_create()
        cr.set_source_rgba(0,0,0,alpha)
        cr.move_to(*p1)
        cr.line_to(*p2)
        cr.stroke()

    def stroke(self, p1):
        x1,y1 = p1
        for p2 in self.points:
            x2,y2=p2
            dx=x1-x2
            dy=y1-y2
            dist = dx*dx+dy*dy
            if dist<1000:
                alpha = (1-dist/1000)*0.01
                self.line(p1, p2, alpha)
        self.points.append(p1)

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
