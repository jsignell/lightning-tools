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
        try:
            df = pd.read_csv(fname, skiprows=9, delim_whitespace=True, header=None, names=header, 
                             parse_dates={'date_time': dates}, date_parser=dateparse, index_col='date_time',
                             skipfooter=3, engine='python')
        except:
            print('time not parsed')
            df = pd.read_csv(fname, skiprows=9, delim_whitespace=True, header=None, names=header)
            
    return df

def bearing_plot(df, ax=None, N=16, bottom=0):
    '''
    This one is a little tricky because at initiation the direction is set to zero, 
    so we first need to get rid of all the zeros. Luckily we know that there are no 
    actual zero values because 360 is included in the possible directions
    '''
    if ax is None:
        ax = plt.subplot(111, polar=True)
    theta = np.linspace(0.0, 2 *np.pi, N+1)
    radii, _ = np.histogram(df['Dirn(DegT)'][df['Dirn(DegT)']>0].values, bins=(theta/np.pi*180))
    width = (2*np.pi) / N

    bars = ax.bar(theta[:-1], radii, width=width, bottom=bottom)
    ax.set_theta_zero_location("S")
    ax.set_theta_direction(-1)

    # Use custom colors and opacity
    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.jet(r/float(np.max(radii))))
        bar.set_alpha(0.8)
    return ax

def windrose(df, dirn='Dirn(DegT)', speed='Speed(km/hr)', ax=None, N=16, bottom=0):
    if ax is None:
        ax = plt.subplot(111, polar=True)
    theta = np.linspace(0.0, 2 *np.pi, N+1)
    ax.set_theta_zero_location("S")
    ax.set_theta_direction(-1)
    width = (2*np.pi) / N
    srange = zip([0,5,10,20,50], [5,10,20,50,100], ['#0000dd','green','#dddd00','#FF7800','#dd0000']) 
    ntot = df[dirn][df[dirn]>0].count()
    
    radii0 = [bottom]*N
    for smin, smax, c in srange:
        cond = ((df[dirn]>0) & (df[speed]>=smin) & (df[speed]<smax))
        radii, _ = np.histogram(df[dirn][cond].values, bins=(theta/np.pi*180))
        radii = radii/float(ntot)*100
        bars = ax.bar(theta[:-1], radii, width=width, bottom=radii0, facecolor=c, alpha=0.8)
        #print smin, smax, c, radii
        radii0+= radii

def up_tilt(s, yp, xp):
    x0 = s.lon
    y0 = s.lat
    if (0 < s.tilt_orient <=45) or (315<s.tilt_orient <=360) and yp>y0:
        return True
    elif (45 < s.tilt_orient <=135) and xp>x0:
        return True
    elif (135 < s.tilt_orient <=225) and yp<y0:
        return True
    elif (225 < s.tilt_orient <=315) and xp<x0:
        return True
    else:
        return False

def in_envelope(s, yp, xp, by=1):
    from math import cos, sin, radians,  pi
    alpha = radians(-90-s.orient)
    x0 = s.lon
    y0 = s.lat
    a = s.major/100.
    b = s.minor/100.
    if (((cos(alpha)*(xp-x0)+sin(alpha)*(yp-y0))**2)/(a**2) + ((sin(alpha)*(xp-x0)-cos(alpha)*(yp-y0))**2)/(b**2)) <=by:
        return True
    else:
        return False