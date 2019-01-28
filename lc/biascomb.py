"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
from .utils import loadlist, datestr, logfile, conf


def biascomb(ini_file, bias_lst, bias_fits, log=None):
    """
    Combine bias fits files
    :param ini_file:
    :param bias_lst: list file of bias fits files
    :param bias_fits: merged bias fits files
    :param log: log
    :return: nothing
    """
    ini = conf(ini_file)
    lf = logfile(log, level=ini["log_level"])

    # load list
    lst = loadlist(bias_lst)
    nf = len(lst)

    # get size of images
    hdr = fits.getheader(lst[0])
    nx = hdr['NAXIS1']
    ny = hdr['NAXIS2']
    lf.show("{:02d} bias files, image sizes {:4d}x{:4d}".format(nf, nx, ny), logfile.DEBUG)

    # load images
    data_cube = np.empty((nf, ny, nx), dtype=np.float32)
    for f in range(nf):
        lf.show("Loading {:02d}/{:02d}: {:40s}".format(f+1, nf, lst[f]), logfile.DEBUG)
        data_cube[f, :, :] = fits.getdata(lst[f])

    # get median
    data_med = np.median(data_cube, axis=0)

    # add process time to header
    hdr.append(('COMBTIME', datestr()))
    s = hdr.tostring()  # force check the header

    # save new fits
    new_fits = fits.HDUList([
        fits.PrimaryHDU(header=hdr, data=data_med),
    ])
    new_fits.writeto(bias_fits, overwrite=True)
    lf.show("Writing to: {}".format(bias_fits), logfile.DEBUG)

    lf.close()
