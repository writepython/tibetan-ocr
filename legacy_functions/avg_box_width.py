#!/usr/bin/python
import sys
from stats import mean, lmean, stdev, lstdev

from opencv.cv import *
from opencv.highgui import *

def get_avg_box_width():
    box_widths = []
    
    filename = './image/test_bi3.jpg'
    image = cvLoadImage(filename, CV_8UC1)
    storage = cvCreateMemStorage(0)
    input_image = cvCloneImage(image)
#    output_image = cvCloneImage(image)
    output_image = cvCreateImage(cvGetSize(input_image), 8, 3)
    cvCvtColor(input_image, output_image, CV_GRAY2BGR)
    count, contours = cvFindContours (input_image, storage, sizeof_CvContour, CV_RETR_CCOMP, CV_CHAIN_APPROX_NONE, cvPoint (0,0))
    for contour in contours.hrange():
        bbox = cvBoundingRect(contour, 0)
        box_width = bbox.width
        if 100 > box_width > 10:
            box_widths.append(box_width)
#    return box_widths
    width_mean = mean(box_widths)
    width_lmean = lmean(box_widths)
    width_stdev = stdev(box_widths)
    width_lstdev = lstdev(box_widths)    
    return (width_mean,width_lmean,width_stdev,width_lstdev)
