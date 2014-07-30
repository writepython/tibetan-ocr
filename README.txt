=== About ===

A Python OCR program for handwritten Tibetan manuscripts like the ones recently digitized in Mongolia: http://www.tibet-dps.org/tempangma_kangyur.htm
The main script for doing character segmentation is character_segmentation.py.  This script contains a function process_image which is explained in detail below.

=== USAGE ===

1) Edit config.py
2) python character_segmentation.py

=== Dependencies ===

OpenCV - http://opencv.org/
cvBlobsLib - http://www.eng.auburn.edu/~troppel/internal/sparc/TourBot/TourBot%20References/cvdocuments/cvBlobsLib.html
NumPy - http://www.numpy.org/
matplotlib - http://matplotlib.org/

=== The Function process_image ===

This function processes each image again and again untill an acceptable result is obtained.  Acceptable means, for instance, no potential character images still exceed max height or width.

This process involves the following steps:

1) Find all the blobs of ink on the page using the class CBlobResult from cvBlobsLib.

2) Determine whether each blob needs to be passed to the vertical projection (vp) or horizontal projection (hp) functions.  Predefined variables like min_char_width, max_width_b4_cutoff, and max_height_b4_cutoff are taken into account.

3) Rerun process_image if some blobs were passed to vertical projection or horizontal projection functions.  (Vertical projection and horizontal projection functions result in alterations to the original image, by drawing one pixel width white lines.)

4) Determine the written order of blobs:

Start each iteration by calling the function get_blobs_sorted_by_distance_from_previous_blob, which gives you a list of blobs sorted by distance from previous blob.  The first blob is the one closest to (0, 0).  For each ensuing blob, we compare the distance between its Min X and Min Y and the Max X and Min Y of the previous blob. Distance between points is determined with the function distance_between_points, which takes the square root of the sum of the squares of the X and Y distances.

   Distance of a blob's Min X and Min Y from Max X and Min Y of the previously known character blob doesn't determine next character blob in 2 cases:

   A) At the end of a line, where the next character is far away.  Therefore we need to determine if we are at the end of line, and to do this we are currently checking to see if any blob remains on the same line.  So the code that attempts to do this is:

      if ( int(blob.maxx) > int(current_blob.minx) ) and ( abs(int(blob.miny)-int(current_blob.miny)) < 30 ):

   B) When we are not yet at the end of the line, but still the the closest blob in terms of distance from the Max X and Min Y of the previously known character is on the next line. So the code that attempts rule out blobs on other lines is:

      if ( int(blob.maxx) > int(previous_blob.minx) ) and ( abs(int(blob.miny)-int(previous_blob.miny)) < 30 )

5) Write each character blob as an image within the folio_characters_directory with the following as part of its filename: its line number, its character number in the line, and optionally, its dimensions.  Additionally, a bounding box is drawn around it on the original image.

6) Exit
