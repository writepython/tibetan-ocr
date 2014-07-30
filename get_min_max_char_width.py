import os
import sys
import operator
import time

from PIL import Image

from opencv.cv import *
from opencv.highgui import *

from pyblobs.BlobResult import CBlobResult
from pyblobs.Blob import CBlob # Note: This must be imported in order to destroy blobs and use other methods

def get_min_max_char_width():
    cwd = os.getcwd()    
    char_dir_path = cwd + '/characters/WIDTH/'
    for char in os.listdir(char_dir_path):
        bi_image  = cvLoadImage(char_dir_path+char)
        gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
        cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
        mask = cvCreateImage(cvGetSize(bi_image), 8, 1)
        cvSet(mask,1)
        initial_blobs = CBlobResult(gray_image, mask, 100, False)
        initial_blob_count = initial_blobs.GetNumBlobs()
        print "initial_blob_count: ", initial_blob_count
        time.sleep(3)

    
if __name__ == '__main__':
    get_min_max_char_width()

    
