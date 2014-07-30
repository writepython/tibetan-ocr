#!/usr/bin/python

import sys

from opencv.cv import *
from opencv.highgui import *

from pyblobs.BlobResult import CBlobResult
from pyblobs.Blob import CBlob # Note: This must be imported in order to destroy blobs and use other methods

def output_images(input_image_filename, output_image_directory):
    bi_image  = cvLoadImage(input_image_filename)
    output_image = cvCloneImage(bi_image)
    gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
    
    mask = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvSet(mask,1)
    initial_blobs = CBlobResult(gray_image, mask, 100, False)
    #initial_blobs.filter_blobs(10, 10000)
    initital_blob_count = initial_blobs.GetNumBlobs()
    print initital_blob_count
    
    for i in range(initital_blob_count):
        blob = initial_blobs.GetBlob(i)
##         if 50 < blob.area < 9500:        
##             rect_dims.append((blob.minx,blob.miny,blob.maxx,blob.maxy,i))
##     for i in range(initital_blob_count):
##         blob = initial_blobs.GetBlob(i)
##         for rect_dim in rect_dims:
##             if blob.minx > rect_dim[0] and blob.miny > rect_dim[1] and blob.maxx < rect_dim[2] and blob.maxy < rect_dim[3]:
##                 bigger_blob = initial_blobs.GetBlob(rect_dim[4])
##                 new_blob = bigger_blob.CopyEdges(blob)
##                 final_blobs.AddBlob(new_blob)
##             else:
##                 final_blobs.AddBlob(blob)
##     new_blob_count = final_blobs.GetNumBlobs()
##     print new_blob_count
##     for i in range(new_blob_count):
##         blob = final_blobs.GetBlob(i)
        
            #print "%d: Area = %d" % (i, my_enumerated_blob.Area())
            #blob.FillBlob(output_image, CV_RGB(255,0,0), 0, 0)    
        cvRectangle(output_image,
                    cvPoint(int(blob.minx),int(blob.miny)),
                    cvPoint(int(blob.maxx),int(blob.maxy)),
                    CV_RGB(0,255,0), 1, 8, 0 
                    )

    cvSaveImage(output_image_directory+"input.jpg", gray_image)
    cvSaveImage(output_image_directory+"output.jpg", output_image)

def draw_bounding_boxes(input_image_filename, output_image_filename):
    bi_image  = cvLoadImage(input_image_filename)
    output_image = cvCloneImage(bi_image)
    gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
    
    mask = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvSet(mask,1)
    initial_blobs = CBlobResult(gray_image, mask, 100, False)
    #initial_blobs.filter_blobs(10, 10000)
    initital_blob_count = initial_blobs.GetNumBlobs()
    print initital_blob_count
    
    for i in range(initital_blob_count):
        blob = initial_blobs.GetBlob(i)
##         if 50 < blob.area < 9500:        
##             rect_dims.append((blob.minx,blob.miny,blob.maxx,blob.maxy,i))
##     for i in range(initital_blob_count):
##         blob = initial_blobs.GetBlob(i)
##         for rect_dim in rect_dims:
##             if blob.minx > rect_dim[0] and blob.miny > rect_dim[1] and blob.maxx < rect_dim[2] and blob.maxy < rect_dim[3]:
##                 bigger_blob = initial_blobs.GetBlob(rect_dim[4])
##                 new_blob = bigger_blob.CopyEdges(blob)
##                 final_blobs.AddBlob(new_blob)
##             else:
##                 final_blobs.AddBlob(blob)
##     new_blob_count = final_blobs.GetNumBlobs()
##     print new_blob_count
##     for i in range(new_blob_count):
##         blob = final_blobs.GetBlob(i)
        
            #print "%d: Area = %d" % (i, my_enumerated_blob.Area())
            #blob.FillBlob(output_image, CV_RGB(255,0,0), 0, 0)    
        cvRectangle(output_image,
                    cvPoint(int(blob.minx),int(blob.miny)),
                    cvPoint(int(blob.maxx),int(blob.maxy)),
                    CV_RGB(0,255,0), 1, 8, 0 
                    )

    cvSaveImage(output_image_filename, gray_image)
    cvSaveImage(output_image_filename, output_image)    

if __name__ == "__main__":
    if sys.argv[0]=="output_images":
        input_image_filename = sys.argv[1]
        output_image_directory  = sys.argv[2]
        output_images(input_image_filename, output_image_directory)
    elif sys.argv[0]=="draw_bounding_boxes":
        input_image_filename = sys.argv[1]
        output_image_filename  = sys.argv[2]
        draw_bounding_boxes(input_image_filename, output_image_filename)
    else:
        print """
        Options:
        1. output_images [input_image_filename] [output_image_directory]
        2. draw_bounding_boxes [input_image_filename] [output_image_filename]
        """
        
### Get the size of the contour
##size = abs(cvContourArea(contour))

### Is convex
##is_convex = cvCheckContourConvexity(contour)
