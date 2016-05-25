import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature

import matplotlib.pyplot as plt

cmap = plt.get_cmap('gnuplot_r', 9)
cmap.set_under('None')

def background(ax):
    '''
    Add standard background features to geoAxes object
    '''
    states = cfeature.NaturalEarthFeature(category='cultural',
                                          name='admin_1_states_provinces_lines',
                                          scale='50m',
                                          facecolor='none')
    
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(states)
    return(ax)

