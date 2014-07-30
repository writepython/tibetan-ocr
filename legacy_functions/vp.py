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

for i in range(1,initial_blob_count):
    blob = initial_blobs.GetBlob(i)
    area = blob.area
    blob_height = int(blob.maxy-blob.miny)
    blob_width = int(blob.maxx-blob.minx)        
    blob_size = cvSize(blob_width,blob_height)
    blob_image = cvCreateImage(blob_size, 8, 1)
    cvZero(blob_image)
    blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))
    zf_num = "%04d"
    width_info = zf_num % blob_width
    width_info = width_info + '__' + str(i)
    cvSaveImage("/home/ryan/openCV/blob_width/"+width_info+".jpg", blob_image)
    height_info = zf_num % blob_height
    height_info = height_info + '__'+ str(i)
    cvSaveImage("/home/ryan/openCV/blob_height/"+height_info+".jpg", blob_image)    
## vp_point_pairs = vp(initial_blobs.GetBlob(567), 3)
## drawing_image = cvCloneImage(bi_image)

## for point_pair in vp_point_pairs:
##     cvDrawLine(drawing_image, point_pair[0], point_pair[1], CV_RGB(0,245,0), 2, 8, 0)

## cvSaveImage("/home/ryan/openCV/output_images/5.jpg", bi_image)
## cvSaveImage("/home/ryan/openCV/output_images/6.jpg", drawing_image)

