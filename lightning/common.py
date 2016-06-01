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

def get_fsizes(fnames, tr):
    fsizes = []
    for i in range(len(fnames)):
        try:
            fsizes.append(os.stat(fnames[i]).st_size)
        except:
            fsizes.append(0)
    s = pd.Series(fsizes, index=tr)
    s = s.sort_values(ascending=False)
    return(s)
