#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 2 09:19:25 2017

@author: sharif
"""
import os
import argparse
import glob
import tables
import traceback
import numpy as np
import scipy.misc as scmisc
import tkinter.filedialog

#Function to select directory through UI
def get_folder_gui():
    
    root = tkinter.Tk()
    root.withdraw()
    foldername = tkinter.filedialog.askdirectory(
        initialdir='.',
        title='Please select a folder containing the data',
    )
    root.update()
    return foldername

#argument parser 
def create_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument("folder", nargs="?", help="Optionally supply the folder on the command line")
    parser.add_argument("-e", "--extension", help="Image format to save to", choices=["jpg", "png", "tif"], default="png")
    return parser

#Searh directory for .mat files, then 
#convert using convert_matfile function
def run_folder(folder, extension="png"):
   
    matfiles = sorted(glob.glob(os.path.join(folder, "*.mat")))
    for matfile in matfiles:
        print("Converting {} to PNG...".format(matfile), end="", flush=True)
        try:
            convert_matfile(matfile, extension=extension)
            print("DONE")
        except:
            print("FAILED\n%s"%traceback.format_exc())

#Convert .mat files to .jpg images
def convert_matfile(matfile, extension="png"):
    
    matobj = loadmat(matfile)
    im = np.array(matobj.root.cjdata.image)
    mask = 255*np.array(matobj.root.cjdata.tumorMask)
    matobj.close()

    savebase = os.path.splitext(matfile)[0]
    scmisc.imsave("{}_image.{}".format(savebase, extension), im)
    scmisc.imsave("{}_mask.{}".format(savebase, extension), mask) 

def loadmat(matfile):
     #try:
     #    matobj = scio.loadmat(matfile)
     #    print(matobj)
     #except:
     #    #with h5py.File(matfile, 'r') as f:
     #    #    print(f.keys())
     #    #fobj = tables.openFile(matfile)
     fobj = tables.open_file(matfile)
     return fobj

#Main function 
def main():

    parser = create_parser()
    args = parser.parse_args()
   
    foldername = get_folder_gui()
    run_folder(foldername, extension=args.extension)

#This allows the main function to excute first
main()