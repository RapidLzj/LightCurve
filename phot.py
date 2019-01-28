"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
import os
from .utils import loadlist, datestr, logfile


def phot(ini_file, out_path, sci_lst, sci_corr_suffix, catalog_suffix, log=None):
    """
    photometry
    :param ini_file:
    :param out_path: path of out files
    :param sci_lst: list file of scientific fits files
    :param sci_corr_suffix: suffix of corrected files
    :param catalog_suffix: suffix of catalog files
    :param log:
    :return:
    """
    lf = logfile(log)
    ini = conf(ini_file)

    # load list
    scif = loadlist(out_path, sci_lst, middlefix=sci_corr_suffix)
    catf = loadlist(out_path, sci_lst, middlefix=catalog_suffix)
    nf = len(scif)
    lf.show("{:03d} science files".format(nf), logfile.DEBUG)

    se_cmd_fmt = "sex {img} -CATALOG_NAME {cat}"

    # load images and process
    for f in range(nf):
        lf.show("SE on {:03d}/{:03d}: {:40s}".format(f + 1, nf, scif[f]), logfile.DEBUG)
        se_cmd = se_cmd_fmt.format(img=scif[f], cat=catf[f])
        lf.show("    " + se_cmd)
        os.system(se_cmd)

    lf.close()
