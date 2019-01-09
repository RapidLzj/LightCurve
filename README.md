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

+ numpy
+ astropy
+ photutils
+ matplotlib

## Steps

### Bias mergeing

A list of bias files should be provided, and then a merged bias fits file will be generated.
A median function is used to evaluated the bias of each pixel.

### Flat mergeing

A list of flat files and the merged bias fits file should be provided, and then a merged flat fits file will be generated.
We normalize each flat image with its median, and then use the median function to merge the flat.

### Science image correction

Correct science fits with the given merged bias and flat files.
For each pixel, bias is substracted, and then the flat if divided.

### Source detection and flux extraction

Use SExtractor or photutils package to detect sources and evaluate their flux.
Stars with $5-\sigma$ over background are detected and their flux measured with aperture photometry with 3-FWHM diameter.

### Alignment of images

Find pointing offset between images, compared with the specified image.
A big enough initial offset tolerance will be used in matching stars between images.
And then the tolerance will be shrinked, until the error is lower enough for target identifying.

### Differential flux calibration

Differential Calibrate the flux of target (giving x & y) with reference stars (also x & y).

A global flux offset between each image and the reference image is measured, 
using the 3 sigma clipped median of offsets of all matched stars.
A local flux offset is also measured by the given refernce stars.

Then the flux changing of the target star by the two offsets are both extracted.
Finally the differential flux report is generated.

### Plotting

Plotting the light curve

## Usage

### Prepare file lists

Use `ls` or other approachs to create a fits file list.
Each line in the list is a filename, without path.
The common part of path will be provided with a parameter.

### Import the package

```python
import lzj_lightcurve as lc
```

### Prepare necessary variables, or use the values later directly

```python
# initial variables
raw_path        = 'raw/'       # path for raw files
out_path        = 'red/'       # path for output files
bias_lst        = 'bias.lst'   # list file name of bias files
bias_fits       = 'bias.fits'  # merged bias file name
flat_lst        = 'flat.lst'   # list file name of flat files
flat_fits       = 'flat.fits'  # merged flat file name
sci_lst         = 'sci.lst'    # list file name of scientific fits files
sci_corr_suffix = 'corr'       # suffix added to corrected fits files
catalog_suffix  = 'cat'        # output catalog suffix
diff_file       = 'diff.txt'   # the output differential calibration flux (mag) file name
curve_fig       = 'diff.png'   # differential light curve figure (pdf/eps/png)
```

### Bias and flat merging

```python
lc.mergebias(
    raw_path,    # path of raw files
    out_path,    # path of out files
    bias_lst,    # list file of bias fits files
    bias_fits,   # merged bias fits files
)
```

```python
lc.mergeflat(
    raw_path,    # path of raw files
    out_path,    # path of out files
    flat_lst,    # list file of flat fits files
    bias_fits,   # merged bias fits files
    flat_fits,   # merged flat fits files
)
```

### Correct scientific images

```python
lc.corr(
    raw_path,         # path of raw files
    out_path,         # path of out files
    sci_lst,          # list file of scientific fits files
    bias_fits,        # merged flat fits files
    flat_fits,        # merged flat fits files
    sci_corr_suffix,  # suffix of corrected files
)
```

### Phtometry

```python
lc.phot(
    out_path,          # path of out files
    sci_lst,           # list file of scientific fits files
    sci_corr_suffix,   # suffix of corrected files
    catalog_suffix,    # suffix of catalog files
)
```

### Alignment

```python
offset = lc.align(
    out_path,        # path of out files
    sci_lst,         # list file of scientific fits files
    catalog_suffix,  # suffix of corrected files
    ref_img_id,      # reference image id, default is 0
)
```

### Differential calibration

```python
lc.cali(
    out_path,        # path of out files
    sci_lst,         # list file of scientific fits files
    catalog_suffix,  # suffix of catalog files
    (x, y),          # x/y coordination of target star
    [(x1, y1), (x2, y2), ...],  # list of x/y coordinations of reference stars
    (xc, yc),        # x/y coordination of check star
    diff_file,       # the output differential calibration flux (mag) file name 
    offset,          # offset between iamges
)
```

### Plotting

```python
lc.curve(
    outpath,    # path of out files
    diff_file,  # the output differential calibration flux (mag) file name
    curve_fig,  # differential light curve figure (pdf/eps/png)
)
```
