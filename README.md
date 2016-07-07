# lightning-tools
Examples of how to use [pointprocess module](https://github.com/jsignell/point-process) for geospatial analysis of ungridded lightning fields. Lightning data is provided by the National Lightning Detection Network (NLDN). We reformatted the data into NetCDF files. For an example of how to access the data from this format, and make a simple map:

 - ![[Read and grid data](https://github.com/jsignell/lightning-tools/blob/master/Read%20Data.ipynb)] (https://github.com/jsignell/lightning-tools/blob/master/output/US_1993.png "US 1993 Flash Count")

For our purposes, we have chosen several research sites and pulled the data out for these sites. An example of how to look at regions which aren't pre-subsetted, is provided here:

 - ![[Un-subsetted](https://github.com/jsignell/lightning-tools/blob/master/Un-subsetted.ipynb)] (https://github.com/jsignell/lightning-tools/blob/master/output/CapeCod.png "Cape Cod")

Once you have your region of interest, notebooks show how to explore the climatology of the region:

 - ![[Flash Density](https://github.com/jsignell/lightning-tools/blob/master/Climatology.ipynb#flash-density)] (https://github.com/jsignell/lightning-tools/blob/master/output/AnnualMeanFD.png "Flash Density")
 - ![[Diurnal Cycle](https://github.com/jsignell/lightning-tools/blob/master/Climatology.ipynb#diurnal-cycle)] (https://github.com/jsignell/lightning-tools/blob/master/output/DiurnalCycle.png "Diurnal Cycle")
 - ![[Initiation](https://github.com/jsignell/lightning-tools/blob/master/Initiation.ipynb)]
 (https://github.com/jsignell/lightning-tools/blob/master/output/JAInitiationLocations.png "JA Initiation Locations")

To look at particular storms, we can get daily characteristics:

 - ![[Daily](https://github.com/jsignell/lightning-tools/blob/master/Daily.ipynb)] (https://github.com/jsignell/lightning-tools/blob/master/output/DailyMaxLoc.png "Daily Max")

Or we can use an object based method to track features using the r package SpatialVx:

 - ![[Tracking](http://nbviewer.jupyter.org/github/jsignell/lightning-tools/blob/master/Spatial%20Tracking-SpatialVx.ipynb)] (https://github.com/jsignell/lightning-tools/blob/master/output/Tracking.png)

We can even compare how radar based tracking compares to lightning trakcing by loading in output from TITAN for the same storms:

 - ![[TITAN](http://nbviewer.jupyter.org/github/jsignell/lightning-tools/blob/master/TITAN%20radar%20and%20SpatialVx%20lightning%20comparison.ipynb)] (https://github.com/jsignell/lightning-tools/blob/master/output/TitanComparison.png)

