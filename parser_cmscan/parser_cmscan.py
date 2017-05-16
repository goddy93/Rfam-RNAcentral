import sys
import pandas as pd

CMSCAN_TBL = sys.argv[1]
PARSED_OUT = sys.argv[2]

# read table
DF_CMSCANTBL = pd.read_table(CMSCAN_TBL,
                             comment="#",
                             engine="python",
                             sep="\s*|-\n",
                             header=None,
                             usecols=range(20)
                             )
# infernal tbl output headers
INFERNAL_TBLHEAD = {0: "hit_num",
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
                    19: "olp"
                    }

# select relevant columns, name them
REL_COLUMNS = [3, 0, 2, 5, 7, 8, 9, 10, 11, 12, 16, 17, 18, 19]
DF_CMSCANTBL = DF_CMSCANTBL[REL_COLUMNS]
DF_CMSCANTBL.columns = [INFERNAL_TBLHEAD[column] for column in REL_COLUMNS]

# output
DF_CMSCANTBL.to_csv(PARSED_OUT, sep='\t', index=False)
