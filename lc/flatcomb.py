"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
from .utils import loadlist, datestr, logfile, conf


def flatcomb(ini_file, flat_lst, bias_fits, flat_fits, log=None):
    """
    Combine bias fits files
    :param ini_file:
    :param flat_lst: list file of bias fits files
    :param bias_fits: merged bias fits file
    :param flat_fits: merged flat fits file
    :param log:
    :return: nothing
    """
    ini = conf(ini_file)
    lf = logfile(log, level=ini["log_level"])

    # load list
    lst = loadlist(flat_lst)
    nf = len(lst)

    # get size of images
    hdr = fits.getheader(lst[0])
    nx = hdr['NAXIS1']
    ny = hdr['NAXIS2']
    lf.show("{:02d} flat files, image sizes {:4d}x{:4d}".format(nf, nx, ny), logfile.DEBUG)

    # load bias
    lf.show("Loading Bias: {}".format(bias_fits), logfile.DEBUG)
    data_bias = fits.getdata(bias_fits)

    # load images
    data_cube = np.empty((nf, ny, nx), dtype=np.float32)
    for f in range(nf):
        data_tmp = fits.getdata(lst[f]) - data_bias
        data_tmp_med = np.median(data_tmp)
        data_cube[f, :, :] = data_tmp / data_tmp_med
        lf.show("Loading {:02d}/{:02d}: {:40s} / Scaled by {:7.1f}".format(
            f + 1, nf, lst[f], data_tmp_med), logfile.DEBUG)

    # get median
    data_med = np.median(data_cube, axis=0)

    # add process time to header
    hdr.append(('COMBTIME', datestr()))
    s = hdr.tostring()  # force check the header

    # save new fits
    new_fits = fits.HDUList([
        fits.PrimaryHDU(header=hdr, data=data_med),
    ])
    new_fits.writeto(flat_fits)
    lf.show("Writing to: {}".format(flat_fits), logfile.DEBUG)

    lf.close()
