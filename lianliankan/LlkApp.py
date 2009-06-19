from pyjamas.Canvas2D import Canvas, CanvasImage
from pyjamas.ui.Image import Image
from pyjamas.ui.RootPanel import RootPanel
from config import uwidth,uheight,cwidth,cheight
from pyjamas.Timer import Timer

def trace(func):
    def new_func(*args, **kwargs):
        result = func(*args, **kwargs)
        console.log(func)
        console.log(args, kwargs)
        console.log(result)
        return result
    return new_func

class Listener:
    def __init__(self, onsuccess=None, onerror=None):
        self.onsuccess = onsuccess
        self.onerror = onerror
    @trace
    def onLoad(self, img):
        if self.onsuccess:
            console.log('onload')
            self.onsuccess(img)
    @trace
    def onError(self, img):
        if self.onerror:
            console.log('onerror')
            self.onerror(img)

@trace
def load_image(url, listener=None):
    img = Image()
    img.onBrowserEvent = trace(img.onBrowserEvent)
    img.onAttach()
    if listener:
        img.addLoadListener(listener)
    img.setUrl(url)
    return img

class Box(object):
    def __init__(self, img, xth, yth):
        self.img = img
        self.xth = xth
        self.yth = yth
        self.x = xth*uwidth
        self.y = yth*uheight

    def update(self, ticks):
        self.x += ticks
        self.y += ticks

    def draw(self, ctx):
        ctx.drawImage(self.img, self.x, self.y, uwidth, uheight,
                self.x, self.y, uwidth, uheight)

class LlkCanvas(Canvas):
    def __init__(self, width, height):
        super(LlkCanvas, self).__init__(width, height)
        self.width,self.height = width,height
        self.img = CanvasImage('output.png', self)
        self.objects = []

    def draw(self):
        ctx = self.context
        ctx.clearRect(0,0,self.width,self.height)
        for obj in self.objects:
            obj.draw(ctx)

    def update(self):
        self.ticks += 1
        for obj in self.objects:
            obj.update(1)

    def onTimer(self, t):
        self.update()
        self.draw()

    def add(self, obj):
        self.objects.append(obj)

    def onLoad(self, img=None):
        if self.img == img:
            self.draw()

    def onError(self, img=None):
        #console.log('load img error')
        pass

if __name__ == '__main__':
    canvas = LlkCanvas(500,500)
    RootPanel().add(canvas)
    img = canvas.img
    canvas.add( Box(img, 1,2) )
    canvas.add( Box(img, 5,2) )
    canvas.add( Box(img, 1,1) )
    canvas.add( Box(img, 2,2) )
    canvas.add( Box(img, 2,3) )
    canvas.add( Box(img, 5,3) )
    canvas.add( Box(img, 1,3) )
    canvas.add( Box(img, 2,8) )
    canvas.add( Box(img, 1,4) )
    Timer(object=canvas).scheduleRepeating(500)
    #load_image('output.png', Listener( (lambda img:canvas.draw(img)) ))
