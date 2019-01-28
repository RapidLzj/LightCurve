"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
from .utils import loadlist, datestr, logfile, conf


def imgproc(ini_file, sci_lst, bias_fits, flat_fits, sci_corr_suffix, out_path="", log=None):
    """

    :param ini_file:
    :param sci_lst: list file of scientific fits files
    :param bias_fits: merged flat fits files
    :param flat_fits: merged flat fits files
    :param sci_corr_suffix: suffix of corrected files
    :param out_path: path of out files, if provided, use this path
    :param log:
    :return: nothing
    """
    ini = conf(ini_file)
    lf = logfile(log, level=ini["log_level"])

    # load list
    lst = loadlist(sci_lst)
    nf = len(lst)
    outf = loadlist(sci_lst, middlefix=sci_corr_suffix, changepath=out_path)
    lf.show("{:03d} science files".format(nf), logfile.DEBUG)

    # load bias and flat
    lf.show("Loading Bias: {}".format(bias_fits), logfile.DEBUG)
    data_bias = fits.getdata(bias_fits)
    lf.show("Loading Flat: {}".format(flat_fits), logfile.DEBUG)
    data_flat = fits.getdata(flat_fits)

    # load images and process
    for f in range(nf):
        lf.show("Loading {:03d}/{:03d}: {:40s}".format(f + 1, nf, lst[f]), logfile.DEBUG)
        hdr = fits.getheader(lst[f])
        dat = (fits.getdata(lst[f]) - data_bias) / data_flat

        # add process time to header
        hdr.update(BZERO=0)
        hdr.append(('PROCTIME', datestr()))

        s = hdr.tostring()  # force check the header

        # save new fits
        new_hdu = fits.PrimaryHDU(header=hdr, data=dat)
        new_fits = fits.HDUList([new_hdu])
        new_fits.writeto(outf[f], overwrite=True)
        lf.show("Writing {:03d}/{:03d}: {:40s}".format(f + 1, nf, outf[f]), logfile.DEBUG)

    lf.close()
