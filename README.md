</br>
# Lightning Tools
[Top](#) | [Presentations](#presentations) | [Data](#data) | [Climatology](#climatology) | [Storms](#storm-level-analyses)

The purpose of this project is to explore methods of conducting geospatial analyses of ungridded lightning data. In the course of this research, a more generalized module was developed. This work depends heavily on that module (see [pointprocess module](https://github.com/jsignell/point-process) for more details).

This research was largely conducted in Python with some 2D spatial tracking done in R. All of the analysis was conducted in Jupyter Notebooks to ease reproducibility and reuse. This project focuses on the American Southwest but examples are provided of how a different geographic region could be used.

**Note**: clicking on any  of the images below will bring you to the notebook that was used to generate the image.

## Presentations
[Top](#) | [Presentations](#presentations) | [Data](#data) | [Climatology](#climatology) | [Storms](#storm-level-analyses)

This research has been presented at:
  - The American Geophysical Union (AGU) fall meeting
    - [Poster](output/AGU_Poster.pdf)


  - The Scientific Python Conference (SciPy)
    - [Slides](https://github.com/jsignell/lightning-tools/blob/master/Lightning%20Talk.ipynb)
    - [Video](https://youtu.be/g15QeR5-Xkk?t=26m27s)

## Data
[Top](#) | [Presentations](#presentations) | [Data](#data) | [Climatology](#climatology) | [Storms](#storm-level-analyses)

Lightning data was provided by the National Lightning Detection Network (NLDN):
>"The National Lightning Detection Network, NLDN, consists of over 100 remote, ground-based sensing stations located across the United States that instantaneously detect the electromagnetic signals given off when lightning strikes the earth's surface. These remote sensors send the raw data via a satellite-based communications network to the Network Control Center operated by Vaisala Inc. in Tucson, Arizona. Within seconds of a lightning strike, the NCC's central analyzers process information on the location, time, polarity, and communicated to users across the country." (*[NASA](http://gcmd.nasa.gov/records/GCMD_NLDN.html)*)

#### Transformation
To facilitate data-use we reformatted the data into NetCDF files and served these files on an internal server using a THREDDS OpenDAP portal.

#### Reading
Once the data are in NetCDF, it is straightforward to read the data using the xarray package.
<a href=https://github.com/jsignell/lightning-tools/blob/master/00%20Read%20Data.ipynb>
  <p align="center">
    <img src=output/US_1993.png?raw=true title="US 1993 Flash Count"/>
  </p>
</a>

#### Subsetting

For our purposes, we have chosen several research sites and pulled the data out for these sites. However, we have also provided methods for subsetting different geographic regions as in this case looking at Cape Cod:
<a href=https://github.com/jsignell/lightning-tools/blob/master/01%20Un-subsetted.ipynb>
  <p align="center">
    <img src=output/CapeCod.png?raw=true title="Cape Cod" width=60%/>
  </p>
</a>

## Climatology
[Top](#) | [Presentations](#presentations) | [Data](#data) | [Climatology](#climatology) | [Storms](#storm-level-analyses)

#### Flash Density
One of the most fundamental climatological analyses of lightning is the flash density - the number of lightning strikes per unit area per unit time.
<a href=https://github.com/jsignell/lightning-tools/blob/master/02%20Climatology.ipynb#flash-density>
  <p align="center">
    <img src=output/AnnualMeanFD.png?raw=true title="Flash Density" width=60%/>
  </p>  
</a>

#### Diurnal Cycle
Another interesting aspect of lightning is the time of day at which it occurs.
We can explore the seasonal dependence in the diurnal cycle of lightning using a plot with polar coordinates where the top represents midnight and the bottom represents noon. Months are indicated by color.
<a href=https://github.com/jsignell/lightning-tools/blob/master/02%20Climatology.ipynb#diurnal-cycle>
  <p align="center">
    <img src=output/DiurnalCycle.png?raw=true title="Diurnal Cycle" width=60%/>
  </p>
</a>

To examine diurnal patterns in space, we map the hour of peak flash count. This shows the topographic dependence of the timing of lightning.
<a href=https://github.com/jsignell/lightning-tools/blob/master/02%20Climatology.ipynb#peak-time>
  <p align="center">
    <img src=output/JAPeakHour.png?raw=true title="Hour of Peak" width=60%/>
  </p>
</a>

#### Initiation
When looking at storms it can be interesting to explore how one strike is related to another. As a first pass, we mapped the locations of strikes in July and August of one year and colored them by the number of strikes that would occur in the proceeding hour.
<a href=https://github.com/jsignell/lightning-tools/blob/master/03%20Initiation.ipynb>
  <p align="center">
    <img src=output/JAInitiationLocations.png?raw=true title="JA Initiation Locations" width=60%/>
  </p>
</a>

## Storm level analyses
[Top](#) | [Presentations](#presentations) | [Data](#data) | [Climatology](#climatology) | [Storms](#storm-level-analyses)

For this research we looked at several case studies over a roughly 1 degree by 1 degree box in Utah. This is what one of the 24 hour case-study periods looks like:
<a href=https://github.com/jsignell/lightning-tools/blob/master/04%20Daily.ipynb>
  <p align="center">
    <img src=output/storm.png?raw=true title="Storm" width=60%/>
  </p>
</a>

#### Conditional Rate of Occurrence
Given a strike at a particular location, what is the rate of occurrence of strikes within 20km in a 2 minute window surrounding the time of strike?

<a href=https://github.com/jsignell/lightning-tools/blob/master/13%20Conditional%20rate%20of%20occurrence.ipynb>
  <p align="center">
    <img src=output/likelihood.png?raw=true title="Conditional Rate of Occurrence" width=60%/>
  </p>
</a>

#### Tracking
We can use an object based method to track features using the r package SpatialVx and compare how radar based tracking compares to lightning tracking by loading in output from TITAN for the same storms:
<a href=http://nbviewer.jupyter.org/github/jsignell/lightning-tools/blob/master/07%20TITAN%20radar%20and%20SpatialVx%20lightning%20comparison.ipynb>
  <p align="center">
    <img src=output/radar_tracked.png?raw=true title="Radar Tracked" width=49%/>
    <img src=output/lightning_tracked.png?raw=true title="Lightning Tracked" width=49%/>
  </p>
</a>

#### Point Process Modeling
The most common point process model is the Poisson process. Lightning strikes constitute a space-time Poisson process if the number of strikes in disjoint time and space intervals are independent and have a Poisson distribution. This independent increment assumption does not hold, because lightning strikes are strongly “clustered”.

Our models build on Cox process models, which are conditional Poisson models in that the rate of occurrence is not a deterministic function of space and time, but a random process.

We setup a model for several case studies and found that the lightning strikes predicted by radar reflectivity agreed reasonably well with observed strikes.

<a href=https://github.com/jsignell/lightning-tools/blob/master/14%Likelihood.ipynb>
  <p align="center">
    <img src=output/poisson_example.png?raw=true title="Example of poisson output" width=60%/>
  </p>
</a>

[Top](#) | [Presentations](#presentations) | [Data](#data) | [Climatology](#climatology) | [Storms](#storm-level-analyses)
