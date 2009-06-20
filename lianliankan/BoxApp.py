from pyjamas.Canvas2D import Canvas, CanvasImage
from pyjamas.ui.Image import Image
from pyjamas.ui.RootPanel import RootPanel
from pyjamas import Window
from config import uwidth,uheight,cwidth,cheight
from pyjamas.Timer import Timer
from random import randint

def trace(func):
    def new_func(*args, **kwargs):
        result = func(*args, **kwargs)
        console.log(func)
        console.log(args, kwargs)
        console.log(result)
        return result
    return new_func

class BasicBox(object):
    def __init__(self, img, position, speed, app):
        self.img = img
        self.xth,self.yth = position
        self.x = self.img_x = self.xth*uwidth
        self.y = self.img_y = self.yth*uheight
        self.xspeed,self.yspeed = speed
        self.app = app

    def update(self, ticks):
        width,height = self.app.width,self.app.height
        if self.x>width and self.xspeed>0:
            self.xspeed = -self.xspeed
        elif self.x<0 and self.xspeed<0:
            self.xspeed = -self.xspeed
        if self.y>height and self.yspeed>0:
            self.yspeed = -self.yspeed
        elif self.y<0 and self.yspeed<0:
            self.yspeed = -self.yspeed

        self.x += self.xspeed * ticks
        self.y += self.yspeed * ticks

    def draw(self, ctx):
        ctx.drawImage(self.img, self.img_x, self.img_y, uwidth, uheight,
                self.x, self.y, uwidth, uheight)

class StaticBox(BasicBox):
    def update(self, ticks):
        pass

class LlkCanvas(Canvas):
    def __init__(self, width, height):
        super(LlkCanvas, self).__init__(width, height)
        self.width,self.height = width,height
        self.img = CanvasImage('output.png', self)
        self.objects = []

    def onTimer(self, t=None):
        self.ticks += 1
        for obj in self.objects:
            obj.update(2)
        ctx = self.context
        ctx.clearRect(0,0,self.width,self.height)
        for obj in self.objects:
            obj.draw(ctx)

    def add(self, obj):
        self.objects.append(obj)

    def onLoad(self, img=None):
        if self.img == img:
            self.onTimer()

    def onError(self, img=None):
        #console.log('load img error')
        pass

if __name__ == '__main__':
    canvas = LlkCanvas(int(Window.getClientWidth()), int(Window.getClientHeight()))
    RootPanel().add(canvas)
    img = canvas.img
    for i in range(100):
        canvas.add( BasicBox(img, (randint(0,20),randint(0,20)), (randint(0,10), randint(0,10)), canvas) )
    Timer(object=canvas).scheduleRepeating(100)
    #load_image('output.png', Listener( (lambda img:canvas.draw(img)) ))
