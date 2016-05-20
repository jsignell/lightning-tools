from __init__ import *
from plotting import *

class Region:
    '''    
    Acronyms:
    FC = Flash Count
    DC = Diurnal Cycle
    MM = Mean Monthly
    '''
    def __init__(self, subsetted=True, **kwargs):
        if 'city' in kwargs:
            city = kwargs['city']
        else:
            city = kwargs
        self.CENTER = (city['lat'], city['lon'])
        self.RADIUS = city['r']
        self.PATH = city['path']
        self.SUBSETTED = subsetted
    
    def show(self):
        for attr in ['center', 'radius', 'path', 'subsetted']:
            if hasattr(self, attr.upper()):
                print('{a}: {val}'.format(a=attr, val=eval('self.'+attr.upper())))
        
    def define_grid(self, nbins, extents=[], **kwargs):
        if len(extents) > 0:
            minx, maxx, miny, maxy = extents
        else:
            minx = self.CENTER[1]-self.RADIUS
            maxx = self.CENTER[1]+self.RADIUS
            miny = self.CENTER[0]-self.RADIUS
            maxy = self.CENTER[0]+self.RADIUS
        self.gridx = np.linspace(minx, maxx, nbins)
        self.gridy = np.linspace(miny, maxy, nbins)
    
    def get_ds(self, cols=['strokes', 'amplitude'], func='grid', **kwargs):
        '''
        Get the dataset for the region and time (assumes function is available locally)
        
        Parameters
        ----------
        cols: columns to include in final dataset - ['strokes', 'amplitude']
        func: functions to run on the dataset - 'grid'
        y: int, or str indicating year with wildcards allowed
        m: int indicating month
        d: int indicating day
        
        Returns
        -------
        ds: concatenated xr.Dataset for the region and time
        '''
        yyyy, mm, dd = ('*', '*', '*')    
        if 'y' in kwargs:
            yyyy = str(kwargs['y'])
        if 'm' in kwargs:
            mm = '{mm:02d}'.format(mm=kwargs['m'])
        if 'd' in kwargs:
            dd = '{dd:02d}'.format(dd=kwargs['d'])
        fname = '{y}_{m}_{d}.nc'.format(y=yyyy, m=mm, d=dd) 
        
        if self.SUBSETTED:
            def preprocess_func(ds):
                return(ds[cols])    
        else:
            def preprocess_func(ds):
                lat, lon = self.CENTER
                r = self.RADIUS
                bounding_box = ((ds.lat<(lat+r)) & (ds.lat>(lat-r)) & (ds.lon<(lon+r)) & (ds.lon>(lon-r)))
                return(ds[cols].where(bounding_box).dropna('record'))
        ds = xr.open_mfdataset(self.PATH+fname, concat_dim='record', preprocess=preprocess_func)    
        
        if func == 'grid':
            self.set_x_y(ds)
            self.FC_grid = self.__to_grid()
        return(ds)
        
    def set_x_y(self, ds):
        self.x = ds.lon.values
        self.y = ds.lat.values
    
    def to_density(self, ds):
        nyears = ds.time.groupby('time.year').count().shape[0]
        self.FD_grid = self.FC_grid/float(nyears)
    
    def __to_grid(self, group=None, **kwargs):        
        if hasattr(group, '__iter__'):
            grid, _, _ = np.histogram2d(self.x[group], self.y[group], bins=[self.gridx, self.gridy], **kwargs)
        else:
            grid, _, _ = np.histogram2d(self.x, self.y, bins=[self.gridx, self.gridy], **kwargs)
        return(grid.T)
    
    def to_DC_grid(self, ds):
        '''
        Count the number of lightning strikes in each grid cell at each hour of the day
        
        Parameters
        ----------
        ds: xr.Dataset with time, lat, and lon as coordinates
        
        Returns
        -------
        self.DC_grid: dictionary of gridded FC for each hour of the day
        '''
        if not hasattr(self, 'x'):
            self.set_x_y(ds)
        gb = ds.groupby('time.hour')
        d = {}
        for k, v in gb.groups.items():
            d.update({k: self.__to_grid(v)})
        self.DC_grid = d
    
    def to_ncfile(self, t, check_existence=True, full_path=True):
        t = pd.Timestamp(t)
        fname = str(t.date()).replace('-','_')+'.nc'
        if check_existence:
            if not os.path.isfile(self.PATH+fname):
                return
        if full_path:
            return self.PATH+fname
        return fname
    
    def get_daily_ds(self, t, base=12, func='grid'):
        '''
        Get the dataset for the region and day using the base hour
        (assumes function is available locally). 
        If you are interested in 0to0 days it is equivalent to using:
        xr.open_dataset(to_ncfile(t))
        
        Parameters
        ----------
        t: str or pd.Timestamp indicating date
        base: int indicating hours between which to take day - 12
        func: functions to run on the dataset - 'grid'
        
        Returns
        -------
        ds: concatenated xr.Dataset for the region and day
        '''
        t = fix_t(t, base)
        if base == 0:
            ds0 = xr.open_dataset(to_ncfile(t))
        else:
            f0 = self.to_ncfile(t)
            f1 = self.to_ncfile(t+pd.DateOffset(1))

            ds = xr.concat([xr.open_dataset(f) for f in [f0, f1]], dim='record')
            UTC12 = [np.datetime64(t) for t in pd.date_range(start=t, periods=2)]

            ds0 = ds.where((ds.time>UTC12[0]) & (ds.time<UTC12[1])).dropna('record')
            ds.close()
        
        if func=='grid':
            self.set_x_y(ds0)
            self.FC_grid = self.__to_grid()
        return(ds0)
    
    def get_grid_slices(self, t, freq='5min', base=12, filter=True):
        '''
        For the pre-defined grid, use indicated frequency to also bin along the time dimension
        
        Parameter
        --------
        t: str or pd.Timestamp indicating date
        freq: str indicating frequency as in pandas - '5min'
        base: int indicating hours between which to take day - 12
        filter: bool indicating whether or not to take only cloud to ground events
                only valid for new type files
        
        Returns
        -------
        box: np.array of shape (ntimesteps, ny, nx)
        tr: timerange of shape (ntimesteps)
        
        Benchmarking
        ------------
        4.26 s for 600x600 1min
        1.16 s for 600x600 5min
        608 ms for 60x60 5min
        '''
        ds = self.get_daily_ds(t, base=base, func=None)
        ds.close()
        df = ds.to_dataframe()
        if filter:
            df = df[df['cloud_ground']=='G']
        df.index = df.time
        t = fix_t(t, base)
        tr = pd.date_range(t, t+pd.DateOffset(1), freq=freq)
        d = []
        for i in range(len(tr)-1):
            grid, _,_ = np.histogram2d(df.lon[tr[i]:tr[i+1]].values, df.lat[tr[i]:tr[i+1]].values, bins=[self.gridx, self.gridy])
            d.append(grid.T)
        return(np.stack(d), tr)

    
    def get_top(self, n=100, base=12):
        '''
        Quick and dirty method for finding top n FC days for a subsetted region. This method
        uses file size as a proxy for number of events and sorts out the n*2 largest of the old
        style files and the largest n*2 of the new style files. It is not proven to work well for 
        n<10.
        
        Parameters
        ----------
        n: number of top events
        base: hour of day to start and end daily on.
        
        Returns
        -------
        s: sorted series containing days and lightning event counts for top n days
        '''
        if not self.SUBSETTED:
            print('This method only works for pre-subsetted regions.')
            return
        d={}
        fnames = [str(t.date()).replace('-','_')+'.nc' for t in pd.date_range('1991-01-01', '2010-01-01')]
        d = self.__get_top(fnames, d, n*2, base)
        fnames = [str(t.date()).replace('-','_')+'.nc' for t in pd.date_range('2010-01-01', '2015-10-02')]
        d = self.__get_top(fnames, d, n*2, base)
        s = pd.Series(d).sort_values(ascending=False).head(n) 
        return s

    def __get_fsizes(self, fnames):
        fsizes = []
        for i in range(len(fnames)):
            try:
                fsizes.append(os.stat(self.PATH+fnames[i]).st_size)
            except:
                fsizes.append(0)
        s = pd.Series(fsizes, index=fnames)
        s = s.sort_values(ascending=False)
        return s

    def __get_top(self, fnames, d, n, base):
        s = self.__get_fsizes(fnames)
        for i in range(n):
            t = pd.Timestamp(s.index[i].strip('.nc').replace('_','-')+' {base}:00'.format(base=base))
            ifname = fnames.index(s.index[i])
            little_fnames = [self.PATH+f for f in fnames[ifname-1:ifname+2] if os.path.isfile(self.PATH+f)]

            ds = xr.concat([xr.open_dataset(f) for f in little_fnames], dim='record')
            UTC12 = [np.datetime64(t) for t in pd.date_range(start=t-pd.DateOffset(1), periods=3)]

            d.update({pd.Timestamp(UTC12[0]): ds.where((ds.time>UTC12[0]) & (ds.time<UTC12[1])).dropna('record').dims.values()[0]})
            d.update({pd.Timestamp(UTC12[1]): ds.where((ds.time>UTC12[1]) & (ds.time<UTC12[2])).dropna('record').dims.values()[0]})
            ds.close()
        return(d)   
    
    def plot_grid(self, grid, ax=None, cbar=False, 
                  cmap=cmap, interpolation='None', **kwargs):
        '''
        Simple and fast plot generation for gridded data
        
        Parameters
        ----------
        grid: np.array with shape matching gridx by gridy
        ax: matplotlib axes object, if not given generates and populates with basic map
        cbar: bool indicating whether or not to show default colorbar
        **kwargs: fed directly into ax.imshow()
        
        Returns
        -------
        im, ax: (output from ax.imshow, matplotlib axes object)
        
        Benchmarking
        ------------
        33.8 ms for 600x600
        32.9 ms for 60x60
        '''     
        if ax is None:
            ax = background(plt.axes(projection=ccrs.PlateCarree()))
        im = ax.imshow(grid, cmap=cmap, interpolation=interpolation,
                       extent=[self.gridx.min(), self.gridx.max(), self.gridy.min(), self.gridy.max()], 
                       **kwargs)
        if cbar:
            plt.colorbar(im, ax=ax)
        return im, ax