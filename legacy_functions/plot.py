from PIL import Image, ImageDraw

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

def plot_y(x,y):
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y)

    ax.set_xlabel('y value')
    ax.set_ylabel('cum_sum_count')
    ax.grid(True)

    fig.savefig('/home/ryan/ocr/openCV/test/image/y_value_hist_02.png')

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

def draw_lines(array,image):
    set_with_counts = get_counts(array)
    last_five = [0,0,0,0,0]
    cum_sum_with_y = []
    for (y,y_val_count) in set_with_counts:
        assert len(last_five) == 5
	new_sum = sum(last_five) + y_val_count
	cum_sum_with_y.append(new_sum,y)
	last_five.append(y_val_count)
	last_five.pop(0)
    cum_sum_with_y.sort()
    cum_sum_with_y.reverse()
    y1_vals = [y for (sum,y) in cum_sum_with_y[:16]]

    im = Image.open("lena.pgm")
    width = im.size[0]
    draw = ImageDraw.Draw(im)
    for y1 in y1_vals:
        line_dims = [0,y1,width,y1]
        draw.line(line_dims, fill="red")
    del draw 
    im.save("/home/ryan/ocr/openCV/test/image/image_with_lines.png", "PNG")
