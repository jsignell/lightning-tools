import os
import numpy as np
import pandas as pd
import xarray as xr

new_path = '/run/media/jsignell/WRF/Data/LIGHT/raw/'
out_path = '/home/jsignell/erddapData/Cloud_to_Ground_Lightning/'

def new_files(path, fname, out_path):
    df = pd.read_csv(path+fname, delim_whitespace=True, header=None, parse_dates={'time':[0,1]})
    df = df.drop(5, axis=1)

    df.columns = ['time', 'lat', 'lon', 'amplitude','strokes',
                  'semimajor','semiminor','ratio','angle','chi_squared','nsensors','cloud_ground']
    df.index.name = 'record'
    
    attrs = {'semimajor': {'long_name': 'Semimajor Axis of 50% probability ellipse for each flash',
                           'units': 'km'},
             'semiminor': {'long_name': 'Semiminor Axis of 50% probability ellipse for each flash',
                           'units': 'km'},
             'ratio': {'long_name': 'Ratio of Semimajor to Semiminor'},
             'angle': {'long_name': 'Angle of 50% probability ellipse from North',
                       'units': 'Deg'},
             'chi_squared': {'long_name': 'Chi-squared value of statistical calculation'},
             'nsensors': {'long_name': 'Number of sensors reporting the flash'},
             'cloud_ground': {'long_name': 'Cloud_to_Ground or In_Cloud Discriminator'}}


    ds = df.to_xarray()
    ds.set_coords(['time','lat','lon'], inplace=True)

    for k, v in attrs.items():
        ds[k].attrs.update(v)
        if k == 'cloud_ground':
            ds[k].encoding.update({'dtype': 'S1'})
        elif k == 'nsensors':
            ds[k].encoding.update({'dtype': np.int32, 'chunksizes':(1000,),'zlib': True})
        else:
            ds[k].encoding.update({'dtype': np.double,'chunksizes':(1000,),'zlib': True})

    ds.amplitude.attrs.update({'units': 'kA',
                               'long_name': 'Polarity and strength of strike'})
    ds.amplitude.encoding.update({'dtype': np.double,'chunksizes':(1000,),'zlib': True})
    ds.strokes.attrs.update({'long_name': 'multiplicity of flash'})
    ds.strokes.encoding.update({'dtype': np.int32,'chunksizes':(1000,),'zlib': True})
    ds.lat.attrs.update({'units': 'degrees_north',
                         'axis': 'Y',
                         'long_name': 'latitude',
                         'standard_name': 'latitude'})
    ds.lat.encoding.update({'dtype': np.double,'chunksizes':(1000,),'zlib': True})
    ds.lon.attrs.update({'units': 'degrees_east',
                         'axis': 'X',
                         'long_name': 'longitude',
                         'standard_name': 'longitude'})
    ds.lon.encoding.update({'dtype': np.double,'chunksizes':(1000,),'zlib': True})
    ds.time.encoding.update({'units':'seconds since 1970-01-01', 
                             'calendar':'gregorian',
                             'dtype': np.double,'chunksizes':(1000,),'zlib': True})

    ds.attrs.update({ 'title': 'Cloud to Ground Lightning',
                      'institution': 'Data from NLDN, hosted by Princeton University',
                      'references': 'https://ghrc.nsstc.nasa.gov/uso/ds_docs/vaiconus/vaiconus_dataset.html',
                      'featureType': 'point',
                      'Conventions': 'CF-1.6',
                      'history': 'Created by Princeton University Hydrometeorology Group at {now}'.format(now=pd.datetime.now()),
                      'author': 'jsignell@princeton.edu',
                      'keywords': 'lightning'})

    date = df.time[len(df.index)/2]
    ds.to_netcdf('{out_path}{y}_{m:02d}_{d:02d}.nc'.format(out_path=out_path, y=date.year, m=date.month, d=date.day), 
                 format='netCDF4', engine='netcdf4')

for fname in os.listdir(new_path):
    try:
        new_files(new_path, fname, out_path)
        print fname
    except:
        f = open('messed_up_new_files.txt', 'a')
        f.write(fname+'\n')
        f.close()