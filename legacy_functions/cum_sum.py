from PIL import Image, ImageDraw

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

from opencv.cv import *
from opencv.highgui import *

def plot_y(x,y):
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y)

    ax.set_xlabel('y value')
    ax.set_ylabel('cum_sum_count')
    ax.grid(True)

    fig.savefig('/home/ryan/ocr/openCV/test/image/y_value_hist_04.png')

def get_counts(array):
    y_vals_with_counts = [(y,array.count(y)) for y in array]
    y_vals_with_counts_distinct = set(y_vals_with_counts)
    y_vals_with_counts_distinct_list = list(y_vals_with_counts_distinct)
    y_vals_with_counts_distinct_list.sort()
    return y_vals_with_counts_distinct_list                          

def cum_sum(array):
    set_with_counts = get_counts(array)
    last_five = [0,0,0,0,0]
    cum_sum_x = []
    cum_sum_y = []
    for (y,y_val_count) in set_with_counts:
        assert len(last_five) == 5
	new_sum = sum(last_five)+y_val_count
	cum_sum_x.append(y)
	cum_sum_y.append(new_sum)
	last_five.append(y_val_count)
	last_five.pop(0)
##    cum_summed.sort()
##    cum_summed.reverse()
    plot_y(cum_sum_x,cum_sum_y)

def draw_lines_2(line_num_anchors_dict, input_image_path = "/home/ryan/ocr/test/input_image/2009_10_19/thresh48_BUM_BA_0010_01.png", min_dist_betw_lines=70, num_of_lines=8):
    im = Image.open(input_image_path)
    draw = ImageDraw.Draw(im)
    for line_num, anchors in line_num_anchors_dict.items():
        draw.line(anchors, fill=128)
    del draw 

    im.save("/home/ryan/ocr/test/input_image/2009_10_19/thresh48_BUM_BA_0010_01_poly.png")
    print "drawn"

def get_lines(array, bi_image, min_dist_betw_lines=70, num_of_lines=8):
    drawn_ys = []
    def should_draw_line(y1):
        for drawn_y in drawn_ys:
            if not abs(drawn_y-y1) > min_dist_betw_lines:
                return False
        return True
    
    set_with_counts = get_counts(array)
    last_five = [0,0,0,0,0]
    cum_sum_with_y = []
    for (y,y_val_count) in set_with_counts:
        assert len(last_five) == 5
	new_sum = sum(last_five)+y_val_count
	cum_sum_with_y.append((new_sum,y))
	last_five.append(y_val_count)
	last_five.pop(0)
    cum_sum_with_y.sort()
    cum_sum_with_y.reverse()

    width = int(bi_image.width)
    for (count,y1) in cum_sum_with_y:
        if len(drawn_ys) >= num_of_lines:
            break
        if should_draw_line(y1):
            point1 = cvPoint(0,y1-3)
            point2 = cvPoint(width,y1-3)                
            drawn_ys.append(y1)
    drawn_ys.sort()
    print "drawn_ys: ",drawn_ys
    return drawn_ys

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
