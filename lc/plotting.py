"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from .utils import meanclip


def plot_im_star(ini, img, x, y, mag, err, title, filename):
    """
    Plot observed image and overplot stars
    :param ini:
    :param img:
    :param x:
    :param y:
    :param mag:
    :param err:
    :param title:
    :param filename: file to save
    :return:
    """

    ny, nx = img.shape
    fig = plt.figure(figsize=(nx/50.0, ny/50.0))
    ax = fig.add_subplot(111)

    d_m, d_s = meanclip(img)
    ax.imshow(img, cmap="gray",
              vmin=d_m - d_s * ini["plot_img_lowsigma"],
              vmax=d_m + d_s * ini["plot_img_highsigma"])
    ax.set_xlim(0, nx)
    ax.set_ylim(0, ny)

    ix_g = np.where(err < 0.1)
    ix_b = np.where(err >= 0.1)
    ms = (25.0 - mag) * 5
    ms[mag > 25] = 1.0
    # ms[mag < 10] = 15.0
    ax.scatter(x[ix_g], y[ix_g], marker="o", s=ms[ix_g], c="", edgecolors="r")
    ax.scatter(x[ix_b], y[ix_b], marker="o", s=ms[ix_b], c="", edgecolors="c")

    ax.set_title(title)

    fig.savefig(filename)


def plot_magerr(ini, mag, err, title, filename):
    """
    Plot mag-err figure
    :param ini:
    :param mag:
    :param err:
    :param title:
    :param filename: file to save
    :return:
    """

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    ax.plot(mag, err, '.')
    ax.set_xlim(10, 25)
    ax.set_ylim(-0.001, 1.0)
    ax.set_xlabel("Mag (Inst)")
    ax.set_ylabel("Error")

    ax.set_title(title)

    fig.savefig(filename)
