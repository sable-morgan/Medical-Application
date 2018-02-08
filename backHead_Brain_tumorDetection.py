# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 02:19:25 2017

@author: sharif
"""
# import the necessary packages
from skimage import measure as skmeas
from skimage import io as skio
from skimage import color as skcol
#from skimage import filters as skfilt
#from skimage import morphology as skmorph
#from skimage import segmentation as skseg
import scipy.ndimage as ndi
# For plotting
import matplotlib.pyplot as plt
import numpy as np
#import argparse
# Folder listings and file path manipulation
import tkinter
import tkinter.filedialog
import glob
import os
import cv2
import imageProcessingUI

#import resultsPage


#size of image
CANVAS_SIZE = 512*512
#Scaling the pixel length using Assumption
TOTAL_AREA = 30
outfilename = ""
#Intructions

#==============================================================================
# To connect with main application uncomment lines 25, 130,131, 225-227
# And comment out line 37-40(except line 39), 240-252
# To disconnect from the main application and run file on its own, do the exact
# opposite
#==============================================================================

def process_files(files):
    result = segmentTumourInFile(files)
    return result
# For Backend testing to process files!
#==============================================================================
#     Nfiles = len(files)
#     print("Processing %d files..."%Nfiles)
#     for n, filename in enumerate(files):
#         segmentTumourInFile(filename)
#         print("Done: {:>6}/{:d}".format(n+1, Nfiles), end="\r")
#==============================================================================


def load_image(filename):

     # Load the ground truth mask
     maskfile = os.path.join(
         os.path.dirname(filename),
         "%s_mask%s"%(
             os.path.basename(filename).split("_")[0],
             os.path.splitext(filename)[1],
         ),
     )

     # If the ground truth mask doesn't exist, raise an error
     if not os.path.isfile(maskfile):
        raise Exception("Mask file missing\nfilename:%s\nmaskfile:%s"%(filename, maskfile))
     # Load the image file into an array
     image = skio.imread(filename)
     # Convert it to grayscale (it's loaded as RGB)
     gray = skcol.rgb2gray(image)
     # Load the mask (and convert it to boolean)
     mask_gt = skio.imread(maskfile) > 0
     return gray, mask_gt


def measure_accuracy(mask, mask_gt):
    # For binary regions (ROIs) A and B
    # Precision is area overlap A with B / area of A
    # Recall is area overlap A with with B / area of B
    overlap = mask[mask_gt].sum()
    precision = overlap/(mask.sum())
    recall = overlap/(mask_gt.sum())
    f_score = (precision + recall) / 2
    return {
        "precision":precision,
        "recall":recall,
        "f-measure":f_score,
        }


def plot_results(image, skull_mask, mask, mask_gt,filename):
    #Basic matplotlib based plotting of the image and
    #contours around the masks
    fig = plt.figure(figsize=(5.12,5.12), dpi=100)
    ax = fig.add_subplot(111)
    plt.imshow(image, cmap='gray')

    #find the biggest area
    # To get the overall bounding box, just get min and max x & y coords
    y,x = mask.nonzero()
    if len(x) > 0:
        x0 = x.min()
        y0 = y.min()
        width = x.max()-x0
        height = y.max()-y0
        ax.add_artist(plt.Rectangle((x0, y0), width, height, facecolor="none", edgecolor="g"))

    # Add in the GT
    #plt.contour(mask_gt, levels=[0.5], colors=['y'])

    # Add in the result
    plt.contour(mask, levels=[0.5], colors=['b'])


    # show the output image
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_position([0,0,1,1])

    outfilename = "{}_segmentation.png".format(os.path.splitext(filename)[0])
    fig.savefig(outfilename)
    plt.show()
    plt.close(fig)
    maskfilename = get_mask(image, skull_mask, mask, mask_gt,filename)
    return maskfilename
def get_mask(image, skull_mask, mask, mask_gt,filename):
    #Basic matplotlib based plotting of the image and
    #contours around the masks
    fig = plt.figure(figsize=(5.12,5.12), dpi=100)
    ax = fig.add_subplot(111)
    plt.imshow(mask, cmap='gray')

    #find the biggest area
    # To get the overall bounding box, just get min and max x & y coords
    y,x = mask.nonzero()
#==============================================================================
#     if len(x) > 0:
#         x0 = x.min()
#         y0 = y.min()
#         width = x.max()-x0
#         height = y.max()-y0
#         ax.add_artist(plt.Rectangle((x0, y0), width, height, facecolor="none", edgecolor="g"))
#==============================================================================

    # Add in the GT
    plt.contour(mask_gt, levels=[0.5], colors=['y'])

    # Add in the result
    plt.contour(mask, levels=[0.5], colors=['b'])


    # show the output image
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_position([0,0,1,1])

    outfilename2 = "{}_predmask.png".format(os.path.splitext(filename)[0])
    fig.savefig(outfilename2)
    plt.show()
    plt.close(fig)
    return outfilename2
def binaryImg(filteredIm):
    
    #This is simply a threshold by half of the maximum value.
    
    max_value = np.max(filteredIm)
    normimg = np.round(filteredIm / max_value)
    newnormimg = np.where(normimg == 1, 0, 255)
    Ithres = cv2.convertScaleAbs(newnormimg)
    return Ithres

def get_skull(image):
    """
    After some binary operations on the initial mask
    this then sets the image data to zero at the locations
    of the biggest and second biggest regions...
    """
    # Generate a 3x3 cross shaped structuring element
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # Perform median filtering
    filtered_image=cv2.medianBlur(image,3)
    # Threshold above 50% of max to true
    mask = binaryImg(filtered_image)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.erode(mask, kernel, iterations=6)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # RETURN BIGGEST CONTOUR STARTS HERE
    im, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    maxContour = 0
    temp = np.zeros(np.size(contours))
    for i, contour in enumerate(contours):
        contourSize = cv2.contourArea(contour)
        temp[i] = contourSize
        if contourSize > maxContour:
            maxContour = contourSize
            # the following is not used
            #maxContourData = contour
    # sort the countour areas
    index = np.argsort(temp)
    final_mask = np.zeros(mask.shape, dtype='uint8')
    cv2.drawContours(final_mask, contours, index[-2], (255, 255, 255), cv2.FILLED)
    cv2.drawContours(final_mask, contours, index[-3], (255, 255, 255), cv2.FILLED)
    return final_mask > 0


def detect_tumours(image, skull_mask):
    skullremoved = ~skull_mask * image
    # Perform a second roung of 50% of max thresholding
    mask = binaryImg(skullremoved)    #again binary image generation
    # Generate a cross-shaped structuring element
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    # Perform closing
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Perform opening
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # Erode the mask
    mask = cv2.erode(mask, kernel, iterations=1)
    # Dilate the mask (this after eroding is the same as "opening"...
    mask = cv2.dilate(mask, kernel, iterations=1)
    # Select the 2nd largest region... (instead of the following)
    regions, num_regions = ndi.label(~mask)
    all_sizes = [p.area for p in skmeas.regionprops(regions)]
    index = np.argsort(all_sizes)
    # Select the 2nd largest
    mask = regions == (index[-1]+1)
    return mask
    """
    # Find contours ala opencv
    im, contours, hierarchy = cv2.findContours(mask,
        cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    maxContour = 0
    all_sizes = np.zeros(np.size(contours))
    for i, contour in enumerate(contours):
        contourSize = cv2.contourArea(contour)
        all_sizes[i] = contourSize
        if contourSize > maxContour:
            maxContour = contourSize
            maxContourData = contour
    # sort the countour areas
    index = np.argsort(all_sizes)
    # Select the 2nd largest contour
    [x, y, w, h] = cv2.boundingRect(contours[index[-2]])
    image_with_box = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return mask
    """

def segmentTumourInFile(filename):
    print("\nProcessing:", filename)
    # Load the dataset
    image, mask_gt = load_image(filename)

    # Perform "skull" removal, which modifies the image data...
    skull_mask = get_skull(image)

    tumour_mask = detect_tumours(image, skull_mask)

    # Determine the accuracy
    stats = measure_accuracy(tumour_mask, mask_gt)
    imageProcessingUI.ImagePage.stats = stats
    print("Tumour detection complete, quality statistics:")
    for name, value in sorted(stats.items()):
        print(name, "=", value)

    results = plot_results(image, skull_mask, tumour_mask, mask_gt, filename,
    )
    print(results)
    return results
##=========================================================
## Folder/File retrieving using a GUI
##=========================================================

#GUI folder getting
def get_folder_gui():
    
    root = tkinter.Tk()
    root.withdraw()
    foldername = tkinter.filedialog.askdirectory(
        initialdir='.',
        title='Please select a folder containing the data',
    )
    root.update()
    return foldername

#GUI filename getting
def get_filename_gui():
  
    root = tkinter.Tk()
    root.withdraw()
    filename = tkinter.filedialog.askopenfile(
        initialdir='.',
        title='Please select a file to process',
    )
    root.update()
    return filename.name

#For backend testing! 
#==============================================================================
# ##=========================================================
# ## Main Functions
# ##=========================================================
# 
# #Main Function to get multi_file from directory
# def main_multi_file():
# 
#     folder = get_folder_gui()
#     print(folder)
#     pattern = "*image.png"
#     files = sorted(glob.glob(os.path.join(folder, pattern)))
#     process_files(files)
# 
# 
# #Main Function to get single file from any directory
# def main_single_file():
# 
#     filename = get_filename_gui()
#     process_files([filename,])
# 
# #==============================================================================
# # def testing():
# #     files=[ "data/331_image.png", ]
# #     process_files_new(files)
# #==============================================================================
# #==============================================================================
# # **For Developer use only**: Please uncomment main_single_file() (line ..) or 
# # main_multi_file() (line ...) in order to process files indivually 
# # or as a whole directory
# #==============================================================================
# if __name__ == '__main__':
#     #testing()
#     main_single_file()
#     #main_multi_file()
#==============================================================================
