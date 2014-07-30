    def finish(blobs):
        need_to_find_first_character = True
        
        while blobs:
            if need_to_find_first_character: # First time around - point is (0,0)
                char_num = 0
                previous_blob = FakeBlob()
                need_to_find_first_character = False
                new_line = True

            blobs = get_blobs_sorted_by_distance_from_previous_blob(blobs, previous_blob)
            if len(blobs) == 1:
                current_blob = blobs.pop(0)
                last_iteration = True
            else:
                if not new_line:
                    for i, blob in enumerate(blobs):
                        if ( int(blob.maxx) > int(previous_blob.minx) ) and ( abs(int(blob.miny)-int(previous_blob.miny)) < 30 ):
                            try:
                                current_blob = blobs.pop(i)
                                break
                            except:
                                print "i: ", i
                else:
                    current_blob = blobs.pop(0)
                    new_line_miny = int(current_blob.miny)
            char_image_name = char_string % (0,0,line,char_num,int(current_blob.miny))
            blob_height = int(current_blob.maxy-current_blob.miny)
            blob_width = int(current_blob.maxx-current_blob.minx)
            blob_size = cvSize(blob_width,blob_height)
            blob_image = cvCreateImage(blob_size, 8, 1)
            cvZero(blob_image)
            blob.FillBlob(blob_image, CV_RGB(255,255,255), -1*int(current_blob.minx), -1*int(current_blob.miny))
            cvSaveImage(os.path.join(folio_characters_directory,char_image_name), blob_image)            
            cvRectangle(bi_image,
                        cvPoint(int(current_blob.minx),int(current_blob.miny)),
                        cvPoint(int(current_blob.maxx),int(current_blob.maxy)),
                        CV_RGB(*(line_color_dict[line])), 1, 8, 0 
                        )            
            cvSaveImage(os.path.join(folio_intermediate_directory,char_image_name), bi_image)
            if not last_iteration:
                blobs_for_checking_EOL = blobs[:]
                continue_on_same_line = False
                for blob in blobs_for_checking_EOL:
                    if ( int(blob.maxx) > int(current_blob.minx) ) and ( abs(int(blob.miny)-int(current_blob.miny)) < 30 ):                    
#                    if int(blob.maxx) > int(current_blob.minx) and int(blob.miny-35) <= int(current_blob.miny):
                        previous_blob = current_blob
                        char_num += 1
                        continue_on_same_line = True
                        new_line = False
                        break
                if not continue_on_same_line:
                    print "FINISHED Line %d of %s" % (line, folio_name)
                    line +=1
                    if line > num_lines:
                        print "Excessive number of lines (%d)for %s" % (line, folio_name)
                        break
                    char_num = 0
                    next_line_y_guess = new_line_miny+10
                    if next_line_y_guess < 0:
                        next_line_y_guess = 0
                    previous_blob = FakeBlob(miny=next_line_y_guess)
