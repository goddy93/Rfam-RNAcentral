#!/usr/bin/env python

"""
Parses Infernal's cmscan table output into .tsv file.
(Infernal 1.1.2 cmscan --tblout --fmt 2)

General usage:
python parser_cmscan.py <tbl>

More:
python parser_cmscan.py -h
"""

# ............................IMPORT MODULES................................

import argparse
import os
import pandas as pd

# ..........................ARGUMENT PARSER.................................


def argparser():
    """
    Argument parsing function, defines:

    tbl: required input table
    out: optional output location
    sig: True/False to keep only 'selected significant' hits
    """
    parser = argparse.ArgumentParser()

    # mandatory argument: input table
    parser.add_argument("tbl",
                        metavar='<cmscan_tbl>',
                        help="Infernal's cmscan table to parse.\
                              (As obtained from Infernal 1.1.2 cmscan\
                              --tblout --fmt 2)")

    # optional argument: output
    parser.add_argument("-o", "--out",
                        metavar='<file>',
                        help="Output file. By default saves it in the\
                              same path as input, same name, with .p.tsv\
                              extension.",
                        default="def_out",
                        type=str)

    # optional argument: significant
    parser.add_argument("-s", "--sig",
                        action="store_true",
                        help="If this option is selected, only the 'selected\
                              best hit' will be kept (where olp = * or ^).",
                        default=False)

    return parser.parse_args()

# .............................FUNCTIONS....................................


def read_tbl(cmscan_tbl):
    """
    Table parser using pandas.

    cmscan_tbl: Input infernal cmscan table
    returns df_tbl: pandas dataframe
    """

    # dictonary defining relation column-header from infernal tbl
    infernal_header = {0: "hit_num",
                       1: "rfam_id",
                       2: "rfam_acc",
                       3: "urs",
                       4: "accession",
                       5: "clan_acc",
                       6: "mdl",
                       7: "mdl_from",
                       8: "mdl_to",
                       9: "seq_from",
                       10: "seq_to",
                       11: "strand",
                       12: "trunc",
                       13: "pass",
                       14: "gc",
                       15: "bias",
                       16: "score",
                       17: "e_value",
                       18: "inc",
                       19: "olp"}

    # read with pandas df, variable space sep, only first 20 columns
    df_tbl = pd.read_table(cmscan_tbl,
                           comment="#",
                           engine="python",
                           sep=r"\s*|-\n",
                           header=None,
                           usecols=range(20))

    # use dictonary to assign column names
    df_tbl.columns = [infernal_header[column] for column in df_tbl]

    return df_tbl


def select_cols(cmscan_tbl):
    """
    Uses read_tbl() to parse infernal cmscan table,
    selects and reorders certain columns.

    cmscan_tbl: Input infernal cmscan table
    returns df_tbl: pandas dataframe
    """

    # use read_tbl() to make pandas df
    df_tbl = read_tbl(cmscan_tbl)

    # columns kept (see infernal_header)
    rel_columns = [3, 0, 2, 5, 7, 8, 9, 10, 11, 12, 16, 17, 18, 19]

    # select only those columns from df
    df_selected = df_tbl[rel_columns]

    return df_selected


def main():
    """
    Reads infernal cmscan table as specified in argument,
    selects and orders columns specified in select_cols(),
    keeps 'selected significant' rows if specified in argument,
    saves as tsv file in specified or default location.
    """

    # define out tsv, depending on given argument
    args = argparser()
    if args.out == "def_out":
        path = os.path.dirname(os.path.abspath(args.tbl))
        name = os.path.splitext(os.path.basename(args.tbl))[0]
        out_tsv = os.path.join(path, name) + ".p.tsv"
    else:
        out_tsv = args.out

    # use select_cols() to read table and keep only certain columns
    df_selected = select_cols(args.tbl)

    # keep 'significant selected' rows if specified in argument
    if args.sig:
        df_selected = df_selected[df_selected["olp"] != "="]

    # save file as tsv
    df_selected.to_csv(out_tsv, sep="\t", index=False)

# ..........................................................................

if __name__ == '__main__':
    main()
