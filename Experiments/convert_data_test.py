#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:45:15 2019

@author: E. Gómez de Mariscal
GitHub username: esgomezm
"""

import numpy as np
import glob
import SimpleITK as sitk
import os

# To find local version
#import sys
#sys.path.append("/home/egomez/miniconda3/envs/mask_rcnn/lib/python3.6/site-packages/")

# path to the data directory which contains folders such as train, val or test
# PATH = "/home/egomez/Documents/data/"
PATH = sys.argv[1]
# subfolder in which the input and ground truth are
mode = 'test/'

# Old data

# name of the folder containing the input videos
PATH2DATA = os.path.join(PATH, sys.argv[2])

# name of the folder containing ground truth
PATH2GT = os.path.join(PATH, sys.argv[3])

# Ground truth's name has a different ending. Write it so as to get the correct
# name of the input file
# END = "_Segmentation2im_Prot"
# END = '_Segmentationim-label'
# END = sys.argv[4]

# New data
# directory in which new files should be saved
PATH2OUTPUT = PATH + mode + 'usiigaci/'
PATH2OUTPUT_MASK = PATH2OUTPUT + 'mask/'
PATH2OUTPUT_IINPUT = PATH2OUTPUT + 'input/'
# name of the new ground truth (specified by usiigaci)
masks_names = 'instances_ids%03d'
# name of the new input slice (specified by Usiigaci)
input_names = 'video%03d'
input_names_time = 't%03d'

if not os.path.exists(PATH2OUTPUT_IINPUT):
    os.makedirs(PATH2OUTPUT_IINPUT)
    
if not os.path.exists(PATH2OUTPUT_MASK):
    os.makedirs(PATH2OUTPUT_MASK)   
    
FILES = glob.glob(PATH2GT+'/*.tif')
COUNT_V = 0

for file in FILES:
    # Load masks from segmented videos
    file_name = file
    print(file_name)
    masks = sitk.ReadImage(file_name)
    masks = sitk.GetArrayFromImage(masks)
    
    # Load original images corresponding to masks.
    # file_name = file_name.split('/')[-1].split('.')[0]
    file_name = file_name.split('/')[-1]
    
    # Option 1 for the input names
    # time_range = file_name[:-len(END)].split('_')[-1]
    # image_name = file_name[:-(len(END+time_range))] + 'stackreg_'+time_range+'.tif'
    
    # Option 2 for the input names
    # image_name = file_name[:-(len(END))] + '.tif'

    # image = sitk.ReadImage(PATH2DATA +image_name)
    image = sitk.ReadImage(PATH2DATA +file_name)
    image = sitk.GetArrayFromImage(image)
    print(image_name)
    COUNT = 0
    for i in range(masks.shape[0]):
        aux = masks[i]
        aux = aux.astype(np.uint8)
        sitk.WriteImage(sitk.GetImageFromArray(aux), PATH2OUTPUT_MASK + masks_names%COUNT_V + input_names_time%COUNT + '.png')

        aux = image[i]
        aux = aux.astype(np.uint16)
        sitk.WriteImage(sitk.GetImageFromArray(aux), PATH2OUTPUT_IINPUT + input_names%COUNT_V + input_names_time%COUNT + '.tif')

        COUNT = COUNT + 1
        
    del(image)
    del(masks)
    COUNT_V = COUNT_V + 1
        
        
