from config import uwidth,uheight,cwidth,cheight
width = uwidth*cwidth
height = uheight*cheight

def main():
    from PIL import Image
    import ImageDraw
    from random import randint
    target_img = Image.new('RGB', (width,height))
    canvas = ImageDraw.Draw(target_img)

    for xth in range(cwidth):
        for yth in range(cheight):
            x, y = (xth*uwidth, yth*uheight)
            canvas.rectangle( ( x,y, x+uwidth, y+uheight), fill=(randint(0,255), randint(0,255), randint(0,255)) )

    target_img.save('output.png')

if __name__ == '__main__':
    main()
