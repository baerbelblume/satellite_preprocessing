#import gdal
#import osr
#import ogr
import glob
import subprocess

import rasterio
from pathlib import Path
from rasterio.mask import mask
from rasterio.plot import show
import os, sys
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.image as mpimg
import tifffile as tiff

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

import numpy as np
import glob
# get corner coordinates
def GrabCornerCoordinates(FileName):
    src = gdal.Open(FileName)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    return [ulx,uly,lrx,lry]
        
# reproject files into WGS84
def ToWGS84(FileName,OutName):
    gdal_str="gdalwarp -t_srs wgs84 "+FileName +" "+OutName
    print(gdal_str)
    os.system(gdal_str)


# check corner points of list of satellite corner coordinates
def Check_PlotExtentions(boxes,plotname=None):
    #Input:
        #boxes -- dict of corner points (aka list of list), with [Upper Left Long, Upper Left Lat, Lower Right Long, Lower Right Lat]
    i=0
    color1=['-k','-b','-g','-m','-o','-c', '-y', '-p', '-k','-b','-g','-m','-o','-c', '-y', '-p', '-k','-b','-g','-m','-o','-c', '-y', '-p']
    #plt.figure(figsize=(12,8))
    
    fig, ax = plt.subplots(figsize = (20, 20))
    for k in boxes.keys():
        X=[boxes[k][0],boxes[k][2],boxes[k][2],boxes[k][0],boxes[k][0]]
        Y=[boxes[k][1],boxes[k][1],boxes[k][3],boxes[k][3],boxes[k][1]]
        ax.plot(X,Y,color1[i],label=k,linewidth=2.0)
        i+=1
    
    #i=0
    #color2=['--r','--y','--c','--o','--g']
    #for k in SE:
    #    X=[SE[k][0],SE[k][2],SE[k][2],SE[k][0],SE[k][0]]
    #    Y=[SE[k][1],SE[k][1],SE[k][3],SE[k][3],SE[k][1]]
    #    plt.plot(X,Y,color2[i],label=k,linewidth=4.0) 
    #    i+=1
        
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    data = rasterio.open('~/ReProj_Files/corrected_WV02_2010-01-12.10-37.tif')
    
    ama_file = '~/AMA_EA.shp'
    ama = gpd.read_file(ama_file)
    
    box_file = '~/accra_box.shp'
    box = gpd.read_file(box_file)
    
    geo = box.to_crs(crs=data.crs.data)
    
    ama.plot(ax=ax, alpha=0.5)
    #geo.plot(ax=ax, alpha=0.1)
    
    if plotname!= None:
        plt.savefig(plotname+'.png')
        
def GetBorder(cx,cy,xres,yres):
    ulx=cx-0.5*xres
    uly=cy-0.5*yres
    lrx=ulx+xres
    lry=uly+yres
    return [ulx,uly,lrx,lry]

def GrabRes(FileName):
    src = gdal.Open(FileName)
    ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
    return [xres,yres]

# check if images intersect
def CheckIntersect(tif_file, shp_file):
    raster = gdal.Open(sample_tif)
    vector = ogr.Open(ama_file)

    ulx,uly,lrx,lry = GrabCornerCoordinates(tif_file)
    
    cols = raster.RasterXSize
    rows = raster.RasterYSize
    
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(ulx, uly)
    ring.AddPoint(ulx, lry)
    ring.AddPoint(lrx, lry)
    ring.AddPoint(lrx, uly)
    ring.AddPoint(ulx, uly)

    rasterGeometry = ogr.Geometry(ogr.wkbPolygon)
    rasterGeometry.AddGeometry(ring)

    # Get vector geometry
    layer = vector.GetLayer()
    feature = layer.GetFeature(0)
    vectorGeometry = feature.GetGeometryRef()

    #if rasterGeometry.Intersect(vectorGeometry) == True:
    #    print (tif_file)
    return (rasterGeometry.Intersect(vectorGeometry))


def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

# Function to normalize the grid values
def normalize(array):
    """Normalizes numpy arrays into scale 0.0 - 1.0"""
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))



############### PCA
## folder with multispectral tif files

def pca_multispectral(files, folder, n_bands)
    for ix, raster_file in enumerate(files):
        raster = tiff.imread(raster_file)
        img_shape =  raster.shape

        # specify no of bands in the image
        n_bands = 8
        # 3 dimensional dummy array with zeros
        MB_img = np.zeros((img_shape[0],img_shape[1],n_bands))
        # Convert 2d band array in 1-d to make them as feature vectors and Standardization
        MB_matrix = np.zeros((MB_img[:,:,0].size,n_bands))

        #normalize
        for i in range(n_bands):
            MB_array = raster[:,:,i].flatten()  # covert 2d to 1d array
            MB_arrayStd = (MB_array - MB_array.mean())/MB_array.std()
            MB_matrix[:,i] = MB_arrayStd

        pca = PCA(n_components=8)
        transformed_data = pca.fit(MB_matrix)
        X_pc = pca.transform(MB_matrix)
        X = X_pc.reshape(img_shape)

        tiff.imsave(folder+str(ix)+'.tif', X[:,:,1])

#### example to run PCA

files = glob.glob('~/Imagery/WV2/multi/AMA/ReProj/Clipped_AMA_box/*.tif')
folder = '~/Imagery/WV2/multi/AMA/ReProj/Clipped_AMA_box/PCA/'
n_bands = 8

pca_multispectral(files, folder, n_bands)

# create tiles 
def create_tiles(input_folder, output_folder, tilesize=128, pan=True):
    for ix, file in enumerate(glob.glob(input_folder + '*.tif')):
        output_filename = Path(file).stem
        #com_string = "gdal_translate -of GTiff -co TILED=YES -co BLOCKXSIZE=128 -co BLOCKYSIZE=128 -ot Byte " + " " + str(file) + " " + str(filepath +output_filename) + "_tiled" + ".tif"
        tile_size_x = tilesize
        tile_size_y = tilesize
        print (output_filename)
        
        ds = rasterio.open(file)
        #ds = gdal.Open(file)
        #band = ds.GetRasterBand(1)
        #xsize = band.XSize
        #ysize = band.YSize

        xsize = ds.width
        ysize= ds.height
        
        print (xsize, ysize)
        
        if pan == True:
            for i in range(0, xsize, tile_size_x):
                    for j in range(0, ysize, tile_size_y):
                        com_string = "gdal_translate -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(file) + " " + str(output_folder+ output_filename) + str(i) + "_" + str(j) + ".tif"
                        #print (com_string)
                        #-scale 0 2047 0 255
                        os.system(com_string)
        else:
                        
            for i in range(0, xsize, tile_size_x):
                    for j in range(0, ysize, tile_size_y):
                        com_string = "gdal_translate -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(file) + " " + str(output_folder+ output_filename) + str(i) + "_" + str(j) + ".tif"
                        os.system(com_string)

        print (ix, 'done')

################### Example for clipping tiles
Proj = '~/accra-maxar-19/'
Clipped = '~/accra-maxar-19/256/'

create_tiles(Proj, Clipped, tilesize=256, pan=True)

