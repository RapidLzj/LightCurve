"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
import os
from .utils import loadlist, datestr, logfile, conf
from .plotting import plot_im_star, plot_magerr


def phot(ini_file, sci_lst, sci_corr_suffix, catalog_suffix, out_path="", log=None):
    """
    photometry
    :param ini_file:
    :param sci_lst: list file of scientific fits files
    :param sci_corr_suffix: suffix of corrected files
    :param catalog_suffix: suffix of catalog files
    :param out_path: path of out files
    :param log:
    :return:
    """
    ini = conf(ini_file)
    lf = logfile(log, level=ini["log_level"])

    # load list
    scif = loadlist(sci_lst, middlefix=sci_corr_suffix, changepath=out_path)
    catf = loadlist(sci_lst, middlefix=catalog_suffix, changepath=out_path)
    magerr = loadlist(sci_lst, suffix="png", middlefix="magerr", changepath=out_path)
    imgplt = loadlist(sci_lst, suffix="png", middlefix="phot", changepath=out_path)
    basename = [os.path.basename(f) for f in catf]
    nf = len(scif)
    lf.show("{:03d} science files".format(nf), logfile.DEBUG)

    se_cmd_fmt = "sex {img} -CATALOG_NAME {cat}"

    # load images and process
    for f in range(nf):
        lf.show("SE on {:03d}/{:03d}: {:40s}".format(f + 1, nf, scif[f]), logfile.DEBUG)
        se_cmd = se_cmd_fmt.format(img=scif[f], cat=catf[f])
        lf.show("    " + se_cmd)
        os.system(se_cmd)

        img = fits.getdata(scif[f])
        cat = fits.getdata(catf[f], 2)

        plot_im_star(ini, img, cat[ini["se_x"]], cat[ini["se_y"]],
                     cat[ini["se_mag"]], cat[ini["se_err"]], basename[f], imgplt[f])
        plot_magerr(ini, cat[ini["se_mag"]], cat[ini["se_err"]], basename[f], magerr[f])

    lf.close()
