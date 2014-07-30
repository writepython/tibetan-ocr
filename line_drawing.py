import os
from PIL import Image, ImageDraw

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

from opencv.cv import *
from opencv.highgui import *

def create_line_drawing_from_black_squares(bi_image, black_squares_image, output_dir, y_values):
    filename = os.path.join(output_dir, "blob_line_drawing_from_black_squares_image.png")
    y_bottom_values = []
    
    for i, y_value1 in enumerate(y_values):
        if i+1 == len(y_values):
            break
        else:
            rowsum_rownum_tuples = []
            y_value2 = y_values[i+1]
            for (i, row) in enumerate( black_squares_image.rowrange() ):
                if y_value1 < i < y_value2:
                    row_sum = cvSum(row)
                    rowsum_rownum_tuples.append( (int(row_sum[0]), i) )        
            rowsum_rownum_tuples.sort()
            rowsum_rownum_tuples.reverse()
            row_with_most_whitespace = rowsum_rownum_tuples[0][1]
            point1 = cvPoint(0, row_with_most_whitespace)
            point2 = cvPoint(bi_image.width, row_with_most_whitespace)
            cvDrawLine(bi_image, point1, point2, CV_RGB(255,0,0), 1, 8, 0)
            y_bottom_values.append(row_with_most_whitespace)

    cvSaveImage(filename, bi_image)
    y_bottom_values.sort()
    return y_bottom_values

def random_color(random):
    """
    Return a random color
    """
    icolor = random.randint(0, 0xFFFFFF)
    return cvScalar(icolor & 0xff, (icolor >> 8) & 0xff, (icolor >> 16) & 0xff)

def create_curved_bottom_line_drawing_image(bi_image, output_dir, y_bottom_values):
    import random
    filename = os.path.join(output_dir, "blob_curved_bottom_line_drawing.png")
    white_scalar = repr(cvScalar(255, 255, 255, 0))    
    lines_to_draw = []

    for y_bottom_value in y_bottom_values:
        previous_successful_y_value = int(y_bottom_value)
        previous_tried_y_value_init = int(y_bottom_value)        
        previous_tried_y_value_neg = int(y_bottom_value)
        previous_tried_y_value_pos = int(y_bottom_value)                
        point_of_equilibrium = int(y_bottom_value)
        line_to_draw = []

        for x in range(bi_image.width):
            previous_tried_y_value_init = previous_successful_y_value
            previous_tried_y_value_neg = previous_successful_y_value
            previous_tried_y_value_pos = previous_successful_y_value                                     
            not_determined_point = True
            if previous_tried_y_value_init == point_of_equilibrium:
                hit_equilibrium = True            
            else:
                hit_equilibrium = False
            while not_determined_point:
                if hit_equilibrium:
                    previous_tried_y_value_neg = previous_tried_y_value_neg - 1
                    previous_tried_y_value_pos = previous_tried_y_value_pos + 1                    
                    y1 = previous_tried_y_value_neg
                    y2 = previous_tried_y_value_pos
                    if y1 >= 0:
                        #print x, y1
                        point1 =  repr(bi_image[y1][x])
                        if point1 == white_scalar:
                            bi_image[y1][x] = CV_RGB(255,0,0)
                            line_to_draw.append( (x, y1) )
                            not_determined_point = False
                            continue
                    if y2 >= 0:
                        point2 = repr(bi_image[y2][x])                    
                        if point2 == white_scalar:
                            bi_image[y2][x] = CV_RGB(255,0,0)
                            line_to_draw.append( (x, y2) )
                            not_determined_point = False
                            continue
                    continue
                else:
                    if previous_tried_y_value_init > point_of_equilibrium:
                        previous_tried_y_value_init = previous_tried_y_value_init - 1
                    else:
                        previous_tried_y_value_init = previous_tried_y_value_init + 1                        
                    if previous_tried_y_value_init == point_of_equilibrium:
                        hit_equilibrium = True
                    y = previous_tried_y_value_init
                    point = repr(bi_image[y][x])                    
                    if point == white_scalar:
                        bi_image[y][x] = CV_RGB(255,0,0)
                        line_to_draw.append( (x, y) )
                        not_determined_point = False
                        continue
                    else:
                        continue
    #cvPolyLine(bi_image, lines_to_draw, 0, 0, 1, CV_RGB(255,0,0), 1, 8, 0)
    cvSaveImage(filename, bi_image)

def create_text_image(blobs, output_dir, bi_image):
    line_type = CV_AA
    filename = os.path.join(output_dir, "blob_text_image.png")
    #font = cvInitFont(CV_FONT_VECTOR0, 0.4, 0.4, 0.0, 2, line_type)
    font = cvInitFont(CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 2, line_type)

    for blob in blobs:
        middle_point = cvPoint(blob.min_x + (blob.max_x-blob.min_x), blob.min_y + (blob.max_y-blob.min_y) )
        cvPutText(bi_image, "pa", cvPoint(blob.min_x, blob.min_y), font, CV_RGB(0,0,0) )    
    cvSaveImage(filename, bi_image)

def create_black_square_image(blobs, output_dir, bi_image):
    filename = os.path.join(output_dir, "blob_black_squares.png")
    for blob in blobs:
        cvRectangle(bi_image, cvPoint(blob.min_x, blob.min_y), cvPoint(blob.max_x, blob.max_y),
                    CV_RGB(0,0,0), CV_FILLED, 8, 0)
    cvSaveImage(filename, bi_image)    
    
def create_bounding_box_image(blobs, output_dir, bi_image):
    filename = os.path.join(output_dir, "blob_bounding_boxes.png")    
    for blob in blobs:
        cvRectangle(bi_image, cvPoint(blob.min_x, blob.min_y), cvPoint(blob.max_x, blob.max_y),
                    CV_RGB(0,255,0), 1, 8, 0)
    cvSaveImage(filename, bi_image)
    
def create_histogram(blobs, output_dir):
    y_array = []
    for blob in blobs:
        y_array.extend([blob.min_y] * blob.width)
    set_with_counts = get_counts(y_array)
    last_five = [0,0,0,0,0]
    cum_sum_x = []
    cum_sum_y = []
    for (y, y_val_count) in set_with_counts:
        assert len(last_five) == 5
	new_sum = sum(last_five) + y_val_count
	cum_sum_x.append(y)
	cum_sum_y.append(new_sum)
	last_five.append(y_val_count)
	last_five.pop(0)

    plot_y(cum_sum_x, cum_sum_y, output_dir)    

def get_y_values_and_create_multiline_drawing(blobs, output_dir, bi_image, num_lines=8, min_dist_betw_lines=50):
    def should_draw_line(y1):
        for drawn_y in drawn_ys:
            if not abs(drawn_y-y1) > min_dist_betw_lines:
                return False
        return True    
    filename = os.path.join(output_dir, "blob_line_drawing.png")
    drawn_points = []

    image_section_width_ranges = [[0, bi_image.width/3], [(bi_image.width/3)+1, (bi_image.width/3)*2], [((bi_image.width/3)*2)+1, bi_image.width]]
    for image_section_width_range in image_section_width_ranges:
        drawn_ys = []
        y_array = []
        last_five = [0,0,0,0,0]
        cumsum_y_tuples = []
        
        for blob in blobs:
            if blob.min_x >= image_section_width_range[0] and blob.max_x <= image_section_width_range[1]:
                y_array.extend([blob.min_y] * blob.width)

        set_with_counts = get_counts(y_array)
    
        for (y, y_val_count) in set_with_counts:
            assert len(last_five) == 5
            new_sum = sum(last_five) + y_val_count
            cumsum_y_tuples.append( (new_sum, y) )
            last_five.append(y_val_count)
            last_five.pop(0)
        cumsum_y_tuples.sort()
        cumsum_y_tuples.reverse()

        width = image_section_width_range[1] - image_section_width_range[0]

        for (count, y1) in cumsum_y_tuples:
            if len(drawn_ys) >= num_lines:
                break
            if should_draw_line(y1):
                point1 = cvPoint(image_section_width_range[0], y1-3)
                point2 = cvPoint(image_section_width_range[1], y1-3)
                cvDrawLine(bi_image, point1, point2, CV_RGB(255,0,0), 1, 8, 0)
                drawn_ys.append(y1)
                drawn_points.append((point1, point2))
        drawn_ys.sort()
        print "drawn_ys: ", drawn_ys        
    cvSaveImage(filename, bi_image)    
    drawn_points.sort()
    print "drawn_points: ", drawn_points
    return drawn_points

def get_y_values_and_create_line_drawing(blobs, output_dir, bi_image, num_lines=8, min_dist_betw_lines=30):
    def should_draw_line(y1):
        for drawn_y in drawn_ys:
            if not abs(drawn_y-y1) > min_dist_betw_lines:
                return False
        return True    
    filename = os.path.join(output_dir, "blob_line_drawing.png")
    drawn_ys = []
    y_array = []
    last_five = [0,0,0,0,0]
    cumsum_y_tuples = []
    
    for blob in blobs:
        y_array.extend([blob.min_y] * blob.width)

    set_with_counts = get_counts(y_array)
    
    for (y, y_val_count) in set_with_counts:
        assert len(last_five) == 5
	new_sum = sum(last_five) + y_val_count
	cumsum_y_tuples.append( (new_sum, y) )
	last_five.append(y_val_count)
	last_five.pop(0)
    cumsum_y_tuples.sort()
    cumsum_y_tuples.reverse()

    width = int(bi_image.width)
    for (count, y1) in cumsum_y_tuples:
        if len(drawn_ys) >= num_lines:
            break
        if should_draw_line(y1):
            point1 = cvPoint(0,y1-3)
            point2 = cvPoint(width,y1-3)
            cvDrawLine(bi_image, point1, point2, CV_RGB(255,0,0), 1, 8, 0)            
            drawn_ys.append(y1)
    cvSaveImage(filename, bi_image)    
    drawn_ys.sort()
    print "drawn_ys: ", drawn_ys
    return drawn_ys
    
def plot_y(x, y, output_dir):
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y)

    ax.set_xlabel('y value')
    ax.set_ylabel('cum_sum_count')
    ax.grid(True)
    
    filename = os.path.join(output_dir, "blob_histogram.png")
    fig.savefig(filename)

def get_counts(y_array):
    y_vals_with_counts = [(y, y_array.count(y)) for y in y_array]
    y_vals_with_counts_distinct = set(y_vals_with_counts)
    y_vals_with_counts_distinct_list = list(y_vals_with_counts_distinct)
    y_vals_with_counts_distinct_list.sort()
    return y_vals_with_counts_distinct_list                          

## def get_lines(array, bi_image, min_dist_betw_lines=70, num_of_lines=8):
##     drawn_ys = []
##     def should_draw_line(y1):
##         for drawn_y in drawn_ys:
##             if not abs(drawn_y-y1) > min_dist_betw_lines:
##                 return False
##         return True
    
##     set_with_counts = get_counts(array)
##     last_five = [0,0,0,0,0]
##     cum_sum_with_y = []
##     for (y,y_val_count) in set_with_counts:
##         assert len(last_five) == 5
## 	new_sum = sum(last_five)+y_val_count
## 	cum_sum_with_y.append((new_sum,y))
## 	last_five.append(y_val_count)
## 	last_five.pop(0)
##     cum_sum_with_y.sort()
##     cum_sum_with_y.reverse()

##     width = int(bi_image.width)
##     for (count,y1) in cum_sum_with_y:
##         if len(drawn_ys) >= num_of_lines:
##             break
##         if should_draw_line(y1):
##             point1 = cvPoint(0,y1-3)
##             point2 = cvPoint(width,y1-3)                
##             drawn_ys.append(y1)
##     drawn_ys.sort()
##     print "drawn_ys: ",drawn_ys
##     return drawn_ys

##     lines_dict = dict([(i+1,y) for i,y in enumerate(drawn_ys)])
##     print "lines_dict: ", lines_dict
##     return lines_dict


## def draw_lines(array, path_to_image_to_draw_on="/home/ryan/ocr/test/image/test_raw.png", min_dist_betw_lines=70):
##     drawn_ys = []
##     def should_draw_line(y1):
##         for drawn_y in drawn_ys:
##             if not abs(drawn_y-y1) > min_dist_betw_lines:
##                 return False
##         return True
    
##     set_with_counts = get_counts(array)
##     last_five = [0,0,0,0,0]
##     cum_sum_with_y = []
##     for (y,y_val_count) in set_with_counts:
##         assert len(last_five) == 5
## 	new_sum = sum(last_five)+y_val_count
## 	cum_sum_with_y.append((new_sum,y))
## 	last_five.append(y_val_count)
## 	last_five.pop(0)
##     cum_sum_with_y.sort()
##     cum_sum_with_y.reverse()

##     im = Image.open(path_to_image_to_draw_on)
##     width = im.size[0]
##     draw = ImageDraw.Draw(im)    
##     for (count,y1) in cum_sum_with_y:
##         if len(drawn_ys) == 16:
##             break
##         if should_draw_line(y1):
##             line_dims = [0,y1-3,width,y1-3]
##             draw.line(line_dims, fill="red")
##             drawn_ys.append(y1)
##     del draw 
##     im.save("/home/ryan/ocr/test/output_image/image_with_lines_raw.png", "PNG")
##     print "drawn_ys: ",drawn_ys

## def draw_lines_2(array, bi_image, min_dist_betw_lines=70, num_of_lines=8):
##     drawn_ys = []
##     def should_draw_line(y1):
##         for drawn_y in drawn_ys:
##             if not abs(drawn_y-y1) > min_dist_betw_lines:
##                 return False
##         return True
    
##     set_with_counts = get_counts(array)
##     last_five = [0,0,0,0,0]
##     cum_sum_with_y = []
##     for (y,y_val_count) in set_with_counts:
##         assert len(last_five) == 5
## 	new_sum = sum(last_five)+y_val_count
## 	cum_sum_with_y.append((new_sum,y))
## 	last_five.append(y_val_count)
## 	last_five.pop(0)
##     cum_sum_with_y.sort()
##     cum_sum_with_y.reverse()

##     width = int(bi_image.width)
##     for (count,y1) in cum_sum_with_y:
##         if len(drawn_ys) == num_of_lines:
##             break
##         if should_draw_line(y1):
##             point1 = cvPoint(0,y1-3)
##             point2 = cvPoint(width,y1-3)                
##             cvDrawLine(bi_image, point1, point2, CV_RGB(255,0,0), 1, 8, 0)
##             drawn_ys.append(y1)
##     cvSaveImage("/home/ryan/ocr/test/output_image/vp_lines_boxes.png", bi_image)
##     print "drawn_ys: ",drawn_ys
