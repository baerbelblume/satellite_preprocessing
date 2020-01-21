import os, gdal

in_path = '../Accra/all_tif_files/4_bands/'
input_filename = 'corrected_QB02_2009-02-02.10-46-37_5.784.-0.124_B-G-R-N_0.00.tif'

out_path = '../Accra/all_tif_files/4_bands/output_folder/corrected_QB02_2009-02-02.10-46-37_5.784.-0.124_B-G-R-N_0.00/'
output_filename = 'solaris_tile_'

tile_size_x = 512
tile_size_y = 512

print (in_path + input_filename)

ds = gdal.Open(in_path + input_filename)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize

for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + str(input_filename) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)
	
