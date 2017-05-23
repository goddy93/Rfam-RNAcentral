#!/usr/bin/env python

"""
Script used to generate .sh job files
"""

# ............................IMPORT MODULES................................

import argparse
import os

# ..........................ARGUMENT PARSER.................................


def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument("fasta_dir",
                        metavar='fasta <dir>',
                        help="Directory with input fasta files")

    parser.add_argument("cmscan",
                        metavar='cmscan <path>',
                        help="Path to Infernal's cmscan")

    parser.add_argument("clanin",
                        metavar='clanin <file>',
                        help="Path locating Rfam.x.clanin file")

    parser.add_argument("cm",
                        metavar='cm <file>',
                        help="Path locating Rfam.cm file")

    parser.add_argument("shfiles_dir",
                        metavar='shfiles <dir>',
                        help="Directory where .sh files will be saved")

    parser.add_argument("tbl_dir",
                        metavar='tbl <dir>',
                        help="Directory where cmscan tables will be saved")

    parser.add_argument("out_dir",
                        metavar='out <dir>',
                        help="Directory where job's .out files will be saved")

    parser.add_argument("err_dir",
                        metavar='err <dir>',
                        help="Directory where job's .err files will be saved")

    return parser.parse_args()


# .............................FUNCTIONS....................................


def list_fasta(in_dir):
    """
    """
    fasta_files = []
    for filex in os.listdir(in_dir):
        if filex.endswith(".fasta"):
            fasta_files.append(os.path.splitext(filex)[0])

    return fasta_files


def generate_sh():
    """
    """
    args = argparser()

    fasta_files = list_fasta(args.fasta_dir)

    for filex in fasta_files:
        shfile = os.path.join(args.shfiles_dir, (filex + ".sh"))
        handle = open(shfile, "w")
        handle.write("#BSUB -q mpi-rh7\n")
        handle.write("#BSUB -J %s\n" % filex)
        handle.write("#BSUB -o %s\n" % os.path.join(args.out_dir, (filex + ".out")))
        handle.write("#BSUB -e %s\n" % os.path.join(args.err_dir, (filex + ".err")))
        handle.write("#BSUB -M 10000\n")
        handle.write('#BSUB -R "rusage[mem=10000]"\n')
        handle.write("#BSUB -n 4\n")
        handle.write("#BSUB -R span[hosts=1]\n")
        handle.write("#BSUB -a openmpi mpiexec\n")
        handle.write("#BSUB -mca btl ^openib\n")
        handle.write("#BSUB -np 4\n")
        handle.write("#BSUB -g /rnacrfam\n")
        handle.write("\n")
        handle.write("#PATHS\n")
        handle.write("input_path='%s'\n" % os.path.join(args.fasta_dir, (filex + ".fasta")))
        handle.write("tblout_path='%s'\n" % os.path.join(args.tbl_dir, (filex + ".tbl")))
        handle.write("cmscan='%s'\n" % args.cmscan)
        handle.write("clanin='%s'\n" % args.clanin)
        handle.write("cm='%s'\n" % args.cm)
        handle.write("\n")
        handle.write("#JOB\n")
        handle.write("$cmscan \\\n")
        handle.write("--tblout $tblout_path \\\n")
        handle.write("-Z 12063.99847 \\\n")
        handle.write("--noali \\\n")
        handle.write("--rfam \\\n")
        handle.write("--cut_ga \\\n")
        handle.write("--acc \\\n")
        handle.write("--nohmmonly \\\n")
        handle.write("--notextw \\\n")
        handle.write("--cpu 4 \\\n")
        handle.write("--fmt 2 \\\n")
        handle.write("--clanin $clanin_path \\\n")
        handle.write("$cm_path \\\n")
        handle.write("$input_path\n")
        handle.close()

# ..........................................................................

if __name__ == '__main__':
    generate_sh()
