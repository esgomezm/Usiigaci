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
import sys



# To find local version
#import sys
#sys.path.append("/home/egomez/miniconda3/envs/mask_rcnn/lib/python3.6/site-packages/")

# path to the data directory which contains folders such as train, val or test
# PATH = "/home/egomez/Documents/data/"
PATH = sys.argv[1]

# subfolder in which the input and ground truth are
mode = 'train/'

# Old data
# name of the folder containing the input videos
# PATH2DATA = PATH + mode + "input_train/"
# PATH2DATA = PATH + mode + sys.argv[2]
PATH2DATA = os.path.join(PATH, sys.argv[2])

# name of the folder containing ground truth
# PATH2GT = PATH + mode + 'train_labels/'
# PATH2GT = PATH + mode + sys.argv[3]
PATH2GT = os.path.join(PATH, sys.argv[3])

# Ground truth's name has a different ending. Write it so as to get the correct
# name of the input file
#END = "_Segmentation2im_Prot"
# END = '_Segmentationim-label'
# END = sys.argv[4]

# New data
# directory in which new files should be saved
PATH2OUTPUT = PATH + mode + 'usiigaci/'
# name of the new folder
NEW_FOLDER_NAME = 'set'
# name of the new ground truth (specified by usiigaci)
masks_names = '/instance_ids.png'
# name of the new input slice (specified by Usiigaci)
input_names = '/raw.tif'


FILES = glob.glob(PATH2GT+'/*.tif')
COUNT = 1   
    
for file in FILES:
    # Load masks from segmented videos
    file_name = file
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
    
    for i in range(masks.shape[0]):
        # make a new directory called set
        if not os.path.exists(PATH2OUTPUT + NEW_FOLDER_NAME + np.str(COUNT)):
            os.makedirs(PATH2OUTPUT + NEW_FOLDER_NAME + np.str(COUNT))

        aux = masks[i]
        aux = aux.astype(np.uint8)
        number = np.str(i)
        sitk.WriteImage(sitk.GetImageFromArray(aux), PATH2OUTPUT + 
                        NEW_FOLDER_NAME + np.str(COUNT) + masks_names)
        
        aux = image[i]
        aux = aux.astype(np.uint16)
        number = np.str(i)
        sitk.WriteImage(sitk.GetImageFromArray(aux), PATH2OUTPUT + 
                        NEW_FOLDER_NAME + np.str(COUNT) + input_names)

        COUNT = COUNT + 1
        
        
        
        
  
