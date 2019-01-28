"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
from .utils import loadlist, datestr, logfile


def imgproc(raw_path, out_path, sci_lst, bias_fits, flat_fits, sci_corr_suffix, log):
    """

    :param raw_path: path of raw files
    :param out_path: path of out files
    :param sci_lst: list file of scientific fits files
    :param bias_fits: merged flat fits files
    :param flat_fits: merged flat fits files
    :param sci_corr_suffix: suffix of corrected files
    :param log:
    :return: nothing
    """
    lf = logfile(log)

    # load list
    lst = loadlist(raw_path, sci_lst)
    nf = len(lst)
    outf = loadlist(out_path, sci_lst, middlefix=sci_corr_suffix)
    lf.show("{:03d} science files".format(nf), logfile.DEBUG)

    # load bias and flat
    lf.show("Loading Bias: {}".format(out_path + bias_fits), logfile.DEBUG)
    data_bias = fits.getdata(out_path + bias_fits)
    lf.show("Loading Flat: {}".format(out_path + flat_fits), logfile.DEBUG)
    data_flat = fits.getdata(out_path + flat_fits)

    # load images and process
    for f in range(nf):
        lf.show("Loading {:03d}/{:03d}: {:40s}".format(f + 1, nf, lst[f]), logfile.DEBUG)
        hdr = fits.getheader(lst[f])
        dat = (fits.getdata(lst[f]) - data_bias) / data_flat

        # add process time to header
        hdr.update(BZERO=0)
        hdr.append(('PROCTIME', datestr()))

        # save new fits
        new_fits = fits.HDUList([
            fits.PrimaryHDU(header=hdr, data=dat),
        ])
        new_fits.writeto(outf[f])
        lf.show("Writing {:03d}/{:03d}: {:40s}".format(f + 1, nf, outf[f]), logfile.DEBUG)

    lf.close()
