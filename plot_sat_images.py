## A. Barbara Metzler
## 20. January 2019

## script to plot extent of satellite imagery
import re
import get_files
from create_dataframe import create_meta_dataframe
import gdal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import mpl_toolkits
#mpl_toolkits.__path__.append('/usr/lib/python2.7/dist-packages/mpl_toolkits/')
from mpl_toolkits.basemap import Basemap

import seaborn as sns
import plotly.graph_objects as go
from shapely.geometry import Point, box, Polygon

import shapely
import rasterio
import geopandas as gp
import shapefile as shp
from affine import Affine
from osgeo import gdal,ogr,osr

def GetExtent(gt,cols,rows):
    ''' Return list of corner coordinates from a geotransform

        @type gt:   C{tuple/list}
        @param gt: geotransform
        @type cols:   C{int}
        @param cols: number of columns in the dataset
        @type rows:   C{int}
        @param rows: number of rows in the dataset
        @rtype:    C{[float,...,float]}
        @return:   coordinates of each corner
    '''
    ext=[]
    xarr=[0,cols]
    yarr=[0,rows]

    for px in xarr:
        for py in yarr:
            x=gt[0]+(px*gt[1])+(py*gt[2])
            y=gt[3]+(px*gt[4])+(py*gt[5])
            ext.append([x,y])
            print (x,y)
        yarr.reverse()
    return ext
def ReprojectCoords(coords,src_srs,tgt_srs):
    ''' Reproject a list of x,y coordinates.

        @type geom:     C{tuple/list}
        @param geom:    List of [[x,y],...[x,y]] coordinates
        @type src_srs:  C{osr.SpatialReference}
        @param src_srs: OSR SpatialReference object
        @type tgt_srs:  C{osr.SpatialReference}
        @param tgt_srs: OSR SpatialReference object
        @rtype:         C{tuple/list}
        @return:        List of transformed [[x,y],...[x,y]] coordinates
    '''
    trans_coords=[]
    transform = osr.CoordinateTransformation( src_srs, tgt_srs)
    for x,y in coords:
        x,y,z = transform.TransformPoint(x,y)
        trans_coords.append([x,y])
    return trans_coords

###### SHAPEFILES
accra_shp = '/home/bmetzler/Documents/Outcomes/Accra/Census/Admin_boundary_shapefiles/GAR/GAR boundary 2000/GAR_Bound_EKG.shp'
accra = gp.read_file(accra_shp)
ghana_shp = '/home/bmetzler/Documents/Outcomes/Accra/Census/Admin_boundary_shapefiles/Ghana Districts/Ghana Districts 2010 census/geo2_gh2010/geo2_gh2010.shp'
ghana = gp.read_file(ghana_shp)
ama_file = '/home/bmetzler/Documents/Outcomes/Accra/Census/Admin_boundary_shapefiles/AMA/AMA EA 2000 census/AMA_EA.shp'
ama = gp.read_file(ama_file)
gama_file = '/home/bmetzler/Documents/Outcomes/Accra/Census/Admin_boundary_shapefiles/GAMA/GAMA_EA_shapefiles_20191022/WGS_1984/GAMA_WGS_1984.shp'
gama = gp.read_file(gama_file)


list_files = get_files.main()

widths = []
heights = []

for i in list_files:
    file = gdal.Open(i)
    W = file.RasterXSize
    H = file.RasterYSize
    widths.append(W)
    heights.append(H)

df = create_meta_dataframe()
df_extra = pd.DataFrame(zip(widths, heights), columns=['width', 'height'])

total_df = pd.concat([df, df_extra], axis=1)
total_df['lat'] = total_df['lat'].astype(np.float32)
total_df['lon'] = total_df['lon'].astype(np.float32)

gcp0_x = []
gcp0_y = []
gcp1_x = []
gcp1_y = []
gcp2_x = []
gcp2_y = []
gcp3_x = []
gcp3_y = []

for i in list_files:
    raster = gdal.Open(i)
    gt = raster.GetGeoTransform()
    ncol = raster.RasterXSize
    nrow = raster.RasterYSize

    if gt == (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
        file = rasterio.open(i)
        gcps, gcp_crs = file.gcps
        #control_points = rasterio.transform.from_gcps(gcps)
        gcp0_x.append(gcps[0].x)
        gcp0_y.append(gcps[0].y)
        gcp1_x.append(gcps[1].x)
        gcp1_y.append(gcps[1].y)
        gcp2_x.append(gcps[2].x)
        gcp2_y.append(gcps[2].y)
        gcp3_x.append(gcps[3].x)
        gcp3_y.append(gcps[3].y)

    else:
        ext=GetExtent(gt,ncol,nrow)
        src_srs=osr.SpatialReference()
        src_srs.ImportFromWkt(raster.GetProjection())
        tgt_srs = src_srs.CloneGeogCS()
        geo_ext=ReprojectCoords(ext,src_srs,tgt_srs)
        gcp0_x.append(geo_ext[0][0])
        gcp0_y.append(geo_ext[0][1])
        gcp1_x.append(geo_ext[1][0])
        gcp1_y.append(geo_ext[1][1])
        gcp2_x.append(geo_ext[2][0])
        gcp2_y.append(geo_ext[2][1])
        gcp3_x.append(geo_ext[3][0])
        gcp3_y.append(geo_ext[3][1])


ground_cp = pd.DataFrame(zip(gcp0_x, gcp0_y, gcp1_x, gcp1_y, gcp2_x, gcp2_y, gcp3_x, gcp3_y), columns=['gcp0_x', 'gcp0_y', 'gcp1_x', 'gcp1_y', 'gcp2_x', 'gcp2_y', 'gcp3_x', 'gcp3_y'])
total = pd.concat([total_df, ground_cp], axis=1)

### CREATE PLOT with Polygons
fig, ax = plt.subplots(figsize = (20, 20))

patches = []
for index, row in total.iterrows():
    pol = Polygon([[row['gcp0_x'], row.gcp0_y], [row.gcp1_x, row.gcp1_y], [row.gcp2_x, row.gcp2_y], [row.gcp3_x, row.gcp3_y]])
    patches.append(pol)

pp = pd.DataFrame(patches, columns=['polys'])
plot_df = pd.concat([total, pp], axis=1)
gf = plot_df.set_geometry('polys')

#total.plot(kind="scatter", x="gcp0_x", y="gcp0_y", ax=ax, c='red')
ghana.plot(ax=ax, alpha=0.4)
gf.plot(ax=ax, cmap='OrRd', alpha=0.5)
ama.plot(ax=ax)

plt.show()
