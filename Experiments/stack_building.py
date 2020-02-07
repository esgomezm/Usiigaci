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
#import glob
#import sys
#sys.path.append("/home/esgomezm/miniconda3/envs/mask_rcnn/lib/python3.6/site-packages/")  # To find local version
PATH = '/home/esgomezm/Documents/DEEPLEARNING/data/'
#PATH2DATA = PATH + 'test_10x/input/_mask/'
PATH2DATA = PATH + 'test_10x/trained_network_10x/_mask/'
network = '_1'
PATH2OUT = PATH2DATA+network+'/RECONSTRUCTED_VIDEOS/'
os.mkdir(PATH2OUT)
#NEW_FOLDER_NAME = 'set'
input_names = 'video%03d'
input_names_time = 't%03d'

FILES = glob.glob(PATH2DATA+network+'/*.png')
FILES.sort()
current_video = -1
for file in FILES:
    print(file)
    frame = sitk.ReadImage(file)
    frame = sitk.GetArrayFromImage(frame)
    frame = frame.reshape((1,frame.shape[0], frame.shape[1]))
    file_name = file.split('/')[-1].split('.')[0]
    video = np.int(file_name.split('video')[-1].split('t')[0])
    t = np.int(file_name.split('video')[-1].split('t')[-1])
    if video != current_video:
        if current_video > -1:
            stack = sitk.GetImageFromArray(stack.astype(np.uint16))
            sitk.WriteImage(stack, PATH2OUT +input_names%video + '.tif')
        stack = frame
    else:
        stack = np.concatenate([stack,frame], axis=0)
    current_video = video
        