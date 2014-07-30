from PIL import Image

for f in os.listdir('.'):
    im = Image.open(os.path.join(os.getcwd(),f))
    width,height = im.size
    print "w:",width,"h:",height

