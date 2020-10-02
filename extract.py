"""
Automatically extract the ligand poses from the calculation that have an
energy lower than some given threshold.

Usage:
    python plot.py param.yaml threshold

The input parameters should be specified in a yaml file, see the example
folder for details. Threshold is some (likely negative) number, for example
-100.
"""


if __name__ == "__main__":
    from sys import argv
    from yaml import load, SafeLoader
    from sweep.helper import get_parameters, get_energies
    from os.path import join, basename

    # Read in the parameters.
    param = get_parameters(argv)
    try:
        threshold = float(argv[2])
    except IndexError:
        raise Exception("Specify a second parameter: threshold.")

    # Read in the list of logfiles.
    with open(join(param["work_dir"], "data.yaml"), "r") as ifile:
        logs = load(ifile, Loader=SafeLoader)

    # Extract the energies.
    energies = {}
    for lg in logs:
        try:
            energies[basename(lg)] = get_energies(lg)
        except StopIteration:
            continue

    # Filter
    results = []
    for lg, ene in energies.items():
        for i, val in enumerate(ene):
            if val < threshold:
                results.append([lg.replace(".log", ""), i, val])

    # Print
    print("File\t"+"Index\t"+"Energy")
    print("-----------------------")
    for r in sorted(results, key=lambda x: x[0]):
        print("\t".join([str(x) for x in r]))
