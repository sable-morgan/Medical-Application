
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 02:19:25 2017

@author: sharif
"""
# import the necessary packages
from skimage import measure as skmeas
from skimage import io as skio
from skimage import color as skcol
from skimage import filters as skfilt
from skimage import morphology as skmorph
#metrics
from sklearn.metrics import confusion_matrix
#from skimage import segmentation as skseg
import scipy.ndimage as ndi
# For plotting
import matplotlib.pyplot as plt
import numpy as np
#import argparse
# Folder listings and file path manipulation
import tkinter as tk
import tkinter.filedialog
#import glob
import os
import resultsPage
import imageProcessingUI
#size of image
CANVAS_SIZE = 512*512
#Scaling the pixel length using Assumption
TOTAL_AREA = 30
outfilename = ""

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

def detect_skull(image, fallback_width=70):
    #filt = ndi.gaussian_filter(gray, 7)
    # Determine the threshold value using the Otsu algorithm
    thresh = skfilt.threshold_otsu(image)

    print("The threshold is" + str(thresh))
    fg = image < thresh
    # Fill in any holes in the region
    fg_filled = ndi.binary_fill_holes(fg)
    # Basic skull esimate - a border within the region
    # of length fallback_width
    inner = ndi.distance_transform_edt(fg_filled) > fallback_width
    return fg_filled.astype('uint8') + inner.astype('uint8')
    
    # IN PROGRESS:
    # Try and detect the skull-brain chasm
    labels, Nlabels = ndi.label(fg)
    edge_labels = np.unique(labels[ fg_filled - ndi.binary_erosion(fg_filled) ])
    if len(edge_labels) == Nlabels:
        # No inner regions
        pass
    skull = fg.astype("uint8")
    for el in edge_labels:
        skull[labels==el] -= 1
    # If that was the whole set of labels,
    # try just a fixed width fall-back

    return skull


def detect_tumours(
        image, mask,
        min_size=50,
        max_size=150*150,
        max_maj_axis=300,
        ):
    
    # Blur the image for smoother outlines
    filt = skfilt.gaussian_filter(image, 5)
    
    # Automatically determine a threshold using Otsu algorithm
    # on just the skull region
    vals = filt[mask]
    thresh = skfilt.threshold_otsu(vals)
    
    # Determine a second threshold (single pass doesn't work well)
    vals = vals[vals>thresh]
    thresh2 = skfilt.threshold_otsu(vals)
    # Potential tumour regions are above the threshold and within the skull
    candidates = mask & (filt >= thresh2)
    
    # Remove small noise using binary_opening
    candidates = skmorph.binary_opening(candidates, selem=skmorph.disk(3))
    # Perform connected component labelling to get individual regions
    labels, num_labels = ndi.label(candidates, np.ones((3,3), dtype=bool))
    final = candidates.copy()
    

    # Use regionprops to determine additional properties
    for prop in skmeas.regionprops(labels, image):
        numPixels = prop.area
        numPixelsConvex = prop.convex_area
        
        print(115, numPixels, numPixelsConvex)
        tumorArea = (numPixelsConvex/CANVAS_SIZE) * TOTAL_AREA
        print('TumorArea is', tumorArea)
        if(tumorArea>.05):
            resultsPage.tumorDetected=1
        
        labelMask = labels== prop.label
        #------------------------------
        # Manual classifications
        #------------------------------
        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels <= min_size:
            final[labelMask] = 0
            continue
        if numPixelsConvex > max_size:
            final[labelMask] = 0
            continue
        if prop.major_axis_length > max_maj_axis:
            final[labelMask] = 0
            continue
    return final

def measure_accuracy(mask, mask_gt):
    # For binary regions (ROIs) A and B 
    # Precision is area overlap A with B / area of A
    # Recall is area overlap A with with B / area of B
    overlap = mask[mask_gt].sum()
    precision = overlap/(mask.sum())
    recall = overlap/(mask_gt.sum())

   # accuracy = confusion_matrix(mask, mask_gt)
    #print(accuracy)

    f_score = (precision + recall) / 2
    return {   
        "precision":precision, 
        "recall":recall, 
        "f-measure":f_score,
        }

def segmentTumourInFile(
        filename,
        ):
    # gt is ground truth
    # Load the data
    image, mask_gt = load_image(filename)
    
    # Determine the skull outline
    skull_mask = detect_skull(image)

    # Determine the tumours, using the image, and the skull outline
    # as skull_mask is 2 in the inner region of the skull (i.e. mainly
    # excluding the skull bone, we use skull_mask == 2 to select only
    # the inner region; this improves the detection
    mask = detect_tumours(image, skull_mask==2)

    # Determine the accyracy measurement
    stats = measure_accuracy(mask, mask_gt)
    imageProcessingUI.ImagePage.stats = stats
    print("Tumour detection complete, quality statistics:")
    for name, value in sorted(stats.items()):
        print(name, "=", value)

    # Finally, take the masks for ground truth, the skull,
    # and the detected tumours, and create an output segmentation result.
    results = plot_results(image, skull_mask, mask, filename)
    return results
def plot_results(image, skull_mask, mask,filename):
    #Basic matplotlib based plotting of the image and
    #contours around the masks
    fig = plt.figure(figsize=(5.12,5.12), dpi=100)
    ax = fig.add_subplot(111)
    print(image.shape)
#==============================================================================
#     for i in range(0,mask.shape[0]):
#         for j in range(0,mask.shape[1]):
#             if(mask_gt[i][j] == True):
#                 mask[i][j] = True
#==============================================================================
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
    #print(mask)
    # Add in the result
    plt.contour(mask, levels=[0.5], colors=['b'])
    

    # show the output image
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_position([0,0,1,1])
    
    print("Saving to :")
    outfilename = "{}_segmentation.png".format(os.path.splitext(filename)[0])
    
    if(resultsPage.tumorDetected==1):
        resultsPage.imageName = outfilename
    print(outfilename)
    fig.savefig(outfilename)
    plt.show(fig)
    plt.close(fig)
    mask_image = get_mask(image, skull_mask, mask, filename)
    return mask_image

def get_mask(image, skull_mask, mask,filename):
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
    #plt.contour(mask_gt, levels=[0.5], colors=['y'])

    # Add in the result
    #plt.contour(mask, levels=[0.5], colors=['b'])


    # show the output image
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_position([0,0,1,1])

    outfilename2 = "{}_predmask.png".format(os.path.splitext(filename)[0])
    fig.savefig(outfilename2)
    plt.show()
    plt.close(fig)
    return outfilename2
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

# For backend Testing! 
#==============================================================================
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
# # **For Developer use only**: Please uncomment main_single_file() (ln 304) or 
# # main_multi_file() (ln 305) in order to process files indivually 
# # or as a whole directory
# #==============================================================================
# if __name__ == '__main__':
#     #testing()
#     #main_single_file()
#     main_multi_file()
# 
#==============================================================================
