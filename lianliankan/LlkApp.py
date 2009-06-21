from pyjamas import DOM
from pyjamas.Canvas2D import Canvas, CanvasImage
from pyjamas.ui.Image import Image
from pyjamas.ui.RootPanel import RootPanel
from pyjamas import Window
from config import uwidth,uheight,cwidth,cheight
from pyjamas.Timer import Timer
from random import randint
import math
from lianliankan import checkllk

def sample(population, k):
    n = len(population)
    if not (0 <= k and k <= n):
        raise ValueError, "sample larger than population"
    random = math.random
    _int = int
    result = []
    for i in range(k):
        result.append(None)
    setsize = 21        # size of a small set minus size of an empty list
    if k > 5:
        setsize += 4 ** math.ceil(math.log(k * 3, 4)) # table size for big sets
    if n <= setsize or hasattr(population, "keys"):
        # An n-length list is smaller than a k-length set, or this is a
        # mapping type so the other algorithm wouldn't work.
        pool = list(population)
        for i in range(k):         # invariant:  non-selected at [0,n-i)
            j = _int(random() * (n-i))
            result[i] = pool[j]
            pool[j] = pool[n-i-1]   # move non-selected item into vacancy
    else:
        try:
            selected = set()
            selected_add = selected.add
            for i in range(k):
                j = _int(random() * n)
                while j in selected:
                    j = _int(random() * n)
                selected_add(j)
                result[i] = population[j]
        except (TypeError, KeyError):   # handle (at least) sets
            if isinstance(population, list):
                raise
            return self.sample(tuple(population), k)
    return result

def trace(func):
    def new_func(*args, **kwargs):
        result = func(*args, **kwargs)
        console.log(func)
        console.log(args, kwargs)
        console.log(result)
        return result
    return new_func

class ImgObj(object):
    def __init__(self, img, xth, yth):
        self.img = img
        self.x,self.y = xth*uwidth,yth*uheight
    def draw(self, ctx, x, y):
        ctx.drawImage(self.img, self.x, self.y, uwidth, uheight,
                x, y, uwidth, uheight)

class BasicBox(object):
    def __init__(self, position, imgobj, app):
        self.img = imgobj
        self.xth,self.yth = position
        self.x,self.y = self.xth*uwidth,self.yth*uheight
        self.app = app
        self.ctx = app.context
        self.selected = False
        self.alive = True
    def update(self, ticks):
        return False

    def draw(self):
        if not self.alive:
            return False
        ctx = self.ctx
        self.img.draw(ctx, self.x, self.y)
        if self.selected:
            # draw border
            ctx.strokeRect(self.x+1, self.y+1, uwidth-2, uheight-2)
    def toggleSelect(self):
        self.selected = not self.selected
        self.draw()
    def doSelect(self):
        self.selected = True
        self.draw()
    def unSelect(self):
        self.selected = False
        self.draw()
    def clear(self):
        self.ctx.clearRect(self.x, self.y, uwidth, uheight)

    def dead(self):
        self.clear()
        self.alive = False
class LlkCanvas(Canvas):
    def __init__(self, width, height):
        super(LlkCanvas, self).__init__(width, height)
        self.width,self.height = width,height
        self.img = CanvasImage('output.png', self)
        self.objects = []
        self.addClickListener(self.onClick)
        self.addKeyboardListener(self)
        self.selected_box = None
    def init_map(self, width,height):
        self.map_width,self.map_height = width,height
        self.map = []
        for x in range(self.map_height):
            line = []
            for y in range(self.map_width):
                line.append(0)
            self.map.append(line)
    def onTick(self, tick, force_draw=False):
        updated = False
        for obj in self.objects:
            if obj.alive and obj.update(tick):
                updated = True
        if updated or force_draw:
            ctx = self.context
            ctx.lineWidth = 2
            ctx.clearRect(0,0,self.width,self.height)
            for obj in self.objects:
                if obj.alive:
                    obj.draw()
    def onTimer(self, t=None):
        self.ticks += 1
        self.onTick(1)
    def add(self, obj):
        self.objects.append(obj)

    def setBox(self, xth, yth, imgobj):
        box = BasicBox( (xth,yth), imgobj, self)
        self.map[yth][xth] = box
        self.add(box)
    def onClick(self, sender, evt):
        x = DOM.eventGetClientX(evt)-DOM.getAbsoluteLeft(self.getElement())
        y = DOM.eventGetClientY(evt)-DOM.getAbsoluteTop(self.getElement())
        xth = int(x/uwidth)
        yth = int(y/uheight)
        box = self.map[yth][xth]
        if not box:
            return
        box.toggleSelect()
        if not box.selected:
            self.selected_box = None
        elif self.selected_box==None:
            self.selected_box = box
        elif box.img != self.selected_box.img:
            # change selection
            self.selected_box.unSelect()
            self.selected_box = box
        else:
            sbox = self.selected_box
            print 'check'
            result = False
            if box.xth<sbox.xth:
                print (box.yth,box.xth), (sbox.yth,sbox.xth)
                result = checkllk(self.map, (box.yth,box.xth), (sbox.yth,sbox.xth))
            else:
                print (sbox.yth,sbox.xth), (box.yth,box.xth)
                result = checkllk(self.map, (sbox.yth,sbox.xth), (box.yth,box.xth))
            if result:
                print 'path:', result
                sbox.dead()
                self.map[sbox.yth][sbox.xth] = 0
                box.dead()
                self.map[box.yth][box.xth] = 0
                self.selected_box = None
            else:
                print 'fail'
                self.selected_box.unSelect()
                self.selected_box = box
    def onKeyPress(self, sender, code, modifiers):
        print code
        if code == 'c'.charCodeAt() and self.selected_box!=None:
            sbox = self.selected_box
            sbox.dead()
            self.map[sbox.yth][sbox.xth] = 0
            self.selected_box = None
    def onKeyDown(self, sender, code, modifiers):
        pass
    def onKeyUp(self, sender, code, modifiers):
        pass
    def onLoad(self, img=None):
        if self.img == img:
            self.onTick(1, True)
            Timer(object=canvas).scheduleRepeating(100)
    def onError(self, img=None):
        #console.log('load img error')
        pass

if __name__ == '__main__':
    canvas = LlkCanvas(int(Window.getClientWidth()), int(Window.getClientHeight()))
    RootPanel().add(canvas)
    img = canvas.img
    imgobjs = []
    for i in range(10):
        xth = i%cwidth
        yth = int(i/cheight)
        print xth, yth
        imgobj = ImgObj(img,xth,yth)
        imgobjs.append(imgobj)

    #imgobjs = sample(imgobjs, len(imgobjs))
    map = \
   [[0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,1,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,1,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
    [0,1,1,1,1,0,0,0,1,1,1,0,0,0,1,1,0,1,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,0,1,0,0]]

    positions = []
    for y,line in enumerate(map):
        for x,position in enumerate(line):
            if position!=0:
                positions.append( (x,y) )
    canvas.init_map(len(map[0]), len(map))
    candidate_imgs = []
    img_count = len(imgobjs)
    for i in range( len(positions)/2 ):
        candidate_imgs.append(imgobjs[i%10])
    for i in range(len(candidate_imgs)):
        candidate_imgs.append(candidate_imgs[i])
    random_imgs = sample(candidate_imgs, len(candidate_imgs))
    for idx, pos in enumerate(positions):
        x, y = pos
        imgobj = random_imgs[idx]
        canvas.setBox(x, y, imgobj)
