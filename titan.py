import pandas as pd
from pointprocess.plotting import *

def read_TITAN(fname):
    f = open(fname)
    header = f.readlines()[8].split(':')[1]
    f.close()
    header = [h.strip() for h in header.split(',')]

    def dateparse(Y, m, d, H, M, S):
        d = pd.datetime(int(Y), int(m), int(d), int(H), int(M), int(S))
        return(d)

    dates = ['Year', 'Month', 'Day', 'Hour', 'Min', 'Sec']
    try:
        df = pd.read_csv(fname, skiprows=9, delim_whitespace=True, header=None, names=header, 
                         parse_dates={'date_time': dates}, date_parser=dateparse, index_col='date_time')
    except:
        df = pd.read_csv(fname, skiprows=9, delim_whitespace=True, header=None, names=header)
    return(df)

def storm_locations(df, ax=None, paths=False, zoom=7, zorder=5):
    from cartopy.io.img_tiles import StamenTerrain
    storm_names = dict([(n[1], n[0]) for n in enumerate(df.ComplexNum.unique())])
    gb = df.groupby(df.ComplexNum)
    if ax is None:
        plt.figure(figsize=(14, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())
        background(ax)
        ax.add_image(StamenTerrain(), zoom)
    df.plot.scatter(x='ReflCentroidLon(deg)', 
                    y='ReflCentroidLat(deg)', 
                    c=[storm_names[n] for n in df['ComplexNum']],
                    ax=ax, cmap='rainbow',
                    edgecolor='None', s=50, zorder=zorder)
    if paths:
        for k,v in gb.groups.items():
            gb.get_group(k).plot(x='ReflCentroidLon(deg)', c='k',
                                 y='ReflCentroidLat(deg)', ax=ax, legend=None, zorder=6)
    return(ax)

def bearing_plot(df, ax=None, N=16, bottom=0):
    if ax is None:
        ax = plt.subplot(111, polar=True)
    theta = np.linspace(0.0, 2 *np.pi, N, endpoint=False)
    radii, _ = np.histogram(df['Dirn(DegT)'][df['Dirn(DegT)']>0].values, bins=N)
    width = (2*np.pi) / N

    bars = ax.bar(theta, radii, width=width, bottom=bottom)
    ax.set_theta_zero_location("S")
    ax.set_theta_direction(-1)

    # Use custom colors and opacity
    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.jet(r/float(np.max(radii))))
        bar.set_alpha(0.8)
    return(ax)

def windrose(df, dirn='Dirn(DegT)', speed='Speed(km/hr)', ax=None, N=16, bottom=0):
    if ax is None:
        ax = plt.subplot(111, polar=True)
    theta = np.linspace(0.0, 2 *np.pi, N, endpoint=False)
    ax.set_theta_zero_location("S")
    ax.set_theta_direction(-1)
    width = (2*np.pi) / N
    srange = zip([0,5,10,20,50], [5,10,20,50,100], ['blue','green','yellow','#FF7800','red']) 
    ntot = df[dirn][df[dirn]>0].count()
    
    radii0 = [bottom]*N
    for smin, smax, c in srange:
        cond = ((df[dirn]>0) & (df[speed]>=smin) & (df[speed]<smax))
        radii, _ = np.histogram(df[dirn][cond].values, bins=N)
        radii = radii/float(ntot)*100
        bars = ax.bar(theta, radii, width=width, bottom=radii0, facecolor=c, alpha=0.8)
        #print smin, smax, c, radii
        radii0+= radii

def windrose_cbar(fig=None):
    '''
    If you have a figsize in mind, then pass a figure object to this function
    and the colorbar will be drawn to suit
    '''
    if fig is None:
        fig = plt.figure(figsize=(16,1))
    y = fig.get_figwidth()
    import matplotlib.patches as mpatch
    srange = zip([0,5,10,20,50], [5,10,20,50,100], ['#0000dd','green','#dddd00','#FF7800','#dd0000']) 
    n=1
    for smin, smax, c in srange:
        ax = plt.subplot(1,5,n)
        patch = mpatch.FancyBboxPatch([0,0], 1, 1, boxstyle='square', facecolor=c)
        ax.add_patch(patch)
        plt.axis('off')
        if y>=12:
            ax.text(.1, .4, '{smin} - {smax} km/hr'.format(smin=smin, smax=smax),
                    fontsize=min(18, y+2), fontdict = {'color': 'white'})
        else:
            ax.text(.1, .4, '{smin} - {smax}\nkm/hr'.format(smin=smin, smax=smax),
                    fontsize=min(14, y+5), fontdict = {'color': 'white'})
        n+=1