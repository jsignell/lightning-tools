# Lightning Tools

Using the [pointprocess module](https://github.com/jsignell/point-process) we develop methods of conducting geospatial analysis of ungridded lightning fields. This work was largely conducted in Python with some 2D spatial tracking done in R. All of the analysis was conducted in Jupyter Notebooks to ease reproducibility and reuse. This project focuses on the American Southwest but examples are provided of how a different geographic region could be used.  

Lightning data was provided by the National Lightning Detection Network (NLDN).

## Read Data
To facilitate data-use we reformatted the data into NetCDF files. For an example of how to access the data from this format, and make a simple map check out this notebook on [reading data](https://github.com/jsignell/lightning-tools/blob/master/00%20Read%20Data.ipynb)

![Climatology](output/US_1993.png?raw=true "US 1993 Flash Count")

For our purposes, we have chosen several research sites and pulled the data out for these sites. An example of how to look at regions which aren't pre-subsetted, is provided here: [subset data](https://github.com/jsignell/lightning-tools/blob/master/01%20Un-subsetted.ipynb)

![Unsubsetted](output/CapeCod.png?raw=true "Cape Cod")

## General Climatology
Once you have your region of interest, notebooks show how to explore the climatology of the region:

- [Flash Density](https://github.com/jsignell/lightning-tools/blob/master/02%20Climatology.ipynb#flash-density)

![Climatology](output/AnnualMeanFD.png?raw=true "Flash Density")

- [Diurnal Cycle](https://github.com/jsignell/lightning-tools/blob/master/02%20Climatology.ipynb#diurnal-cycle)

![Climatology](output/DiurnalCycle.png?raw=true "Diurnal Cycle")

- [Initiation](https://github.com/jsignell/lightning-tools/blob/master/03%20Initiation.ipynb)

![Initiation](output/JAInitiationLocations.png?raw=true "JA Initiation Locations")

## Storm level analyses
To look at particular storms, we can get daily characteristics: [Daily](https://github.com/jsignell/lightning-tools/blob/master/04%20Daily.ipynb)

![Daily](output/DailyMaxLoc.png?raw=true "Daily Max")

Or we can use an object based method to track features using the r package SpatialVx: [Tracking](http://nbviewer.jupyter.org/github/jsignell/lightning-tools/blob/master/06%20Storm%20Tracking-SpatialVx.ipynb)

![Tracks](output/Tracking.png?raw=true "Tracking")

We can even compare how radar based tracking compares to lightning trakcing by loading in output from TITAN for the same storms: [TITAN](http://nbviewer.jupyter.org/github/jsignell/lightning-tools/blob/master/07%20TITAN%20radar%20and%20SpatialVx%20lightning%20comparison.ipynb) 

![TITAN](output/TitanComparison.png?raw=true "Titan Comparison)

