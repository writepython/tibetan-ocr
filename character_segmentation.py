#!/usr/bin/python
import sys, os, operator, time, datetime

from math import sqrt
from PIL import Image

from opencv.cv import *
from opencv.highgui import *

from pyblobs.BlobResult import CBlobResult
from pyblobs.Blob import CBlob # Note: This must be imported in order to destroy blobs and use other methods

from config import *
from line_drawing import *

class FakeBlob:
    def __init__(self, minx=0, miny=0, maxx=0, maxy=0):
        self.minx = str(minx)
        self.miny = str(miny)
        self.maxx = str(maxx)
        self.maxy = str(maxy)    

## def output_blob(blob,output_dir="/home/ryan/openCV/b/"):
##     blob_height = int(blob.maxy-blob.miny)
##     blob_width = int(blob.maxx-blob.minx)
##     blob_size = cvSize(blob_width,blob_height)
##     blob_image = cvCreateImage(blob_size, 8, 1)
##     cvZero(blob_image)
##     blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(blob.minx), -1*int(blob.miny))
##     info_string = "w_%04d__h_%04d__miny_%04d.png"
##     info = info_string % (blob_width, blob_height, int(blob.miny))
##     cvSaveImage(output_dir+info, blob_image)

def distance_between_points(point1, point2):
    squared_distance1 = (point1[0]-point2[0])**2
    squared_distance2 = (point1[1]-point2[1])**2
    distance = sqrt(squared_distance1+squared_distance2)
    return distance

def get_blobs_sorted_by_distance_from_previous_blob(blobs, previous_blob):
    distance_blob_tuples = []
    for blob in blobs:
        try:
            distance_blob_tuples.append( (distance_between_points((int(blob.minx),int(blob.miny)), (int(previous_blob.maxx),int(previous_blob.miny))), blob) )
        except:
            print "type blob: %s, type previous: %s" % (type(blob), type(previous_blob))
    distance_blob_tuples.sort()
    return [tup[1] for tup in distance_blob_tuples]
    
## FIX LINE VAR VARAIBLE NAMES
def find_corresponding_anchor(sup_or_sub,anchors,line_num):
    for anchor in anchors:
        if (sup_or_sub.minx >= anchor.minx) and (sup_or_sub.maxx <= anchor.maxx):
            anchor.sup = sup_or_sub

def vp(blob, vp_dir, left_right_margin = 10, show_blobs=True):
    def get_col_miny_maxy(column):
        miny = 0
        maxy = 0
        for i,pixel_value in enumerate(column):
            if pixel_value == 255:
                maxy = i
                if not miny:
                    miny = i
        return miny,maxy
    print "NEW VP BLOB"
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
    num_cols_minus_margin = num_cols - left_right_margin

    for (i, col) in enumerate(blob_image.colrange()):
## TO SKIP PIXELS AT LEFT AND RIGHT MARGIN
        if (i+1 < min_char_width) or (i > num_cols_minus_margin):
            continue
        col_sum = cvSum(col)
        colsum_colnum_col_tuples.append((int(col_sum[0]),i,col))

    colsum_colnum_col_tuples.sort()

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
        cvSaveImage(os.path.join(vp_dir, info), blob_image_2)
##         info_string = "%04d__%04d__%s.png"
##         info = info_string % (blob_width, blob_height, str(datetime.datetime.now())) 
##         cvSaveImage(os.path.join(vp_dir, info, blob_image_2)
##    cvReleaseImage(blob_image)    
    return vp_point_pairs

def hp(blob, hp_dir, show_blobs=True):
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
    
##    for acceptable_row_range in acceptable_row_ranges:
    rowsum_rownum_row_tuples = []
    hp_rows = []

    for (i, row) in enumerate(blob_image.rowrange()):
##            if acceptable_row_range[0] <= i <= acceptable_row_range[1]:
        row_sum = cvSum(row)
        rowsum_rownum_row_tuples.append((int(row_sum[0]),i,row))
    rowsum_rownum_row_tuples.sort()
    lowest_rowsum_tuple = rowsum_rownum_row_tuples[0]
    new_hp_row = lowest_rowsum_tuple[1]
    delta_minx, delta_maxx = get_row_minx_maxx(lowest_rowsum_tuple[2])
    point1 = cvPoint(int(blob.minx)+delta_minx, int(blob.miny)+new_hp_row)
    point2 = cvPoint(int(blob.minx)+delta_maxx, int(blob.miny)+new_hp_row)
    hp_points = (point1, point2)
    if show_blobs:
##        for acceptable_row_range in acceptable_row_ranges:
        rowsum_rownum_row_tuples = []
        hp_rows = []
        
        for (i, row) in enumerate(blob_image.rowrange()):
        ##    if acceptable_row_range[0] <= i <= acceptable_row_range[1]:
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
        info_string = "w_%04d__h_%04d.png"
        info = info_string % (blob_width, blob_height)
        cvSaveImage(os.path.join(hp_dir, info), blob_image_2)            
    return hp_points

def get_blob_line(blob, y_values):
    diff_linenum_list = [ [abs(blob.min_y - y), i+1] for (i, y) in enumerate(y_values[1:]) ]
    return min(diff_linenum_list)[1]
    
def process_image(bi_image, folio_hp_directory, folio_vp_directory, folio_intermediate_directory, folio_characters_directory, folio_name, num_lines, previous_blob_count=0):

    image_size = cvGetSize(bi_image)
    image_width = bi_image.width
    image_height = bi_image.height
    gray_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvCvtColor(bi_image, gray_image, CV_BGR2GRAY)
    mask = cvCreateImage(cvGetSize(bi_image), 8, 1)
    cvSet(mask,1)
    initial_blobs = CBlobResult(gray_image, mask, 100, False)
    initial_blob_count = initial_blobs.GetNumBlobs()
    print "%s Initial Blob Count:  %s" % (folio_name, initial_blob_count)
    print "%s - Width %s - Height %s" % (folio_name, image_width, image_height)

    need_to_rerun = False
    need_to_find_first_character = True
    blob_list = [initial_blobs.GetBlob(i) for i in range(1,initial_blob_count)]
    blobs = []

    for blob in blob_list:
        width = int(blob.maxx) - int(blob.minx)
        height = int(blob.maxy) - int(blob.miny)
        blob_miny = int(blob.miny)
        blob_maxy = int(blob.maxy)

        blob.width = int(blob.maxx) - int(blob.minx)
        blob.height = int(blob.maxy) - int(blob.miny)
        blob.min_y = int(blob.miny)
        blob.max_y = int(blob.maxy)
        blob.min_x = int(blob.minx)
        blob.max_x = int(blob.maxx)        
        # area = int(blob.area)
        if max_width_b4_cutoff > width > min_char_width and max_height_b4_cutoff > height > min_char_height:
                blobs.append(blob)
        elif width > min_char_width and height > min_char_height:
            if width >= max_width_b4_cutoff:
                need_to_rerun = True
                vp_point_0, vp_point_1 = vp(blob, folio_vp_directory)
                cvDrawLine(bi_image, vp_point_0, vp_point_1, CV_RGB(255,255,255), 2, 8, 0)
            elif height >= max_height_b4_cutoff:
                need_to_rerun = True
                hp_point_0, hp_point_1 = hp(blob, folio_hp_directory)
                cvDrawLine(bi_image, hp_point_0, hp_point_1, CV_RGB(255,255,255), 2, 8, 0)
    if need_to_rerun and initial_blob_count - previous_blob_count > 1:
        process_image(bi_image, folio_hp_directory, folio_vp_directory, folio_intermediate_directory, folio_characters_directory, folio_name, num_lines, previous_blob_count=initial_blob_count)        
    else:
        print "FINISHED CHOPPING BLOBS for %s" % folio_name
        cvSaveImage(os.path.join(folio_intermediate_directory,"blobs_chopped.png"), bi_image)
        # create images needed for misc. drawings 
        line_drawing_image = cvCloneImage(bi_image)
        bounding_box_image = cvCloneImage(bi_image)
        black_square_image = cvCreateImage(cvGetSize(bi_image), 8, 1)
        cvRectangle(black_square_image, cvPoint(0,0), cvPoint(black_square_image.width, black_square_image.height), CV_RGB(255,255,255), CV_FILLED, 8, 0)
        line_drawing_from_black_squares_image = cvCloneImage(bi_image)
        curved_bottom_line_drawing_image = cvCloneImage(bi_image)        

        create_black_square_image(blobs, folio_intermediate_directory, black_square_image)        
        y_values = get_y_values_and_create_line_drawing(blobs, folio_intermediate_directory, line_drawing_image, num_lines)
        y_bottom_values = create_line_drawing_from_black_squares(line_drawing_from_black_squares_image, black_square_image, folio_intermediate_directory, y_values)
        create_curved_bottom_line_drawing_image(curved_bottom_line_drawing_image, folio_intermediate_directory, y_bottom_values)
        # y_values = get_y_values_and_create_multiline_drawing(blobs, folio_intermediate_directory, line_drawing_image, num_lines=8)        
        y_values.insert(0, 0)
        create_histogram(blobs, folio_intermediate_directory)
        create_bounding_box_image(blobs, folio_intermediate_directory, bounding_box_image)

        # character output
        char_string = "text_%02d__folio_%02d__line_%02d__char_%02d__miny_%04d.png"
        line_color_dict = {1:(45,106,19), 2:(255,0,255), 3:(0,255,255), 4:(255,0,0), 5:(0,0,255),
                           6:(0,255,0), 7:(213,111,56), 8:(50,5,150), 9:(205,5,0), 10:(56,70,105),
                           11:(222,35,5), 12:(25,250,14), 13:(40,40,45), 14:(50,55,60), 15:(23,11,156),
                           16:(240, 0, 240)
                           }
        
        blobs = sorted( blobs, key=operator.attrgetter('min_x') )
        line_counters = [1] * (num_lines+1)
        for blob in blobs:
            line = get_blob_line(blob, y_values)
            char_num = line_counters[line]
            line_counters[line] = line_counters[line] + 1

            char_image_name = char_string % (0, 0, line, char_num, blob.min_y)
            blob_height = blob.max_y - blob.min_y
            blob_width = blob.max_x - blob.min_x
            blob_size = cvSize(blob_width,blob_height)
            blob_image = cvCreateImage(blob_size, 8, 1)
            cvRectangle(blob_image, cvPoint(0,0), cvPoint(blob_image.width, blob_image.height), CV_RGB(255,255,255), CV_FILLED, 8, 0)
            blob.FillBlob(blob_image, CV_RGB(0,0,0), -1*blob.min_x, -1*blob.min_y)
            cvSaveImage(os.path.join(folio_characters_directory,char_image_name), blob_image)            
            cvRectangle(bi_image,
                        cvPoint(blob.min_x, blob.min_y),
                        cvPoint(blob.max_x, blob.max_y),
                        CV_RGB(*(line_color_dict[line])), 1, 8, 0 
                        )            
        cvSaveImage(os.path.join(folio_intermediate_directory, "FINISHED.png"), bi_image)
        print "line_counters: %s" % line_counters

    
if __name__ == "__main__":
    for folio_image_name in os.listdir(INPUT_IMAGE_DIR):
        try:
            folio_name = "%s_%s" % ( datetime.datetime.now().strftime("Y%Y_m%m_d%d_H%H_M%M_S%S"), folio_image_name.rsplit('.')[0] )
            base_folio_directory = os.path.join(OUTPUT_IMAGE_DIR, folio_name)
            folio_hp_directory = os.path.join(base_folio_directory, 'hp')
            folio_vp_directory = os.path.join(base_folio_directory, 'vp')
            folio_intermediate_directory = os.path.join(base_folio_directory, 'intermediate')
            folio_characters_directory = os.path.join(base_folio_directory, 'characters')            
            os.makedirs(base_folio_directory)
            os.makedirs(folio_hp_directory)
            os.makedirs(folio_vp_directory)
            os.makedirs(folio_intermediate_directory)
            os.makedirs(folio_characters_directory)                        
        except:
            print "Cannot make directories for image: %s" % folio_name
        binary_image = cvLoadImage(os.path.join(INPUT_IMAGE_DIR, folio_image_name))
        if binary_image:
            process_image(binary_image, folio_hp_directory, folio_vp_directory, folio_intermediate_directory, folio_characters_directory, folio_name, num_lines=8)
        else:
            print "Cannot load image: %s from directory: %s" % (folio_image_name, INPUT_IMAGE_DIR)
