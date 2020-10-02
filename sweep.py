"""
Automatically generate input parameters for the auto-dock vina program such
that the entire protein is considered.

Usage:
    python sweep.py param.yaml

The input parameters should be specified in a yaml file, see the example
folder for details.
"""


def create_boxes(sys, box_size):
    """
    Create a list of boxes that covers the full system box.

    Arg:
        sys (Box): the bounding box of the system.
        box_size (list): the size of the boxes to create.
    """
    from numpy import linspace
    from math import ceil

    xspace = linspace(sys.xmin, sys.xmax, ceil((sys.xmax - sys.xmin) /
                      (box_size[0]/2)))
    yspace = linspace(sys.ymin, sys.ymax, ceil((sys.ymax - sys.ymin) /
                      (box_size[1]/2)))
    zspace = linspace(sys.zmin, sys.zmax, ceil((sys.zmax - sys.zmin) /
                      (box_size[2]/2)))

    blist = []
    for i, x in enumerate(xspace):
        for j, y in enumerate(yspace):
            for k, z in enumerate(zspace):
                xmin = x - box_size[0]/2
                xmax = x + box_size[0]/2
                ymin = y - box_size[1]/2
                ymax = y + box_size[1]/2
                zmin = z - box_size[2]/2
                zmax = z + box_size[2]/2

                blist.append(Box(xmin, xmax, ymin, ymax, zmin, zmax))

    return blist


def generate(name, box, param):
    """
    Generate an input file with a given box.

    Returns:
        (str): the name of the file created.
    """
    from os.path import exists, join, basename
    from os import mkdir

    # Create the config file
    fname = join(param["work_dir"], name+".conf")
    lname = join(param["work_dir"], name+".log")
    with open(fname, "w") as ofile:
        ofile.write("out = " + name + ".pdbqt\n")
        ofile.write("log = " + name + ".log\n")

        ofile.write("receptor = " + basename(param["receptor"]) + "\n")
        ofile.write("ligand = " + basename(param["ligand"]) + "\n")

        ofile.write("center_x = " + str(box.center[0]) + "\n")
        ofile.write("center_y = " + str(box.center[1]) + "\n")
        ofile.write("center_z = " + str(box.center[2]) + "\n")

        ofile.write("size_x = " + str(box.xlen) + "\n")
        ofile.write("size_y = " + str(box.ylen) + "\n")
        ofile.write("size_z = " + str(box.zlen) + "\n")

        if "vina" in param:
            for k, v in param["vina"].items():
                ofile.write(k + " = " + str(v) + "\n")

    return fname, lname


def validate_log(fname):
    """
    Validates that a calculation has competed.
    """
    from os.path import exists
    if not exists(fname):
        return False
    with open(fname) as ifile:
        for line in ifile:
            if "Writing output ... done." in line:
                return True
    return False


if __name__ == "__main__":
    from sys import argv
    from os.path import exists, join, basename
    from os import mkdir, system
    from shutil import copyfile
    from yaml import dump
    from sweep.helper import get_parameters
    from sweep.Box import get_box, Box

    # Read in the parameters.
    param = get_parameters(argv)

    # Read boxes.
    protein_box = get_box(param["receptor"])
    ligand_box = get_box(param["ligand"])

    # Combine the two boxes.
    system_box = Box(min(protein_box.xmin, ligand_box.xmin),
                     max(protein_box.xmax, ligand_box.xmax),
                     min(protein_box.ymin, ligand_box.ymin),
                     max(protein_box.ymax, ligand_box.ymax),
                     min(protein_box.zmin, ligand_box.zmin),
                     max(protein_box.zmax, ligand_box.zmax))

    # Copy the input geometries to the work directory.
    if not exists(join(param["work_dir"])):
        mkdir(param["work_dir"])
    copyfile(param["receptor"], join(param["work_dir"],
             basename(param["receptor"])))
    copyfile(param["ligand"], join(param["work_dir"],
             basename(param["ligand"])))

    # Create all the boxes we will generate.
    box_list = create_boxes(system_box, param["box_size"])

    # Generate the input files.
    files = []
    logs = []
    for i, box in enumerate(box_list):
        f, lg = generate(str(i), box, param)
        files.append(f)
        logs.append(lg)

    # Write the logfile names into a cache datastructure.
    with open(join(param["work_dir"], "data.yaml"), "w") as ofile:
        dump(logs, ofile)

    # Run autodock.
    for f, lg in zip(files, logs):
        if validate_log(lg):
            continue
        cmd = "cd " + param["work_dir"] + " ; vina --config " + basename(f)
        print(cmd)
        system(cmd)
