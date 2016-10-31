import numpy as np
import pandas as pd

def get_loc(ll, grid_ll):
    if ll<grid_ll[-1] and ll>grid_ll[0]:
        return np.argmax(grid_ll>ll)
    else:
        return np.nan

def get_l(x, grid_lat, grid_lon):
    '''
    Given a latlon position, return the 1D and 2D index
    of the corresponding grid cell. Also works on series
    of positions

    Parameters
    ----------
    x: (lat, lon) where lat, lon are floats or series
    grid_lat: list of the lat edges of the y grid cells
    grid_lon: list of the lon edges of the x grid cells

    Returns
    -------
    yloc, xloc, l: tuple of integers or tuple of series

    Examples
    --------
    # for one position
    get_l((df.lat[0], df.lon[0]), c.gridy, c.gridx)

    df.assign(**dict(list(zip(['yloc', 'xloc', 'l'],
                              get_l((df.lat, df.lon),
                                    c.gridy, c.gridx)
    '''
    lat, lon = x
    if hasattr(lat, '__iter__'):
        yloc = lat.apply(get_loc, grid_ll=grid_lat)
        xloc = lon.apply(get_loc, grid_ll=grid_lon)
    else:
        yloc = get_loc(lat, grid_lat)
        xloc = get_loc(lon, grid_lon)
    l = (yloc-1)*(grid_lon.shape[0]-1)+(xloc-1)
    return yloc, xloc, l

def at_t(grid_lat, grid_lon, t, dfi, gamma, alpha, beta):
    '''
    This function is the powerhouse so anything we can
    do to quicken things up with pay dividends later on

    Parameters
    ----------
    t: time at which there is a storm element
    dfi: dataframe for just the storm

    Return
    ------
    g: np.array of shape nl
    '''
    # 1.69 ms
    d = dfi.loc[t,:].to_dict()

    sigmai = Equation_12(d['Ai'], gamma)
    Ii = Equation_13(d['Zi'], alpha, beta)

    g = []
    ncols = grid_lon.shape[0]-1
    for iy, y in enumerate(grid_lat[1:]):
        if iy<(d['yloc']-sigmai*2) or iy>(d['yloc']+sigmai*2):
            g.extend([0]*ncols)
            continue
        for ix, x in enumerate(grid_lon[1:]):
            if ix<(d['xloc']-sigmai*2) or ix>(d['xloc']+sigmai*2):
                g.append(0)
                continue
            g.append(Equation_11((y,x), Yi=(d['lat'],d['lon']), sigmai=sigmai, Ii=Ii))
    return np.array(g)

def Equation_11(x, Yi, sigmai, Ii):
    from geopy.distance import great_circle
    g = Ii/(sigmai*(2*np.pi)**.5) * np.exp(-.5*(great_circle(Yi, x).km**2)/sigmai**2)
    return g

def Equation_12(Ai, gamma):
    sigmai = gamma * (Ai/np.pi)**.5
    return sigmai

def Equation_18(box):
    lambda_kl = Equation_19(box)
    return ((box - lambda_kl.reshape(box.shape))**2).sum()

def Equation_13(Zi, alpha, beta):
    Ii = alpha*(Zi-beta)
    return Ii

def Equation_16(grid_lat, grid_lon, tr, mini_df, gamma=1, alpha=0, beta=45):
    '''
    Benchmarking: 2.54 s for nl=12400, nk=102, ni=89
    '''
    gamma_at_t = []
    for i, dfi in mini_df.groupby('i'):
        gamma_at_t.extend([at_t(grid_lat, grid_lon, t, dfi,
                                gamma, alpha, beta) for t in dfi.index])
    gamma_at_t = np.stack(gamma_at_t)

    bar = pd.DataFrame(gamma_at_t, index=mini_df.index)
    bar = bar.sort_index()

    d = {}
    for t in tr:
        d.update({t: bar[bar.index==t].sum()})
    gamma_kl = pd.DataFrame(d).T

    return gamma_kl.values.reshape(box.shape)

def Equation_17(N_kl, gamma_kl):
    '''
    Benchmarking: 5.41 ms
    '''
    L = ((np.subtract(N_kl, gamma_kl))**2).sum()
    return L

def Equation_19(box):
    # total number of time periods
    n1 = box.shape[0]

    # total number of grids
    n2 = box.shape[1] * box.shape[2]

    # sum of counts over all the grid cells divided by n2
    A = box.sum(axis=(1,2))/n2

    # sum of counts over all the timesteps divided by n1
    B = box.sum(axis=0).flatten()/n1

    # 1 over sum of counts divided by n1 and n2
    C = 1/(box.sum()/n1/n2)

    # control lambda of k, l
    lambda_kl = np.outer(A, B)*C

    return lambda_kl
