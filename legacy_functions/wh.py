import sys
import operator
import time

from PIL import Image

from opencv.cv import *
from opencv.highgui import *

from pyblobs.BlobResult import CBlobResult
from pyblobs.Blob import CBlob

input_image_filename = "/home/ryan/ocr/test/image/thresh48.jpg"
bi_image  = cvLoadImage(input_image_filename)
gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
mask = cvCreateImage(cvGetSize(bi_image), 8, 1)
cvSet(mask,1)
initial_blobs = CBlobResult(gray_image, mask, 100, False)
initial_blob_count = initial_blobs.GetNumBlobs()

min_char_width=20
min_char_height=27
max_width_b4_cutoff=45
max_height_b4_cutoff=112
max_blob_area=2800

need_to_rerun = False
vp_blobs = []
hp_blobs = []

## W_GT_45
## for i in range(1,initial_blob_count): # if checking area, don't need to ignore 0
##     blob = initial_blobs.GetBlob(i)
##     width = blob.maxx-blob.minx
##     height = blob.maxy-blob.miny
##     area = blob.area
##     if area < max_blob_area:
##         if (width > max_width_b4_cutoff) and (height >= min_char_height):
##             blob_height = int(blob.maxy-blob.miny)
##             blob_width = int(blob.maxx-blob.minx)        
##             blob_size = cvSize(blob_width,blob_height)
##             blob_image = cvCreateImage(blob_size, 8, 1)
##             cvZero(blob_image)
##             blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))
##             zf_num = "%04d"
##             width_info = zf_num % blob_width
##             height_info = zf_num % blob_height
##             info = width_info + '__' + height_info + '__' + str(i)
##             cvSaveImage("/home/ryan/openCV/w/"+info+".jpg", blob_image)
            

## WH
for i in range(1,initial_blob_count):
    blob = initial_blobs.GetBlob(i)
    area = blob.area
    blob_height = int(blob.maxy-blob.miny)
    blob_width = int(blob.maxx-blob.minx)        
    blob_size = cvSize(blob_width,blob_height)
    blob_image = cvCreateImage(blob_size, 8, 1)
    cvZero(blob_image)
    blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))
    cvSaveImage("/home/ryan/openCV/blob_images/"+str(i)+".jpg", blob_image)



## vp_point_pairs = vp(initial_blobs.GetBlob(567), 3)
## drawing_image = cvCloneImage(bi_image)

## for point_pair in vp_point_pairs:
##     cvDrawLine(drawing_image, point_pair[0], point_pair[1], CV_RGB(0,245,0), 2, 8, 0)

## cvSaveImage("/home/ryan/openCV/output_images/5.jpg", bi_image)
## cvSaveImage("/home/ryan/openCV/output_images/6.jpg", drawing_image)

