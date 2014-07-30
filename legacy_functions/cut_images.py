import os, sys

from PIL import Image

def cut_images(input_dir, output_dir):
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir,item)
        if os.path.isdir(item_path):
            print "Could not cut. Reason: Is a Directory: ", item

        else:
            orig_image_name, orig_image_ext = os.path.splitext(item)
            pill_image = Image.open(os.path.join(item_path))
            w = pill_image.size[0]
            h = pill_image.size[1]        
        
            top_half_region = pill_image.crop((0,0,w,h/2))
            top_half_image = Image.new("RGB", top_half_region.size, color=None)
            top_half_image.paste(top_half_region)
            top_half_image.save(os.path.join(output_dir,orig_image_name+"_01"+orig_image_ext))
        
            bottom_half_region = pill_image.crop((0,h/2,w,h))
            bottom_half_image = Image.new("RGB", bottom_half_region.size, color=None)
            bottom_half_image.paste(bottom_half_region)            
            bottom_half_image.save(os.path.join(output_dir,orig_image_name+"_02"+orig_image_ext))

if __name__ == "__main__":
    abort = False    
    num_args = len(sys.argv)

    if num_args == 2:
        input_dir = output_dir = sys.argv[1]
    elif num_args == 3:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        abort = True

    if not abort:
        cut_images(input_dir, output_dir)
        print "\nImages placed in: ", output_dir, "\n"
    else:
        print "\nUsage: python cut_images.py input_dir [output_dir]\n"
