import cv2
from PIL import Image, ImageDraw, ImageFont #dynamic import
import PIL
import numpy as np

DIVIDER = 1
CONTRAST_MIN = 150
CONTRAST_MAX = 120

def center_crop(img, dim):
	"""Returns center cropped image
	Args:
	img: image to be center cropped
	dim: dimensions (width, height) to be cropped
	"""
	width, height = img.shape[1], img.shape[0]

	# process crop width and height for max available dimension
	crop_width = dim[0] if dim[0]<img.shape[1] else img.shape[1]
	crop_height = dim[1] if dim[1]<img.shape[0] else img.shape[0] 
	mid_x, mid_y = int(width/2), int(height/2)
	cw2, ch2 = int(crop_width/2), int(crop_height/2) 
	crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
	return crop_img


def resizeAndPad(img, size, padColor=0):

    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = abs((sh-new_h)/2)
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
        padColor = [padColor]*3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    #scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

    return scaled_img


import os
rootdir = 'vid'
            
extensions = ('.mp4')

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            print (os.path.join(subdir, file))

            video_file=os.path.join(subdir, file)

            vid = cv2.VideoCapture(video_file)
            success = True
            frame_cnt = 0
            
            while success:
                success, img = vid.read()
                if not success:
                    break
                
                img = resizeAndPad(img, (64, 128))
                img = center_crop(img, (128, 64))
                #img = img[::, (64 - np.floor(img.shape[2]/2)):- (128 - np.floor(img.shape[2]/2))]

                #img = cv2.resize(img, (128, 64), cv2.INTER_LANCZOS4)
                converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, converted_img = cv2.threshold(converted_img, CONTRAST_MIN, CONTRAST_MAX, cv2.THRESH_BINARY)
                print(converted_img.shape)
                #if frame_cnt % DIVIDER == 0:
                cv2.imwrite(video_file[:-(len(extensions))] + str(int(frame_cnt/2)) + ".png", converted_img, [cv2.IMWRITE_PNG_BILEVEL, 1])
                
                frame_cnt += 1
                #success = False
            #img.resize((128, 64), PIL.Image.LANCZOS)
            #img.save(video_file+".png",'png', optimize=True, quality=100)