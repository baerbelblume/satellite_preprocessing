import os, gdal

in_path = '../Accra/all_tif_files/8_bands/'
input_filename = 'corrected_WV02_2010-03-27.10-41-15_5.700.-0.287_C-B-G-Y-R-RE-N-N2_0.04.tif'

out_path = '../Accra/edited_tif_files/output_folder/corrected_WV02_2010-03-27.10-41-15_5.700.-0.287_C-B-G-Y-R-RE-N-N2_0.04/'
output_filename = 'solaris_tile_'

tile_size_x = 224
tile_size_y = 224

print (in_path + input_filename)

ds = gdal.Open(in_path + input_filename)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize

for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)
