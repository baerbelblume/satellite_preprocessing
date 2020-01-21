## A. Barbara Metzler
## 25. November 2019

## script to create dataframe with information of images
import re
import get_files
from create_dataframe import create_meta_dataframe
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import mpl_toolkits
#mpl_toolkits.__path__.append('/usr/lib/python2.7/dist-packages/mpl_toolkits/')
from mpl_toolkits.basemap import Basemap

import seaborn as sns
import plotly.graph_objects as go


#### get DataFrame

df = create_meta_dataframe()



## SEABORN PLOTTING
#show date_time/ satellite_id relationship
#sns.catplot(y="date_time", hue="satellite_id", kind="count", palette="pastel", edgecolor=".6", data=df)

#show bandlist/ satellite_id relationship
#sns.catplot(y="band_list", hue="type_of_image", kind="count", palette="pastel", edgecolor=".6", data=df)


#show months
#g = sns.catplot(y="month", hue="year", kind="count", palette="pastel", edgecolor=".6", units=12, data=df)
#g.set(ylim=(0, 12))
#g.set_yticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])




## MAPPING
#create map with points of images taken
fig = go.Figure(data=go.Scattergeo(
        lon = df['lon'],
        lat = df['lat'],
        marker_color = df['year'],
        text=df['year'],
        mode = 'markers+text',
        showlegend=False))
fig.update_traces(textposition='top center')

fig.update_layout(
        title = 'Satellite Image Location: Accra',
        geo = dict(
        scope = 'africa',
        showland = True,
        landcolor = "rgb(212, 212, 212)",
        subunitcolor = "rgb(255, 255, 255)",
        countrycolor = "rgb(255, 255, 255)",
        showlakes = True,
        lakecolor = "rgb(255, 255, 255)",
        showsubunits = True,
        showcountries = True,
        resolution = 50))

fig.show()
