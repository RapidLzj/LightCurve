# -*- coding: utf-8 -*-
"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import astropy.io.fits as fits
from .utils import loadlist, datestr, logfile, conf, meanclip
from .cata import match


def offset(ini_file, sci_lst, catalog_suffix, offset_file, ref_id=0, out_path="", log=None):
    """
    photometry
    :param ini_file:
    :param sci_lst: list file of scientific fits files
    :param catalog_suffix: suffix of catalog files
    :param offset_file: offset file
    :param ref_id: the file chosen as the reference base
    :param out_path: path of out files
    :param log:
    :return:
    """
    ini = conf(ini_file)
    lf = logfile(log, level=ini["log_level"])

    # load list
    catf = loadlist(sci_lst, middlefix=catalog_suffix, changepath=out_path)
    nf = len(catf)
    lf.show("{:03d} catalog files".format(nf), logfile.DEBUG)

    # prepare an empty catalog cube
    xy_off = np.zeros((6, nf))
    n_off = np.zeros(nf, dtype=int)
    cat_ref = fits.getdata(catf[ref_id], 2)
    goodix = np.where(cat_ref[ini["se_err"]] < ini["good_err"])[0]
    x_ref = cat_ref[goodix][ini["se_x"]]
    y_ref = cat_ref[goodix][ini["se_y"]]
    m_ref = cat_ref[goodix][ini["se_mag"]]
    lf.show("Load {:03d}/{:03d}: N={:4d}/{:4d} Reference {}".format(
        ref_id, nf, len(goodix), len(cat_ref), catf[ref_id]), logfile.DEBUG)

    # load images and process
    for f in range(nf):
        if f != ref_id:
            cat_k = fits.getdata(catf[f], 2)
            goodix = np.where(cat_k[ini["se_err"]] < ini["good_err"])[0]
            x_k = cat_k[goodix][ini["se_x"]]
            y_k = cat_k[goodix][ini["se_y"]]
            m_k = cat_k[goodix][ini["se_mag"]]
            lim = ini["offset_max"]
            lf.show("Load {:3d}/{:3d}: N={:4d}/{:4d} {}".format(
                f, nf, len(goodix), len(cat_k), catf[f]), logfile.DEBUG)
            r = 0
            dxm, dxs = dym, dys = dmm, dms = drm, drs = 0.0, np.nan
            n = 0
            while lim > ini["offset_min"] and r < ini["offset_iter"]:
                r += 1
                ix_r, ix_k, dis = match(x_ref, y_ref, x_k + xy_off[0, f], y_k + xy_off[2, f], lim)
                n = len(ix_r)
                dx = x_ref[ix_r] - x_k[ix_k]
                dy = y_ref[ix_r] - y_k[ix_k]
                dm = m_ref[ix_r] - m_k[ix_k]
                dr = np.sqrt(dx * dx + dy * dy)
                dxm, dxs = meanclip(dx)
                dym, dys = meanclip(dy)
                dmm, dms = meanclip(dm)
                drm, drs = meanclip(dr)
                lf.show("  K={:1d} N={:4d} X={:7.3f}+-{:7.4f} Y={:7.3f}+-{:7.4f} R={:7.3f}+-{:7.4f} Mag={:7.3f}+-{:7.4f}".format(
                    r, n, dxm, dxs, dym, dys, drm, drs, dmm, dms), logfile.DEBUG)
                lim = drs * ini["offset_factor"]

                xy_off[:, f] = dxm, dxs, dym, dys, dmm, dms
                n_off[f] = n

    with open(offset_file, "w") as ff:
        for f in range(nf):
            ff.write("{:3d} {:40s} {:4d} {:7.3f} {:7.4f}  {:7.3f} {:7.4f}  {:7.3f} {:7.4f}\n".format(
                f, catf[f], n_off[f],
                xy_off[0, f], xy_off[1, f],
                xy_off[2, f], xy_off[3, f],
                xy_off[4, f], xy_off[5, f]
            ))
    lf.show("Report save to {}".format(offset_file), logfile.DEBUG)

    lf.close()
