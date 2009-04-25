import gtk
import cairo
from utils import Position

class PngDrawer(object):
    def __init__(self):
        self.suf = cairo.ImageSurface(cairo.FORMAT_RGB24, 5000,5000)
        self.height = self.suf.get_height()
        cr = cairo.Context(self.suf)
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(1.0)
        self.cr = cr
    
    def transform(self, position):
        scale = 3
        x, y = 0, -1000
        return Position(position.x*7+x,  self.height-(position.y*7-y))

    def move_to(self, position):
        position = self.transform(position)
        self.cr.move_to(position.x, position.y)

    def line_to(self, position):
        position = self.transform(position)
        self.cr.line_to(position.x, position.y)

    def draw_end(self):
        import os, tempfile
        filename = '/tmp/result.png'
        self.cr.stroke()
        self.suf.write_to_png(filename)
        os.system('gnome-open '+filename)

class GtkDrawer(object):
    def __init__(self):
        win = gtk.Window()
        win.connect('delete-event', gtk.main_quit)
        win.set_default_size(400,300)
        cr = win.get_root_window().cairo_create()

        self.window = win
        self.cr = cr

    def draw_line(self, position1, position2):
        cr = self.cr
        cr.move_to(position1.x, position1.y)
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.line_to(position2.x, position2.y)

    def draw_end(self):
        self.cr.clip()
        self.window.show_all()
        gtk.main()
