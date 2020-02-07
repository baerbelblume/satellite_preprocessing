import os
import glob
import gdal

in_path = '/home/bmetzler/Documents/Imagery/Accra/all_tif_files/8_bands/'
out_path = '/home/bmetzler/Documents/Imagery/Accra/preprocessed/tif_cut_file/8_bands/'

tile_size_x = 224
tile_size_y = 224

for filepath in glob.glob(os.path.join(in_path, '*.tif')):
    ds = gdal.Open(filepath)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize

    out = filepath.split('/', 8)[8]
    #print (out)
    output_filename = out.split('.', 6)[0:6]
    output_filename = ''.join(output_filename)

    #com_string = "gdal_translate -co 'TILED=YES' -co BLOCKXSIZE=224 -co BLOCKYSIZE=224 -co COMPRESS=LZW -ot Byte -scale" + " " + str(filepath) + " " + str(output_filename) + "_tiled" + ".tif"
    #print (com_string)
    #os.system(com_string)
    for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
            #com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
            com_string = "gdal_translate -b 2 -b 3 -b 5 -scale 0 2047 0 255 -ot Byte -co PHOTOMETRIC=RGB -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(filepath) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
            os.system(com_string)
            break
