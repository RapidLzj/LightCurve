"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


import numpy as np
import time


def loadlist(listfile, basepath="", suffix=".fits", middlefix=""):
    """
    Load file list from list file, add base path and suffix to each filename
    :param listfile:
    :param basepath:
    :param suffix: if filename not ends with fits/fit/gz, then .fits will be append
    :param middlefix: add middle name if necessary
    :return: a list of filename
    """
    if basepath != "" and not basepath.endswith("/"):
        basepath += "/"
    if not suffix.startswith("."):
        suffix = "." + suffix

    lst = open(listfile, "r").readlines()
    lst = [basepath + f.strip() for f in lst]
    lst = [f if f.endswith(('.fit', '.fits', '.gz', )) else f + suffix for f in lst]

    def ins_middle(fn, mf):
        p = fn.rfind(".fit")
        return fn[:p] + mf + fn[p:]

    if middlefix != "":
        middlefix = "." + middlefix.strip(".")
        lst = [ins_middle(f, middlefix) for f in lst]

    return lst


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
    LEVEL_CODE={DEBUG:">", INFO:"|", WARNING:"?", ERROR:"!"}

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
        self.level = level
        self.ff = (None if filename is None or filename == "" else
                   open(filename, filemode) )

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
            self.ff.write(self.scrfmt.format(
                time=datestr(), level=self.LEVEL_CODE[level], message=message))

    def close(self):
        if self.ff is not None:
            self.ff.close()
            self.ff = None

    def __del__(self):
        self.close()
