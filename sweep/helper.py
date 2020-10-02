"""
Helper routines.
"""


def get_parameters(argv):
    """
    Reads in the input parameters.
    """
    from yaml import load, SafeLoader

    # Get the input file name.
    try:
        infile = argv[1]
    except IndexError:
        raise Exception("Requires the input file as the first parameter.")

    # Read.
    with open(infile) as ifile:
        param = load(ifile, Loader=SafeLoader)

    # Verify the input file.
    for k in ["receptor", "ligand", "box_size", "cpu", "work_dir"]:
        if k not in param:
            raise Exception("Input file needs to contains " + k)

    return param


def get_energies(fname):
    """
    Read in the energies from a logfile.

    Args:
        fname (str): the name of the logfile.

    Returns:
        (list): a list of energies.
    """
    ene = []
    with open(fname) as ifile:
        for line in ifile:
            split = line.split()
            if len(split) > 0 and split[0] == "mode":
                break
        next(ifile)
        next(ifile)
        for line in ifile:
            split = line.split()
            if split[0] == "Writing":
                break
            ene.append(float(split[1]))
    return ene
