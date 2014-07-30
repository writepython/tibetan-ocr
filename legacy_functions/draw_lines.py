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
