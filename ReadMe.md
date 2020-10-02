# Autovina Sweep

The python scripts here help simplify an exhaustive docking procedure using
autodock vina. This will automatically generate a large set of calculations
with boxes covering every inch of the unit cell (including buffer) so that
you can search for off-target docking without having to identify other
pockets, or pay the price of a large box.

There are three scripts included in this project that should be run one
after another. The first one is `sweep.py` which generates input files and
then runs autodock vina on each of those files. The second is `plot.py` which
creates a plot of the scores generated. This will help you pick a cutoff
for the final script `extract.py` which will extract all structures with
scores above a desired threshold.

This script uses a very naive algorithm of simply cutting up the unit cell
into evenly spaced blocks. Half the dimension of each block in each direction
is used as a buffer.

## Workflow

Thus the typical workflow is:
```
python sweep.py input.yaml
python plot.py input.yaml
# examine the plot to pick a threshold, let's say -100
python extract.py input.yaml -100
```
In each case we have passed a file `input.yaml` which includes the
configuration you would like. This file might look like this:
```
# List the names of the files to consider.
receptor: protein.pdbqt
ligand: ligand.pdbqt
# The size of the box to generate (x, y, z).
box_size: [20, 20, 20]
# The directory to put all the generated data.
work_dir: work
# Other parameters for vina.
cpu: 1
```

This program automatically runs the `vina` command, and assumes that `vina`
is on the path.
