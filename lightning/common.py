import os
import pandas as pd

def to_decimal(degree, minute, second):
    return(degree+(minute/60.)+(second/3600.))

def fix_t(t, base):
    t = pd.Timestamp(t)
    if t.hour != base:
        t += pd.DateOffset(hours=base)
    return(t)

def import_r_tools(filename='r-tools.R'):
    from rpy2.robjects import pandas2ri, r, globalenv
    from rpy2.robjects.packages import STAP
    pandas2ri.activate()
    path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(path,filename), 'r') as f:
        string = f.read()
    rfuncs = STAP(string, "rfuncs")
    return rfuncs

def dotvars(**kwargs):
    res = {}
    for k, v in kwargs.items():
        res[k.replace('_', '.')] = v
    return res

def get_fsizes(fnames):
    fsizes = []
    for i in range(len(fnames)):
        try:
            fsizes.append(os.stat(fnames[i]).st_size)
        except:
            fsizes.append(0)
            s = pd.Series(fsizes, index=fnames)
            s = s.sort_values(ascending=False)
    return s

def get_top(fnames, d, n, base):
    s = get_fsizes(fnames)
    for i in range(n):
        t = fix_t(t, base)
        ifname = fnames.index(s.index[i])
        little_fnames = [f for f in fnames[ifname-1:ifname+2] if os.path.isfile(f)]

        ds = xr.concat([xr.open_dataset(f) for f in little_fnames], dim='record')
        UTC12 = [np.datetime64(t) for t in pd.date_range(start=t-pd.DateOffset(1), periods=3)]

        d.update({pd.Timestamp(UTC12[0]): ds.where((ds.time>UTC12[0]) & (ds.time<UTC12[1])).dropna('record').dims.values()[0]})
        d.update({pd.Timestamp(UTC12[1]): ds.where((ds.time>UTC12[1]) & (ds.time<UTC12[2])).dropna('record').dims.values()[0]})
        ds.close()
    return(d)  