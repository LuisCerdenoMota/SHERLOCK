<p align="center">
  <img width="350" src="logo/sherlock3.png">
</p>

The <b>SHERLOCK</b> (<b>S</b>earching for <b>H</b>ints of <b>E</b>xoplanets f<b>R</b>om <b>L</b>ightcurves 
<b>O</b>f spa<b>C</b>e-based see<b>K</b>ers) <b>PIPE</b>line is a user-friendly pipeline, which
minimizes the interaction of the user to the minimum when using data coming from Kepler or TESS missions. SHERLOCK makes use of previous well-known and well-tested codes which allow the exoplanets community to explore the public data from space-based missions without need of a deep knowledge of how the data are built and stored. 
In most of cases the user only needs to provide with a KOI-ID, EPIC-ID, TIC-ID or coordinates of the host star where wants to search for exoplanets.

## Main Developers
Active: <i>[F.J. Pozuelos](https://github.com/franpoz), 
[M. Dévora](https://github.com/martindevora) </i> 

## Additional contributors 
<i>A. Thuillier</i> & <i>[L. García](https://github.com/LionelGarcia) </i>

## SHERLOCK PIPEline Workflow
It is important to note that SHERLOCK PIPEline uses some csv files with TOIs, KOIs and EPIC IDs
from the TESS, Kepler and K2 missions. Therefore in your first execution of the pipeline it might
take longer because it will download the information.

### Provisioning of light curve
The light curve for every input object needs to be obtained from its mission database. For this we 
use the high level API of [Lightkurve](https://github.com/KeplerGO/lightkurve), which enables the
download of the desired light curves for TESS, Kepler and K2 missions. We also include Full Frame
Images from the TESS mission by the usage of [ELEANOR](https://adina.feinste.in/eleanor/). We 
always use the PDCSAP signal from the ones provided by any of those two packages.

### Pre-processing of light curve
In many cases we will find light curves which contain several systematics like noise, high dispersion
beside the borders, intense periodicities caused by pulsators, fast rotators, etc. SHERLOCK PIPEline
provides three methods to reduce these most important systematics.

#### Local noise reduction.
For local noise, where very close measurements show high deviation from the local trend, we apply a
Savitzky-Golay filter. This has proved a highly increment of the SNR of found transits. This feature 
can be disabled with a flag.

#### High RMS areas masking.
Sometimes the spacecrafts have to perform reaction wheels momentum dumps by firing thrusters,
sometimes there is high light scattering and sometimes the spacecraft can infer some jitter into
the signal. For all of those systematics we found that in many cases the data from those regions
should be discarded. Thus, SHERLOCK PIPEline includes a binned RMS computation where bins whose
RMS value is higher than a configurable factor multiplied by the median get automatically masked.
This feature can be disabled with a flag. 

#### Detrend of intense periodicities. 
Our most common foes with high periodicties are fast-rotators, which infer a high sinusoidal-like
trend in the PDCSAP signal. This is why SHERLOCK PIPEline includes an automatic intense periodicities
detection and detrending during its preparation stage. This feature can be disabled with a flag.

### Main execution (run)
After the preparation stage, the SHERLOCK PIPEline will execute what we call `runs` iteratively:
* Several detrended fluxes with increasing window sizes will be extracted from the original 
PDCSAP light curve.
* For each detrended flux, the [TransitLeastSquares](https://github.com/hippke/tls) utility will 
be executed to find the most prominent transit.
* The best transit is chosen from all the ones found in the detrended fluxes. Here we have three 
different algorithms for the selection:
    * Basic: Selects the best transit signal only based in the highest SNR value.
    * Border-correct: Selects the best transit signal based in a corrected SNR value. This 
    correction is applied with a border-score factor, which is calculated from the found transits 
    which overlap or are very close to empty-measurements areas in the signal.
    * Quorum: Including the same correction from the border-correct algorithm, quorum will also
    increase the SNR values when several detrended fluxes 'agree' about their transit selection 
    (same ephemerids). The more detrended fluxes agree, the more SNR they get. This algorithm 
    can be slightly tuned by changing the stregth or weight of every detrend vote. It is currently 
    in testing stage and hasn't been used intensively.
* Measurements matching the chosen transit are masked in the original PDCSAP signal.

### Reporting
SHERLOCK PIPEline produces several information logs:
* Object report log: The entire log of the object run is written here.
* Most Promising Candidates log: A summary of the parameters of the best transits found for each
run is written at the end of the object execution.
* 

## Installation
The package can be installed from the PyPi repositories:

```python3 -m pip install sherlockpipe```

### Dependencies
All the needed dependencies should be included by your `pip` installation of SHERLOCK. 
These are the Python libraries which are <b>required</b> for <i>SHERLOCK</i> to be run:
* numpy: If you run into problems by installing numpy, it might be helpful to install 
the next packages (if you're under an Ubuntu distribution)
    * sudo apt-get install libblas-dev  liblapack-dev
    * sudo apt-get install gfortran
* cython (for lightkurve and pandas dependencies)
* pandas
* lightkurve
* transitleastsquares
* eleanor
* wotan
* matplotlib

The next libraries are <b>required</b> for <i>SHERLOCK Explorer</i> to be run:
* plotly
* colorama

## Testing
SHERLOCK Pipeline comes with a light automated tests suite which can be executed with:
```python3 -m unittest sherlock_tests.py```
This suite tests several points from the pipeline:
* The construction of the Sherlock object.
* The parameters setup of the Sherlock object.
* The provisioning of objects of interest files.
* Load and filtering of objects of interest.
* Different kind of short Sherlock executions.

In case you want to test the entire SHERLOCK PIPEline functionality we encourage you to
run some (or all) the [manual examples](https://github.com/franpoz/SHERLOCK/tree/master/examples).
If so, please read the instructions provided there to execute them.

## Integration
SHERLOCK integrates with several third party services. Some of them are listed below:
* TESS, Kepler and K2 databases through [Lightkurve](https://github.com/KeplerGO/lightkurve) and 
[ELEANOR](https://adina.feinste.in/eleanor/)
* MAST and Vizier catalogs through [Lightkurve](https://github.com/KeplerGO/lightkurve)
* [NASA Exoplanet Archive API](https://exoplanetarchive.ipac.caltech.edu/docs/program_interfaces.html)
* [TESS ExoFOP](https://exofop.ipac.caltech.edu/tess/view_toi.php)
