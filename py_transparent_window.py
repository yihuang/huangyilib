#!/usr/bin/python
# coding: utf-8
import math
import gtk
import cairo
import pango
import pangocairo

def draw_window(win, event):
   	win_width, win_height = win.get_size()

    ctx = win.window.cairo_create()
    ctx.set_operator(cairo.OPERATOR_SOURCE)

    ctx.set_source_rgba(1,0,1,.3)
    ctx.rectangle(0,0,win_width,win_height)
    ctx.fill()

    '''
    pat = cairo.LinearGradient (win_width/2, 0.0, win_width/2, win_height)
    pat.add_color_stop_rgba (0, 0, 0, 0, 1)
    pat.add_color_stop_rgba (1, 0, 1, 1, 0)

    ctx.rectangle(0,0,win_width,win_height)
    ctx.set_source(pat)
    ctx.fill()

    ctx.set_operator(cairo.OPERATOR_ADD)

    pat = cairo.RadialGradient (0.0, 0.0, 0.0,
                                0.0, 0.0, win_width*1.2)
    pat.add_color_stop_rgba (0.5, 1, 1, 1, 0)
    pat.add_color_stop_rgba (1, 0, 0, 0, 1)

    ctx.rectangle(0,0,win_width,win_height)
    ctx.set_source(pat)
    ctx.fill()
    '''

    ctx = pangocairo.CairoContext(ctx)
    layout = ctx.create_layout()
    layout.set_alignment(pango.ALIGN_CENTER)

    lyric_texts = '''
In the year of 2007
the 17th National Congress of the communist party was held
president hu described China's brand new future to the whole world
Since then the chinese people's life began to change
涛哥我爱你，我爱你，我爱你，都说你就是一个奇迹
想帮你刷刷碗做做饭擦擦地
大家都爱你
MUSIC
'''

    layout.set_markup('''
            <span font-desc="Sans Bold">%s</span>
            ''' % lyric_texts)
    ctx.set_source_rgba (0,1,0,1)
    ctx.move_to(0,0)
    ctx.show_layout(layout)
    ctx.fill()

win = gtk.Window()
win.connect('delete-event', gtk.main_quit)
win.connect('expose_event', draw_window)
win.set_default_size(400,300)
#win.set_decorated(False)

win.set_app_paintable(True)
screen = win.get_screen()
colormap = screen.get_rgba_colormap()
win.set_colormap(colormap)

win.show_all()
gtk.main()
