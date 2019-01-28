# -*- coding: utf-8 -*-
"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
from .utils import loadlist, datestr, logfile
from .cata import match
from .conf import conf


def offset(ini_file, out_path, sci_lst, catalog_suffix, offset_file, base_id=0, log=None):
    """
    photometry
    :param ini_file:
    :param out_path: path of out files
    :param sci_lst: list file of scientific fits files
    :param catalog_suffix: suffix of catalog files
    :param offset_file: offset file
    :param base_id: the file chosen as the reference base
    :param log:
    :return:
    """
    lf = logfile(log)
    ini = conf(ini_file)

    # load list
    catf = loadlist(out_path, sci_lst, middlefix=catalog_suffix)
    nf = len(catf)
    lf.show("{:03d} catalog files".format(nf), logfile.DEBUG)

    # prepare an empty catalog cube
    xy_off = np.zeros((2, nf))
    cat_ref = fits.getdata(catf[base_id], 2)
    x_ref = cat_ref["x_image_dbl"]
    y_ref = cat_ref["y_image_dbl"]

    # load images and process
    for f in range(nf):
        if f != base_id:
            cat_k = fits.getdata(catf[f], 2)
            x_k = cat_k["x_image_dbl"]
            y_k = cat_k["y_image_dbl"]
            lim = 50.0
            for r in (50.0, 10.0, 5.0, 2.5):
                ix_r, ix_k, dis = match(
                    x_ref, y_ref, x_k + xy_off[0, f], y_k + xy_off[1, f], lim)
                dx = np.median(x_ref[ix_r] - x_k[ix_k])
                dy = np.median(y_ref[ix_r] - y_k[ix_k])
                xy_off[:, f] = dx, dy
            lf.show("Offset of {:03d}/{:03d}: {:40s} = {:6.2f} {:6.2f}".format(
                f + 1, nf, catf[f], dx, dy), logfile.DEBUG)

    with open(offset_file, "w") as ff:
        for f in range(nf):
            ff.write("{:3d} {:40s} {:6.2f} {:6.2f}\n".format(
                f, catf[f], xy_off[0, f], xy_off[1, f]
            ))
    lf.show("Report save to {}".format(offset_file), logfile.DEBUG)

    lf.close()
