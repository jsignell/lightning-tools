import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import srtm, PostprocessedRasterSource, LocatedImage
from cartopy.io.srtm import SRTM3Source

import matplotlib.pyplot as plt
import numpy as np

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
    ax.add_feature(cfeature.OCEAN, zorder=5)
    ax.add_feature(cfeature.COASTLINE, zorder=6)
    ax.add_feature(cfeature.BORDERS, zorder=7)
    ax.add_feature(states, zorder=8)
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    return(ax)

def shade(located_elevations):
    """
    Given an array of elevations in a LocatedImage, add a relief (shadows) to
    give a realistic 3d appearance.

    """
    new_img = srtm.add_shading(located_elevations.image,
                               azimuth=315, altitude=45)
    return LocatedImage(new_img, located_elevations.extent)

def shaded_relief(ax, extents=[]):
    """
    After the example illustrating the automatic download of STRM data, and adding of
    shading to create a so-called "Shaded Relief SRTM".

    Originally contributed by Thomas Lecocq (http://geophysique.be).

    """
    # Define a raster source which uses the SRTM data and applies the
    # shade function when the data is retrieved.
    shaded_srtm = PostprocessedRasterSource(SRTM3Source(), shade)

    # Add the shaded SRTM source to our map with a grayscale colormap.
    ax.add_raster(shaded_srtm, cmap='Greys')

    # This data is high resolution, so pick a small area which has some
    # interesting orography.
    if len(extents) == 4:
        ax.set_extent(extents)
    return(ax)

def dem(ax, dem_cbar=False):
    x0, xn, y0, yn = ax.get_extent()
    elev, crs, extent = srtm.srtm_composite(np.floor(x0),np.floor(y0), np.ceil(xn-x0),np.ceil(yn-y0))

    levels = [((elev.max()-elev.min())/whole, whole) for whole in [10,20,50,100,200,500,1000]]
    level = min([level for level in levels if 5<level[0]<20])

    plot_kwargs = dict(cmap=plt.get_cmap('Greys', level[0]), 
                       vmin=level[1]* np.floor_divide(elev.min(), level[1]),
                       vmax=level[1]* np.floor_divide(elev.max(), level[1]))
    dem = ax.imshow(elev, extent=extent, transform=crs, origin='lower', **plot_kwargs)
    if dem_cbar:
        plt.colorbar(dem, ax=ax, ticks=range(int(plot_kwargs['vmin']), int(plot_kwargs['vmax']), level[1]), 
                     orientation='horizontal');
    return(ax)
        
def urban(ax, **kwargs):
    urban = cfeature.NaturalEarthFeature(category='cultural',
                                         name='urban_areas',
                                         scale='10m',
                                         edgecolor='red', 
                                         facecolor='None')
    ax.add_feature(urban, zorder=9, **kwargs)
    return(ax)
    