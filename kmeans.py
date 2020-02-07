### 7/2/2020 run kmeans on multiple images

from os import listdir,makedirs
from os.path import isfile,join
import matplotlib.pylab as plt
import matplotlib.image as mpimg
import cv2
import numpy as np
from PIL import Image
import os.path, sys



path = "/home/bmetzler/Documents/Imagery/Accra/preprocessed/tif_cut_file/rgb/"
out_path = "/home/bmetzler/Documents/Imagery/Accra/preprocessed/kmeans_8_tiles/"


def multi_pic_kmean(path, out_path, K):
    dirs = os.listdir(path)
    for item in dirs:
        fullpath = os.path.join(path,item)
        pathos = os.path.join(out_path,item)
        if os.path.isfile(fullpath):
            #img = Image.open(fullpath)
            img = np.array(Image.open(fullpath))
            f, e = os.path.splitext(pathos)
            #img = cv2.imread('Desktop/Gray/fmtial_gb/good_crop/RD091090(80)Cropped.bmp')
            Z = img.reshape((-1,3))

            # convert to np.float32
            Z = np.float32(Z)

            # define criteria, number of clusters(K) and apply kmeans()
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

            # Now convert back into uint8, and make original image
            center = np.uint8(center)
            res = center[label.flatten()]
            res2 = res.reshape((img.shape))

            #cv2.imshow('res2',res2)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            Image.fromarray(res2).save(f + 'kmeans.png', "png", quality=100)

multi_pic_kmean(path, out_path, 8)
