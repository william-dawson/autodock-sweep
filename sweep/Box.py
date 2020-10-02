"""
Things related to the box class.
"""


class Box:
    """
    An object representing a 3 dimensional box.
    """
    def __init__(self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    @property
    def xlen(self):
        return self.xmax - self.xmin

    @property
    def ylen(self):
        return self.ymax - self.ymin

    @property
    def zlen(self):
        return self.zmax - self.zmin

    @property
    def center(self):
        return [self.xmin + self.xlen/2.0,
                self.ymin + self.ylen/2.0,
                self.zmin + self.zlen/2.0]


def get_box(fname):
    """
    Reads in a pdb file and creates a bounding box.

    Args:
        fname (str): the name of the pdb file.

    Returns:
        (Box): the bounding box.
    """
    with open(fname) as ifile:
        xvals = []
        yvals = []
        zvals = []
        for line in ifile:
            try:  # See if there is an atom on this line
                if line[:4] == "ATOM" or line[:6] == "HETATM":
                    xvals += [float(line[30:38])]
                    yvals += [float(line[38:46])]
                    zvals += [float(line[46:54])]
            except IndexError:
                continue
        return Box(min(xvals), max(xvals),
                   min(yvals), max(yvals),
                   min(zvals), max(zvals))