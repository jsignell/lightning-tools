library('SpatialVx')
library('stringr')

FeatureFinder_gaussian <- function(hold, nx=199, ny=199, ...) {
    look <- FeatureFinder(hold, smoothfun="gauss2dsmooth", smoothfunargs=c(nx=nx, ny=ny), ...)
    return(look)
}