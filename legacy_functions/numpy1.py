import sys

import opencv, numpy
from opencv import highgui as hg

def run():
    filename = 'C:\\Documents and Settings\\rmccormack\\Desktop\\work_projects\\openCV\\test\\test1.jpg'
    im = hg.cvLoadImage(filename)
    if not im:
        print "Error opening %s" % filename
        sys.exit(-1)
    im2 = opencv.cvCreateImage(opencv.cvGetSize(im),8, 4)
    opencv.cvCvtColor(im,im2,opencv.CV_BGR2BGRA)
    buffer = numpy.fromstring(im2.imageData,dtype=numpy.uint32).astype(numpy.float32)
    buffer.shape=(im2.width, im2.height)
    return buffer
