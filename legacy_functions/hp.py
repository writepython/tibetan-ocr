import sys
import operator
import time

from PIL import Image

from opencv.cv import *
from opencv.highgui import *

from pyblobs.BlobResult import CBlobResult
from pyblobs.Blob import CBlob

def hp(blob, suspected_num_chars=2, min_char_height=27):
    rowsum_rownum_tuples = []
    hp_rows = []
    hp_point_pairs = []

    blob_height = int(blob.maxy-blob.miny)
    blob_width = int(blob.maxx-blob.minx)
    blob_size = cvSize(blob_width,blob_height)
    blob_image = cvCreateImage(blob_size, 8, 1)
    cvZero(blob_image)

## FOR WHITE BG
    blob_image_2 = cvCreateImage(blob_size, 8, 3)    
    cvRectangle(blob_image_2, cvPoint(0,0), cvPoint(blob_width, blob_height), CV_RGB(255,255,255), CV_FILLED, 8, 0)
    blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))
    
## TO SKIP PIXELS AT LEFT AND RIGHT MARGIN
    num_rows = blob_image.rows
    num_rows_minus_min_char_height = num_rows - min_char_height
## TO SKIP PIXELS AT LEFT AND RIGHT MARGIN (NOT BASED ON VARAIBLE)
##     num_rows = blob_image.rows
##     num_rows_minus_arb_value = num_rows - 5

    for (i, row) in enumerate(blob_image.rowrange()):
## TO SKIP PIXELS AT LEFT AND RIGHT MARGIN
        if i+1 < min_char_height or i > num_rows_minus_min_char_height:
            continue
## TO SKIP PIXELS AT LEFT AND RIGHT MARGIN (NOT BASED ON VARAIBLE)
##         if i < 5 or i > num_rows_minus_arb_value:
##             continue
        row_sum = cvSum(row)
        rowsum_rownum_tuples.append((int(row_sum[0]),i+1))

    rowsum_rownum_tuples.sort()
    chars_cut = 1

    for (i, rowsum_rownum) in enumerate(rowsum_rownum_tuples):
        if chars_cut >= suspected_num_chars:
            break
        if i == 0:
            new_hp_row = rowsum_rownum[1]
            print "first_hp_row ", new_hp_row
            point1 = cvPoint(int(blob.minx), int(blob.miny)+int(new_hp_row))
            point2 = cvPoint(int(blob.maxx), int(blob.miny)+int(new_hp_row))            
            hp_point_pairs.append([point1,point2])
            hp_rows.append(new_hp_row)
            chars_cut += 1            
        else:
            new_hp_row = rowsum_rownum[1]            
            for hp_row in hp_rows:
                if not abs(hp_row-new_hp_row) < min_char_height:
                    print "new_hp_row ", new_hp_row
                    point1 = cvPoint(int(blob.minx), int(blob.miny)+int(new_hp_row))
                    point2 = cvPoint(int(blob.maxx), int(blob.miny)+int(new_hp_row))
                    hp_point_pairs.append([point1,point2])
                    hp_rows.append(new_hp_row)
                    chars_cut += 1

    if chars_cut != suspected_num_chars:
        info_string = "%04d__%04d__suspected_%02d__cut_%02d.jpg"
        info = info_string % (blob_width, blob_height, suspected_num_chars, chars_cut)
        cvSaveImage("/home/ryan/openCV/hp_blobs/"+info, blob_image)
    cvSaveImage("/home/ryan/openCV/output_images/7.jpg", blob_image)
    return hp_point_pairs

input_image_filename = "/home/ryan/ocr/test/image/thresh48.jpg"
bi_image  = cvLoadImage(input_image_filename)
gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
mask = cvCreateImage(cvGetSize(bi_image), 8, 1)
cvSet(mask,1)
initial_blobs = CBlobResult(gray_image, mask, 100, False)
initial_blob_count = initial_blobs.GetNumBlobs()

hp_point_pairs = hp(initial_blobs.GetBlob(2865), 2)
drawing_image = cvCloneImage(bi_image)

for point_pair in hp_point_pairs:
    cvDrawLine(drawing_image, point_pair[0], point_pair[1], CV_RGB(0,245,0), 2, 8, 0)

cvSaveImage("/home/ryan/openCV/output_images/5.jpg", bi_image)
cvSaveImage("/home/ryan/openCV/output_images/6.jpg", drawing_image)
