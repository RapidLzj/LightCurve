# Light Curve
Photometric correction and photometry, light curve plotting

## Code Author
Dr. Jie Zheng (National Astronomical Observatories (NAOC), CAS) @rapidlzj

## Purpose

This is a pipeline to extract light curve from a serial of fits images.

This pipeline will merge bias and flat, correct science images,
and then extract stars and their magnitudes,
finally it can provide a light curve.

## Package depenency

Install packages by pip or conda, or other package management command

+ astropy
+ photutils
+ numpy
+ matplotlib

## Steps

### Bias mergeing

A list of bias files should be provided, and then a merged bias fits file will be generated.

### Flat mergeing

A list of flat files and the merged bias fits file should be provided, and then a merged flat fits file will be generated.

### Science image correction

Correct science fits with the given merged bias and flat files.

### Source detection and flux extraction

Use SExtractor or photutils package to detect sources and evaluate their flux.

### Differential flux calibration

Differential Calibrate the flux of target (giving x & y) with reference stars (also x & y).

Output a Differential flux report

### Plotting

Plotting the light curve

## Usage

```python
import lzj_lightcurve as lc

raw_path = 'raw/'  # path for raw files
out_path = 'red/'  # path for output files
bias_lst = 'bias.lst'  # list file name of bias files
bias_fits = 'bias.fits'  # merged bias file name
flat_lst = 'flat.lst'  # list file name of flat files
flat_fits = 'flat.fits'  # merged flat file name
sci_lst = 'sci.lst'  # list file name of scientific fits files
sci_corr_suffix = 'corr'  # suffix added to corrected fits files
catalog_suffix = 'cat'  # output catalog suffix
diff_file = 'diff_result.cat.txt'  # the output differential calibration flux (mag) file name
curve_fig = 'diff.png'  # differential light curve figure (pdf/eps/png)
```

### Bias and flat merging

```python
lc.mergebias(
    raw_path,  # path of raw files
    out_path,  # path of out files
    bias_lst,  # list file of bias fits files
    bias_fits, # merged bias fits files
)

lc.mergeflat(
    raw_path,  # path of raw files
    out_path,  # path of out files
    flat_lst, 
    bias_fits, # merged bias fits files
    flat_fits, # merged flat fits files
)
```

### Correct scientific images

```python
lc.corr(
    raw_path,  # path of raw files
    out_path,  # path of out files
    sci_lst,   # list file of scientific fits files
    bias_fits, # merged flat fits files
    flat_fits, # merged flat fits files
    sci_corr_suffix,  # suffix of corrected files
)
```

### Phtometry

```python
lc.phot(
    out_path,  # path of out files
    sci_lst,   # list file of scientific fits files
    sci_corr_suffix,   # suffix of corrected files
    catalog_suffix,    # suffix of catalog files
)
```

### Differential calibration

```python
lc.cali(
    out_path,  # path of out files
    sci_lst,   # list file of scientific fits files
    catalog_suffix,   # suffix of catalog files
    (x, y),  # x/y coordination of target star
    [(x1, y1), (x2, y2), ...],  # list of x/y coordinations of reference stars
    (xc, yc),   # x/y coordination of check star
    diff_file,  # the output differential calibration flux (mag) file name 
)
```

### Plotting

```python
lc.curve(
    outpath,  # path of out files
    diff_file,  # the output differential calibration flux (mag) file name
    curve_fig,  # differential light curve figure (pdf/eps/png)
)
```
