import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import srtm, PostprocessedRasterSource, LocatedImage
from cartopy.io.srtm import SRTM3Source

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
                               azimuth=135, altitude=15)
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
    return ax
    