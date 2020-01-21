## A. Barbara Metzler
## 13. November 2019

## script to create dataframe with information of images
import re
import get_files
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import mpl_toolkits
#mpl_toolkits.__path__.append('/usr/lib/python2.7/dist-packages/mpl_toolkits/')
from mpl_toolkits.basemap import Basemap

import seaborn as sns
import plotly.graph_objects as go


def create_meta_dataframe():

	#### dataframe with 11 columns
	#Index(['name', 'type_of_image', 'satellite_id', 'date_time', 'coordinates',
       #'band_list', 'cloud_cover', 'lat', 'lon', 'year', 'month'],
      #dtype='object')

	list_files = get_files.main()

	names = []

	for item in list_files:
		names.append(item.split('/')[-1])


	df = pd.DataFrame(names, columns=['name'])

	# Example for name
	#corrected_WV02_2011-03-19.10-52-21_5.859.0.063_P_0.00.tif

	#print(len(list_files))
	#print(df.name.str.split("_", expand = True)[1:3])

	df[['type_of_image', 'satellite_id', 'date_time',
		'coordinates', 'band_list',
		'cloud_cover']] = df.name.str.split("_", expand = True)

	#print(df.head)
	df['cloud_cover'] = df['cloud_cover'].str[:-4]
	df['date_time'] = pd.to_datetime(df['date_time'], format="%Y-%m-%d.%H-%M-%S")


	df['lat'] = df['coordinates'].str[:5]
	df['lon'] = df['coordinates'].str[6:]

	df['year'] = df['date_time'].dt.year
	df['month'] = df['date_time'].dt.month

	return df

df = create_meta_dataframe()
#print (df.head)
