import sys
import pandas as pd

TBL_PATH = sys.argv[1]
PAR_TBL_OUT = sys.argv[2]

# ----FUNCTIONS-----------------


def parsetbl_makematrix(infile):
    """
    Takes NHMMER table output (option --tblout) and makes
    matrix matching e-values from queries(vertical) with targets(horizontal).
    """
    df_tbl = pd.read_table(
        infile,
        comment="#",
        engine="python",
        sep=r"\s*|-\n",
        index_col=False,
        header=None,
        usecols=range(14)
        )
    # select relevant columns only
    df_tbl = df_tbl[[2, 0, 6, 7, 12, 13]]
    df_tbl.columns = ['query', 'target', 'alifrom', 'alito', 'e_value', 'score']
    # leave only rows with sig values
    df_tbl = df_tbl[df_tbl["e_value"] < 0.01]
    return df_tbl


# ----PROCESS-------------------
PARSED_TBL = parsetbl_makematrix(TBL_PATH)

# ----OUTPUT--------------------
# ...tables...
PARSED_TBL.to_csv(PAR_TBL_OUT, sep='\t', index=False)
