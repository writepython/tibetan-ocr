#!/usr/bin/python
import sys
from opencv.cv import *
from opencv.highgui import *

##abc = ['__class__', '__del__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattr__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__swig_destroy__', '__swig_getmethods__', '__swig_setmethods__', '__weakref__', '_s', 'append', 'block_max', 'cast', 'delta_elems', 'elem_size', 'first', 'flags', 'free_blocks', 'h_next', 'h_prev', 'header_size', 'hrange', 'pop', 'ptr', 'storage', 'this', 'total', 'v_next', 'v_prev', 'vrange']
### Get the size of the contour
##size = abs(cvContourArea(contour))
##
### Is convex
##is_convex = cvCheckContourConvexity(contour)
##for i in range(a[91].total):
##	print a[91][i]
def create_bbox():
    i=1
    d=[]
    #f=open('./abc.txt','w')
    
    raw_image_filename = './image/test_raw.jpg'
    bi_image_filename = './image/test_bi2.jpg'

    raw_image = cvLoadImage(raw_image_filename)
    bi_image = cvLoadImage(bi_image_filename)

    output_image = cvCloneImage(raw_image)
    gray = cvCreateImage(cvGetSize(bi_image), 8, 1)
    #output_image = cvCloneImage(white_image)
    #output_image = cvCloneImage(raw_image)
    cvCvtColor(bi_image, gray, cv.CV_BGR2GRAY)
    
    #cv.cvAdaptiveThreshold(bi_image, gray, 255, cv.CV_ADAPTIVE_THRESH_MEAN_C, cv.CV_THRESH_BINARY) 
    storage = cvCreateMemStorage(0)
    count, contours = cvFindContours (gray, storage, sizeof_CvContour, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, cvPoint (0,0))
##  Alt method
#    contours = cvApproxPoly(contours, sizeof_CvContour, storage, CV_POLY_APPROX_DP, 0, 1)
    for contour in contours.hrange():
        contour_size = abs(cvContourArea(contour))
        if 50 < contour_size < 9500:
            bbox = cvBoundingRect(contour, 0)
##        box_width = bbox.width
##        box_height = bbox.height
##        if 100 > box_width > 10:
##            if box_height > 15:  
            cvRectangle(output_image, cvPoint(int(bbox.x), int(bbox.y)),
                     cvPoint(int(bbox.x+bbox.width), int(bbox.y+bbox.height)),
                     CV_RGB(0,255,0), 1, 8, 0)      

    #cvDrawContours(output_image, contours, CV_RGB(255,0,0), CV_RGB(0,0,255), 2, 1, 8, cvPoint (0,0))
    cvSaveImage("./image/input.jpg", gray)
    cvSaveImage("./image/output.jpg", output_image)
    

if __name__ == "__main__":
    create_bbox()
