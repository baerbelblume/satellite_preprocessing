### 20. January 2002
#adapted from https://svn.osgeo.org/gdal/trunk/autotest/gcore/gcps2geotransform.py
from osgeo import gdal
import rasterio
import sys


###############################################################################
# Helper to make gcps
def _list2gcps(src_list):
    gcp_list = []
    for src_tuple in src_list:
        gcp = gdal.GCP()
        gcp.GCPPixel = src_tuple[0]
        gcp.GCPLine = src_tuple[1]
        gcp.GCPX = src_tuple[2]
        gcp.GCPY = src_tuple[3]
        gcp_list.append(gcp)
    return gcp_list

xx = '/home/bmetzler/Documents/Imagery/Accra/all_tif_files/8_bands/corrected_WV02_2010-01-12.10-37-48_5.956.-0.479_C-B-G-Y-R-RE-N-N2_0.31.tif'
src = gdal.Open(xx)

dst =rasterio.open(xx)
gcps, gcp_crs = dst.gcps

yay =rasterio.transform.from_gcps(gcps)
print (yay)
print (gcps[1].x)
print (gcps[3].x)
