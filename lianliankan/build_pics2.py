from config import uwidth,uheight,cwidth,cheight
width = uwidth*cwidth
height = uheight*cheight

def main():
    import os
    from PIL import Image
    target_img = Image.new('RGB', (width,height))
    counter = -1
    path = './resource/'
    for filename in os.listdir(path):
        if filename.lower().endswith('.jpg'):
            fullname = path+filename
            img = Image.open(fullname)
            img = img.resize( (uwidth,uheight) )
            counter += 1
            xth = counter%cwidth
            yth = int(counter/cheight)
            target_img.paste(img, (xth*uwidth,yth*uheight))

    target_img.save('output2.png')

if __name__ == '__main__':
    main()
