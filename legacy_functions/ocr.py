#!/usr/bin/python

import sys
import os
import operator
import time
import datetime

from PIL import Image

from opencv.cv import *
from opencv.highgui import *

from pyblobs.BlobResult import CBlobResult
from pyblobs.Blob import CBlob # Note: This must be imported in order to destroy blobs and use other methods

#num_blobs_found = True

def output_blob(blob,output_dir="/home/ryan/openCV/b/"):
    blob_height = int(blob.maxy-blob.miny)
    blob_width = int(blob.maxx-blob.minx)
    blob_size = cvSize(blob_width,blob_height)
    blob_image = cvCreateImage(blob_size, 8, 1)
    cvZero(blob_image)
    blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))
    info_string = "w_%04d__h_%04d__miny_%04d.png"
    info = info_string % (blob_width, blob_height, int(blob.miny))
    cvSaveImage(output_dir+info, blob_image)
    
def vp(blob, min_char_width, show_blobs=True):
    def get_col_miny_maxy(column):
        miny = 0
        maxy = 0
        for i,pixel_value in enumerate(column):
            if pixel_value == 255:
                maxy = i
                if not miny:
                    miny = i
        return miny,maxy

    colsum_colnum_col_tuples = []
    vp_point_pairs = []

    blob_height = int(blob.maxy-blob.miny)
    blob_width = int(blob.maxx-blob.minx)
    blob_size = cvSize(blob_width,blob_height)
    blob_image = cvCreateImage(blob_size, 8, 1)
    cvZero(blob_image)
    blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))

    if show_blobs:
        blob_image_2 = cvCreateImage(blob_size, 8, 3)    
        cvRectangle(blob_image_2, cvPoint(0,0), cvPoint(blob_width, blob_height), CV_RGB(255,255,255), CV_FILLED, 8, 0)
        blob.FillBlob(blob_image_2, CV_RGB(0,255,0), -1*int(blob.minx), -1*int(blob.miny))        

## TO SKIP PIXELS AT LEFT AND RIGHT MARGIN
    num_cols = int(blob_image.cols)
    num_cols_minus_min_char_width = num_cols - min_char_width

    for (i, col) in enumerate(blob_image.colrange()):
## TO SKIP PIXELS AT LEFT AND RIGHT MARGIN
        if (i+1 < min_char_width) or (i > num_cols_minus_min_char_width):
            continue
        col_sum = cvSum(col)
        colsum_colnum_col_tuples.append((int(col_sum[0]),i,col))

    colsum_colnum_col_tuples.sort()
#    print "colsum_colnum_col_tuples", colsum_colnum_col_tuples

    new_vp_colsum_colnum_col = colsum_colnum_col_tuples[0]
    new_vp_col = new_vp_colsum_colnum_col[1]
    delta_miny, delta_maxy = get_col_miny_maxy(new_vp_colsum_colnum_col[2])
    point1 = cvPoint(int(blob.minx)+new_vp_col, int(blob.miny)+delta_miny)
    point2 = cvPoint(int(blob.minx)+new_vp_col, int(blob.miny)+delta_maxy)
    vp_point_pairs = (point1,point2)

    if show_blobs:
        point1 = cvPoint(0+new_vp_col, 0+delta_miny)
        point2 = cvPoint(0+new_vp_col, 0+delta_maxy)
        cvDrawLine(blob_image_2, point1, point2, CV_RGB(255,0,255), 2, 8, 0)
        info_string = "%s__%04d__%04d.png"
        info = info_string % (str(datetime.datetime.now()), blob_width, blob_height)
        cvSaveImage("/home/ryan/openCV/vp_blobs_time/"+info, blob_image_2)
        info_string = "%04d__%04d__%s.png"
        info = info_string % (blob_width, blob_height, str(datetime.datetime.now())) 
        cvSaveImage("/home/ryan/openCV/vp_blobs_dimensions/"+info, blob_image_2)        
#    cvReleaseImage(blob_image)    
    return vp_point_pairs

def hp(blob, acceptable_row_ranges, min_char_height=27, show_blobs=True):
    print "NEW HP BLOB"
    def get_row_minx_maxx(row):
        minx = 0
        maxx = 0
        for i,pixel_value in enumerate(row):
            if pixel_value == 255:
                maxx = i
                if not minx:
                    minx = i
        return minx,maxx

    hp_point_pairs = []

    blob_height = int(blob.maxy-blob.miny)
    blob_width = int(blob.maxx-blob.minx)
    blob_size = cvSize(blob_width,blob_height)
    blob_image = cvCreateImage(blob_size, 8, 1)
    cvZero(blob_image)
    blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))

    if show_blobs:
        hp_point_pairs_2 = []        
        blob_image_2 = cvCreateImage(blob_size, 8, 3)    
        cvRectangle(blob_image_2, cvPoint(0,0), cvPoint(blob_width, blob_height), CV_RGB(255,255,255), CV_FILLED, 8, 0)
        blob.FillBlob(blob_image_2, CV_RGB(0,255,0), -1*int(blob.minx), -1*int(blob.miny))
    
    for acceptable_row_range in acceptable_row_ranges:
        rowsum_rownum_row_tuples = []
        hp_rows = []

        for (i, row) in enumerate(blob_image.rowrange()):
            if acceptable_row_range[0] <= i <= acceptable_row_range[1]:
                row_sum = cvSum(row)
                rowsum_rownum_row_tuples.append((int(row_sum[0]),i,row))
        rowsum_rownum_row_tuples.sort()
        lowest_rowsum_tuple = rowsum_rownum_row_tuples[0]
        new_hp_row = lowest_rowsum_tuple[1]
        delta_minx, delta_maxx = get_row_minx_maxx(lowest_rowsum_tuple[2])
        point1 = cvPoint(int(blob.minx)+delta_minx, int(blob.miny)+new_hp_row)
        point2 = cvPoint(int(blob.minx)+delta_maxx, int(blob.miny)+new_hp_row)
        hp_point_pairs.append([point1,point2])
    if show_blobs:
        for acceptable_row_range in acceptable_row_ranges:
            rowsum_rownum_row_tuples = []
            hp_rows = []

            for (i, row) in enumerate(blob_image.rowrange()):
                if acceptable_row_range[0] <= i <= acceptable_row_range[1]:
                    row_sum = cvSum(row)
                    rowsum_rownum_row_tuples.append((int(row_sum[0]),i,row))
            rowsum_rownum_row_tuples.sort()
            lowest_rowsum_tuple = rowsum_rownum_row_tuples[0]
            new_hp_row = lowest_rowsum_tuple[1]
            delta_minx, delta_maxx = get_row_minx_maxx(lowest_rowsum_tuple[2])
            point1 = cvPoint(0+delta_minx, 0+new_hp_row)
            point2 = cvPoint(0+delta_maxx, 0+new_hp_row)
            hp_point_pairs_2.append([point1,point2])        
        for point_pair in hp_point_pairs_2:
            cvDrawLine(blob_image_2, point_pair[0], point_pair[1], CV_RGB(255,0,0), 2, 8, 0)
        info_string = "w_%04d__h_%04d__rowranges_%02d.png"
        info = info_string % (blob_width, blob_height, len(acceptable_row_ranges))        
        cvSaveImage("/home/ryan/openCV/hp_blobs/"+info, blob_image_2)            
    return hp_point_pairs

def process_image(binary_image, min_char_width=20, min_char_height=27, max_width_b4_cutoff=80, max_height_b4_cutoff=120, max_blob_area=2800, min_sub_super_width = 21, min_sub_super_height = 14, max_sub_super_width_b4_cutoff = 66, max_sub_super_height_b4_cutoff = 38, miny_linetop_var=25, range_above_below_line=15, draw_lines=False, lines=[], left_margin=250, top_margin=80, num_lines_on_pecha=8):

    global num_blobs_found
## FIX LINE VAR VARAIBLE NAMES
    def find_corresponding_anchor(sup_or_sub,anchors,line_num):
        for anchor in anchors:
            if (sup_or_sub.minx >= anchor.minx) and (sup_or_sub.maxx <= anchor.maxx):
                anchor.sup = sup_or_sub
    bi_image  = binary_image
    image_size = cvGetSize(bi_image)
    image_width = bi_image.width
    image_height = bi_image.height
    gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
    mask = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvSet(mask,1)
    initial_blobs = CBlobResult(gray_image, mask, 100, False)
    initial_blob_count = initial_blobs.GetNumBlobs()
    print "initial_blob_count: ", initial_blob_count

##     if initial_blob_count == num_blobs_found:
##         can_rerun = False
##     else:
##         can_rerun = True
##     num_blobs_found = initial_blob_count        
        
    need_to_rerun = False
    vp_blobs = []
    hp_blobs = [] # Blobs spanning more than one topline

    if lines:
        for i in range(1,initial_blob_count): # if checking area, don't need to ignore 0
            blob = initial_blobs.GetBlob(i)
            width = int(blob.maxx-blob.minx)
            height = int(blob.maxy-blob.miny)
            blob_miny = int(blob.miny)
            blob_maxy = int(blob.maxy)            
            area = int(blob.area)
            acceptable_row_ranges = []
            if area < max_blob_area:
                if (height > max_height_b4_cutoff) and (width >= min_char_width):                
                    for line in lines:
                        if blob_miny <= line <= blob_maxy:
                            line_dist_from_miny = line-blob_miny
                            acceptable_row_ranges.append((line_dist_from_miny-range_above_below_line, line_dist_from_miny+range_above_below_line))
            if acceptable_row_ranges:
                hp_blobs.append((blob,acceptable_row_ranges))
    if hp_blobs:
        need_to_rerun = True
        for blob,acceptable_row_ranges in hp_blobs:
            hp_point_pairs = hp(blob,acceptable_row_ranges)
            for point_pair in hp_point_pairs:
                cvDrawLine(bi_image, point_pair[0], point_pair[1], CV_RGB(255,255,255), 2, 8, 0)

    for i in range(1,initial_blob_count): # if checking area, don't need to ignore 0
        blob = initial_blobs.GetBlob(i)
        width = int(blob.maxx-blob.minx)
        height = int(blob.maxy-blob.miny)
        area = int(blob.area)
        if area < max_blob_area:
            if (width > max_width_b4_cutoff) and (min_char_height <= height <= max_height_b4_cutoff):
##                suspected_num_chars = (width/max_width_b4_cutoff)+1
                vp_blobs.append(blob)

    if vp_blobs:
        need_to_rerun = True
        for blob in vp_blobs:
            vp_point_0, vp_point_1 = vp(blob, min_char_width)
            cvDrawLine(bi_image, vp_point_0, vp_point_1, CV_RGB(255,255,255), 2, 8, 0)
##                cvDrawLine(binary_image_2, point_pair[0], point_pair[1], CV_RGB(255,0,255), 1, 8, 0)

    if need_to_rerun:
        process_image(bi_image,lines=lines)
    else:
        if not lines:
## OUTPUT CHARACTER IMAGES
            from cum_sum import get_lines
            y1_array = []
            right_margin = image_width - left_margin
            bottom_margin = image_height - top_margin
            for i in range(1,initial_blob_count):
                blob = initial_blobs.GetBlob(i)
                minx = int(blob.minx)                
                maxx = int(blob.maxx)
                miny = int(blob.miny)
                maxy = int(blob.maxy)                
                width = maxx - minx
                height = maxy - miny
                if (min_char_width <= width <= max_width_b4_cutoff) and (min_char_height <= height <= max_height_b4_cutoff):
                    if (minx > left_margin) and (maxx < right_margin) and (miny > top_margin) and (maxy < bottom_margin):                
                        y1_array.append(miny)
            lines = get_lines(y1_array, bi_image, num_of_lines=num_lines_on_pecha)
            process_image(bi_image, lines=lines)
## IF WE GET HERE, WE HAVE FINISHED CHOPPING BLOBS
        else:
            print "FINISHED CHOPPING BLOBS"
            cvSaveImage("/home/ryan/openCV/bi_image.png", bi_image)
            output_dir = "/home/ryan/openCV/final_output/"
            char_string = "text_%02d__folio_%02d__line_%02d__char_%02d.png"
            pecha_line_empty_list_tuples = [(i+1,[]) for i in range(num_lines_on_pecha)]
            line_anchors = dict(pecha_line_empty_list_tuples)
            line_supers = dict(pecha_line_empty_list_tuples)
            line_subs = dict(pecha_line_empty_list_tuples)
            right_margin = image_width - left_margin
            bottom_margin = image_height - top_margin
            for i in range(1,initial_blob_count): # if checking area, don't need to ignore 0
                blob = initial_blobs.GetBlob(i)
                minx = int(blob.minx)                
                maxx = int(blob.maxx)
                miny = int(blob.miny)
                maxy = int(blob.maxy)                
                width = maxx - minx
                height = maxy - miny
                if (min_char_width <= width <= max_width_b4_cutoff) and (min_char_height <= height <= max_height_b4_cutoff):
                    if (minx > left_margin) and (maxx < right_margin) and (miny > top_margin) and (maxy < bottom_margin):                
## ANCHOR                        
                        for i, line_value in enumerate(lines):
                            if (miny <= line_value <= maxy): # or (miny-line_value <= miny_linetop_var):
                                line_anchors[i+1].append(blob)
                                break
## POTENTIAL SUB, SUPER, OR VOWEL
                    elif (min_sub_super_width <= width <= max_sub_super_width_b4_cutoff) and (min_sub_super_height <= height <= max_sub_super_height_b4_cutoff):
                        pass
                    else:
                        output_blob(blob)
## DRAW POLYGONS
            from cum_sum import draw_lines_2
            line_num__empty_list_tuples = [(k,[]) for k in line_anchors.keys()]
            d = dict(line_num__empty_list_tuples)
            right_margin = image_width - left_margin
            bottom_margin = image_height - top_margin
            for line_num, anchors in line_anchors.items():
                for i,blob in enumerate(sorted(anchors,key=operator.attrgetter('minx'))):
                    minx = int(blob.minx)
                    maxx = int(blob.maxx)
                    miny = int(blob.miny)
                    maxy = int(blob.maxy)                
                    width = maxx - minx
                    height = maxy - miny
                    if (min_char_width <= width <= max_width_b4_cutoff) and (min_char_height <= height <= max_height_b4_cutoff):
                        if (minx > left_margin) and (maxx < right_margin) and (miny > top_margin) and (maxy < bottom_margin):                
                            d[line_num].append((blob.minx, blob.miny))
                            d[line_num].append((blob.maxx, blob.miny))

            print "draw lines"
            draw_lines_2(d)
            print 'draw lines done'

## FINAL OUTPUT
            for line_num, anchors in line_anchors.items():
                for i,blob in enumerate(sorted(anchors,key=operator.attrgetter('minx'))):
                    if line_num == 7:
                        cvRectangle(bi_image,
                                cvPoint(int(blob.minx),int(blob.miny)),
                                cvPoint(int(blob.maxx),int(blob.maxy)),
                                CV_RGB(0,255,0), 1, 8, 0 
                                )            
                    char_image_name = char_string % (0,0,line_num,i)
                    blob_height = int(blob.maxy-blob.miny)
                    blob_width = int(blob.maxx-blob.minx)
                    blob_size = cvSize(blob_width,blob_height)
                    blob_image = cvCreateImage(blob_size, 8, 1)
                    cvZero(blob_image)
                    blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))
                    cvSaveImage(os.path.join(output_dir,char_image_name), blob_image)
                print "line %d completed" % line_num
                cvSaveImage(os.path.join(output_dir,"SEVEN.png"), bi_image)
    
if __name__ == "__main__":
#    f = open("/home/ryan/openCV/vars","a")
    input_image_path = "/home/ryan/ocr/test/input_image/2009_10_19/thresh48_BUM_BA_0010_01.png"
    binary_image = cvLoadImage(input_image_path)
#    print>>f, "\nDIR\n", dir(), "\nGLOBALS\n", globals(), "\nLOCALS\n", locals(), "\nTIME\n", datetime.datetime.now()    
    process_image(binary_image)
#    print>>f, "\nDIR\n", dir(), "\nGLOBALS\n", globals(), "\nLOCALS\n", locals(), "\nTIME\n", datetime.datetime.now()
#    f.close()
#    print>>f, "\nDIR\n", dir(), "\nGLOBALS\n", globals(), "\nLOCALS\n", locals(), "\nTIME\n", datetime.datetime.now()    
##     command_name = sys.argv[1]
##     if command_name=="output_images":
##         input_image_filename = sys.argv[2]
##         output_image_directory  = sys.argv[3]
##         output_images(input_image_filename, output_image_directory)
##     elif command_name=="draw_bounding_boxes":
##         input_image_filename = sys.argv[2]
##         output_image_filename  = sys.argv[3]
##         draw_bounding_boxes(input_image_filename, output_image_filename)        
##     elif command_name=="create_y1_histogram":
##         input_image_filename = sys.argv[2]
##         create_y1_histogram(input_image_filename)
##     elif command_name=="draw_top_of_lines":
##         input_image_filename = sys.argv[2]
##         output_image_filename  = sys.argv[3]
##         draw_top_of_lines(input_image_filename, output_image_filename)    

##     else:
##         print """
##         Options:
##         1. output_images [input_image_filename] [output_image_directory]
##         2. draw_bounding_boxes [input_image_filename] [output_image_filename]
##         3. create_y1_histogram [input_image_filename]
##         4. draw_top_of_lines [input_image_filename] [output_image_filename]

##         """
        
### Get the size of the contour
##size = abs(cvContourArea(contour))

### Is convex
##is_convex = cvCheckContourConvexity(contour)
##             cvRectangle(output_image,
##                     cvPoint(int(blob.minx),int(blob.miny)),
##                     cvPoint(int(blob.maxx),int(blob.maxy)),
##                     CV_RGB(0,255,0), 1, 8, 0 
##                     )
# #sorted(blobs_not_too_big_small,key=operator.attrgetter('area'))]

## USES PILL AND BOXES RATHER THAN BLOBS 
## def output_images(input_image_filename, output_image_directory):
##     global rect_dims
##     bi_image  = cvLoadImage(input_image_filename)
##     pill_image = Image.open(input_image_filename)
##     gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
##     cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
    
##     blobs = process_image(bi_image,gray_image)

##     for (img_num,blob) in enumerate(blobs):
##         if is_box_within_box(blob):
##             pass
##         else:
##             blob_width = blob.maxx-blob.minx
##             blob_height = blob.maxy-blob.miny
##             blob_size = (blob_width,blob_height)
##             blob_box = (blob.minx,blob.miny,blob.maxx,blob.maxy)
##             blob_region = pill_image.crop(blob_box)
##             character_image = Image.new("RGB",blob_size,color=None)
## ## im.paste(image, box) -- box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted image must match the size of the region.
##             character_image.paste(blob_region,box=None)
##             character_image.save(output_image_directory+'_'+str(img_num)+'.png')
##     print 'done'

## DRAW LINES VERSION 1 PIL
##             from cum_sum import draw_lines
##             y1_array = []
            
##             for i in range(1,initial_blob_count): # if checking area, don't need to ignore 0
##                 blob = initial_blobs.GetBlob(i)
##                 width = int(blob.maxx-blob.minx)
##                 height = int(blob.maxy-blob.miny)
##                 area = int(blob.area)
##                 if area < max_blob_area:
##                     if (min_char_width <= width <= max_width_b4_cutoff) and (min_char_height <= height <= max_height_b4_cutoff):
##                         y1_array.append(blob.miny)
##             print "len(y1_array): ",len(y1_array)
##             draw_lines(y1_array)
##             print 'done'

## def create_y1_histogram(input_image_filename):
##     from cum_sum import cum_sum
##     y1_array = []

##     global rect_dims
##     bi_image  = cvLoadImage(input_image_filename)
##     output_image = cvCloneImage(bi_image)
##     pill_image = Image.open(input_image_filename)
##     gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
##     cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
    
##     blobs = process_image(bi_image,gray_image)

##     for (img_num,blob) in enumerate(blobs):
##         if is_box_within_box(blob):
##             pass
##         else:
##             y1_array.append(blob.miny)
##     print "len(y1_array): ",len(y1_array)
##     cum_sum(y1_array)
##     print 'done'

## def draw_bounding_boxes(input_image_filename, output_image_filename):
##     global rect_dims
##     bi_image  = cvLoadImage(input_image_filename)
##     output_image = cvLoadImage(output_image_filename)
##     gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
##     cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
    
##     blobs = process_image(bi_image,gray_image)

##     for (img_num,blob) in enumerate(blobs):
##         if is_box_within_box(blob):
##             pass
## ##             blobs.pop(img_num)
## ##             print "len(blobs): ", len(blobs)
##         else:
##             cvRectangle(output_image,
##                     cvPoint(int(blob.minx),int(blob.miny)),
##                     cvPoint(int(blob.maxx),int(blob.maxy)),
##                     CV_RGB(0,255,0), 1, 8, 0 
##                     )            

##     cvSaveImage("/home/ryan/ocr/openCV/test/image/input.png", gray_image)
##     cvSaveImage("/home/ryan/ocr/openCV/test/image/output.png", output_image)
##     print 'done'
