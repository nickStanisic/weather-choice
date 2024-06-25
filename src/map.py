
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import os

def create_map(lowTemp, highTemp, info):
    
    colorado = gpd.read_file('../Shapefiles/tl_rd22_08_tract.shp')
    
    lat = []
    lon = []
    withinRange = []

    for i in range (0,len(info)):
        lat.append(info[i].get('lat'))
        lon.append(info[i].get('lon'))
        withinRange.append(info[i].get('withinRange'))
    
    data = pd.DataFrame({
            'latitude': lat,
            'longitude': lon,
            'withinRange': withinRange
        })
    bins = [int(lowTemp) - 100,int(lowTemp),int(highTemp)]
    colors = ['red', 'blue']

    fig, ax = plt.subplots(figsize=(10,10))


    colorado.plot(ax=ax, color='white', edgecolor='black')

    withinRangeFrame = pd.DataFrame({
            'latitude': [],
            'longitude': [],
            'withinRange': []
        })
    
    outOfRangeFrame = pd.DataFrame({
            'latitude': [],
            'longitude': [],
            'withinRange': []
        })
    outIndex = 0
    inIndex = 0
    for i in range (0,len(data)):
        row = data.loc[i]
        if row['withinRange'] == False:
            outOfRangeFrame.loc[outIndex] = row
            outIndex += 1
        else:
            withinRangeFrame.loc[inIndex] = row
            inIndex += 1
            
    ax.scatter(outOfRangeFrame['longitude'], outOfRangeFrame['latitude'], color=colors[0], s=5000, marker='s', alpha = .4, label = f'temp < {bins[1]} or > {bins[2]}F')
    ax.scatter(withinRangeFrame['longitude'], withinRangeFrame['latitude'], color=colors[1], s=5000, marker='s', alpha = .4, label = f'{bins[1]}-{bins[2]}F')

    legend_handles = [
        Line2D([0], [0], marker='s', color='w', markerfacecolor=colors[0], markersize=10, label=f'temp < {bins[1]} or > {bins[2]}F'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor=colors[1], markersize=10, label=f'{bins[1]}-{bins[2]}F')
    ]

    plt.legend(handles=legend_handles, title='Temperature (F)', loc='lower left')

    plt.title('Temperature map of Colorado')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    map_path = os.path.join('static', 'map.png')
    plt.savefig(map_path)
    plt.close(fig)
    return map_path