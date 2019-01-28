"""
    201901, Dr. Jie Zheng, Beijing & Xinglong, NAOC
    Light_Curve
"""


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

