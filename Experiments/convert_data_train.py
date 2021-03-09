"""
Created on Wed Jul 17 10:45:15 2019

@author: E. Gómez de Mariscal
GitHub username: esgomezm
"""
import numpy as np
from PIL import Image 
import os
import sys
# path to the data directory which contains folders such as train, val or test
PATH = sys.argv[1]
# subfolder in which the input and ground truth are
mode = 'train/'
# name of the folder containing the input videos
PATH2DATA = os.path.join(PATH, sys.argv[2])
# name of the folder containing ground truth
PATH2GT = os.path.join(PATH, sys.argv[3])
# New data
# directory in which new files should be saved
if not os.path.exists(sys.argv[4]):
  os.mkdir(sys.argv[4])

PATH2OUTPUT = os.path.join(sys.argv[4], 'usiigaci/')
if not os.path.exists(PATH2OUTPUT):
  os.mkdir(PATH2OUTPUT)
  
# name of the new folder
NEW_FOLDER_NAME = 'set{}'
# name of the new ground truth (specified by usiigaci)
masks_names = 'instances_ids.png'
# name of the new input slice (specified by Usiigaci)
input_names = 'raw.tif'

FILES = os.listdir(PATH2GT)

COUNT = 1   
print('Updating image format...')    
for file in FILES:
    # Load masks from segmented videos
    masks = Image.open(os.path.join(PATH2GT, file))    
    image = Image.open(os.path.join(PATH2DATA, file))
    if masks.size[0]<512:
        # Add pixels to the image to fit the same size
        mask_aux = np.zeros((512,512), dtype=np.uint8)
        image_aux = np.zeros((512,512), dtype=np.uint16)
        mask_aux[:masks.size[0], :masks.size[1]] = np.asarray(masks)
        image_aux[:masks.size[0], :masks.size[1]] = np.asarray(image)
        masks = Image.fromarray(mask_aux)
        image = Image.fromarray(image_aux)
        # Save the images
        SET_PATH = os.path.join(PATH2OUTPUT, NEW_FOLDER_NAME.format(COUNT))
        if not os.path.exists(SET_PATH):
            os.makedirs(SET_PATH)

        masks.save(os.path.join(SET_PATH, masks_names))
        
        image.save(os.path.join(SET_PATH, input_names))
        COUNT = COUNT + 1
    else:
        it = np.int(np.floor(masks.size[0]/512))
        for i in range(it): 
            for j in range(it):         
                SET_PATH = os.path.join(PATH2OUTPUT, NEW_FOLDER_NAME.format(COUNT))
                if not os.path.exists(SET_PATH):
                    os.makedirs(SET_PATH)               
                
                masks_aux = masks.crop((512*i, 512*j, 512*(i+1), 512*(j+1)))
                image_aux = image.crop((512*i, 512*j, 512*(i+1), 512*(j+1)))
                masks_aux.save(os.path.join(SET_PATH, masks_names))
              
                image_aux.save(os.path.join(SET_PATH, input_names))
                
                COUNT = COUNT + 1

print('Process finished')
