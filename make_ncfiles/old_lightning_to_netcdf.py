import os
import numpy as np
import pandas as pd
import xarray as xr

old_path = '/run/media/jsignell/WRF/Data/LIGHT/Data_1991-2009/'
out_path = '/home/jsignell/erddapData/Cloud_to_Ground_Lightning/'
    
def write_day(df, out_path):

    ds = df.drop('index', axis=1).to_xarray()
    ds.set_coords(['time','lat','lon'], inplace=True)
    
    ds.amplitude.attrs.update({'units': 'kA',
                               'long_name': 'Polarity and strength of strike'})
    ds.amplitude.encoding.update({'dtype': np.double})
    ds.strokes.attrs.update({'long_name': 'multiplicity of flash'})
    ds.strokes.encoding.update({'dtype': np.int32})
    ds.lat.attrs.update({'units': 'degrees_north',
                         'axis': 'Y',
                         'long_name': 'latitude',
                         'standard_name': 'latitude'})
    ds.lat.encoding.update({'dtype': np.double})
    ds.lon.attrs.update({'units': 'degrees_east',
                         'axis': 'X',
                         'long_name': 'longitude',
                         'standard_name': 'longitude'})
    ds.lon.encoding.update({'dtype': np.double})
    ds.time.encoding.update({'units':'seconds since 1970-01-01', 
                             'calendar':'gregorian',
                             'dtype': np.double})

    ds.attrs.update({ 'title': 'Cloud to Ground Lightning',
                      'institution': 'Data from NLDN, hosted by Princeton University',
                      'references': 'https://ghrc.nsstc.nasa.gov/uso/ds_docs/vaiconus/vaiconus_dataset.html',
                      'featureType': 'point',
                      'Conventions': 'CF-1.6',
                      'history': 'Created by Princeton University Hydrometeorology Group at {now} '.format(now=pd.datetime.now()),
                      'author': 'jsignell@princeton.edu',
                      'keywords': 'lightning'})


    date = df.time[len(df.index)/2]
    
    ds.to_netcdf('{out_path}{y}_{m:02d}_{d:02d}.nc'.format(out_path=out_path, y=date.year, m=date.month, d=date.day), 
                 format='netCDF4', engine='netcdf4')

def old_files(path, fname, out_path):
    df = pd.read_csv(path+fname, delim_whitespace=True, header=None, names=['D', 'T','lat','lon','amplitude','strokes'],
                     parse_dates={'time':[0,1]})
    
    days = np.unique(df.time.apply(lambda x: x.date()))
    for day in days:
        df0 = df[(df.time >= day) & (df.time < day+pd.DateOffset(1))]
        df0 = df0.reset_index()
        df0.index.name = 'record'
        write_day(df0, out_path)
        

for fname in os.listdir(old_path):
    try:
        old_files(old_path, fname, out_path)
        print fname
    except:
        f = open('messed_up_old_files.txt', 'a')
        f.write(fname+'\n')
        f.close()
