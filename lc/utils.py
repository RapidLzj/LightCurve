"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
from scipy import stats as st
import time
import os


def loadlist(listfile, suffix=".fits", middlefix="", changepath=""):
    """
    Load file list from list file, add base path and suffix to each filename
    :param listfile:
    :param suffix: if filename not ends with fits/fit/gz, then .fits will be append
    :param middlefix: add middle name if necessary
    :param changepath: if necessary, use new path
    :return: a list of filename
    """

    def get_ext(f):
        sp = os.path.splitext(f)
        base = sp[0]
        ext = sp[1]
        if ext == ".gz":
            spsp = os.path.splitext(base)
            ext = spsp[1] + ext
            base = spsp[0]
        return os.path.basename(base), ext

    if not suffix.startswith("."):
        suffix = "." + suffix

    lst = open(listfile, "r").readlines()
    lst = [f.strip() for f in lst]

    ori_path = [os.path.dirname(f) for f in lst]
    base_name = [get_ext(f)[0] for f in lst]
    ori_ext = [get_ext(f)[1] for f in lst]

    if suffix in ('.fit', '.fits', '.fit.gz', '.fits.gz', ):
        # lst = [f if f.endswith(('.fit', '.fits', '.gz', )) else f + suffix for f in lst]
        new_ext = [f if f in ('.fit', '.fits', '.fit.gz', '.fits.gz', ) else suffix for f in ori_ext]
    else:
        new_ext = [suffix for f in ori_ext]

    if middlefix != "":
        middlefix = "." + middlefix.strip(".")
        new_ext = [middlefix + f for f in new_ext]

    if changepath != "":
        new_path = [changepath for f in ori_path]
    else:
        new_path = [f + "/" for f in ori_path]

    new_lst = [p + f + e for p, f, e in zip(new_path, base_name, new_ext)]

    return new_lst


def datestr():
    """
    Generate a string of current time
    :return:
    """
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


class logfile(object):
    """
    Log file generator
    """

    # log level
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 90

    LEVEL_CODE={DEBUG:">", INFO:"|", WARNING:"!", ERROR:"X"}
    LEVEL_STR = {"DEBUG":DEBUG, "INFO":INFO, "WARNING":WARNING, "ERROR":ERROR}

    def __init__(self,
                 filename=None,
                 filemode="w",
                 filefmt="{time} {level} {message}",
                 scrfmt="{message}",
                 level=INFO):
        """
        Create a log object
        :param filename:
        :param filemode:
        :param filefmt:
        :param scrfmt:
        :param level:
        """
        self.filefmt = filefmt + "\n"
        self.scrfmt = scrfmt
        self.ff = (None if filename is None or filename == "" else
                   open(filename, filemode) )
        if type(level) in (int, float):
            self.level = level
        elif type(level) is str:
            self.level = self.LEVEL_STR[level.upper()]
        else:
            self.level = self.INFO

    def show(self, message, level=INFO):
        """
        Show message
        :param message:
        :param level:
        :return:
        """
        if level >= self.level:
            print(self.scrfmt.format(
                time=datestr(), level=self.LEVEL_CODE[level], message=message))
        if self.ff is not None:
            self.ff.write(self.filefmt.format(
                time=datestr(), level=self.LEVEL_CODE[level], message=message))

    def close(self):
        if self.ff is not None:
            self.ff.close()
            self.ff = None

    def __del__(self):
        self.close()


class conf(object):
    """
    Configuration file loader
    """

    def __init__(self, ini_filename):
        """
        Load ini file
        :param ini_filename:
        """
        self.data = {}
        self.load(ini_filename)

    @staticmethod
    def _check_type_(v):
        """
        transfer v to int or float if posible
        :param v:
        :return:
        """
        try:
            a = int(v)
        except ValueError:
            try:
                a = float(v)
            except ValueError:
                a = v
        return a

    def load(self, ini_filename):
        """
        Real loading operation
        :param ini_filename:
        :return:
        """
        lines = open(ini_filename, "r").readlines()
        for l in lines:
            p0 = l.find("=")
            p1 = l.find("#")
            k = l[:p0].strip()
            v = l[p0+1:p1].strip() if p1 > -1 else l[p0+1:].strip()
            v = self._check_type_(v)
            self.data[k] = v

    def __getitem__(self, item):
        """
        enable visit conf by conf["prop"]
        :param item:
        :return:
        """
        return self.data.get(item, None)


def meanclip(dat, nsigma=3.0):
    """
    Compute clipped median and sigma of dat
    :param dat: data, can be list, tuple or np array, 1-d or n-d,
                but if use checking, n-d array will be flattened
    :param nsigma: how many sigma used in clipping
    :return:
    """
    if len(dat) == 0:
        m, s = np.nan, np.nan
        ix = []
    elif len(dat) == 1:
        m, s = dat[0], np.nan
        ix = [0]
    else:
        c, l, u = st.sigmaclip(dat, nsigma, nsigma)
        m = np.nanmedian(c)
        s = np.nanstd(c)
    return m, s
