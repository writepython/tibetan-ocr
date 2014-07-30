## Get the size of the contour
size = abs(cvContourArea(contour))

## Find out if is convex
is_convex = cvCheckContourConvexity(contour)

## Draw Rectangle
cvRectangle(output_image,
            cvPoint(int(blob.minx),int(blob.miny)),
            cvPoint(int(blob.maxx),int(blob.maxy)),
            CV_RGB(0,255,0), 1, 8, 0 
            )

## Sort by blob attribute
sorted(blobs_big_and_small,key=operator.attrgetter('area'))

## Save image
cvSaveImage("/home/ryan/ocr/openCV/test/image/input.png", gray_image)

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
