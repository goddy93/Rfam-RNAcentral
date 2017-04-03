import sys
import pandas as pd

TBL_PATH = sys.argv[1]
SELECT_TBL_OUT = sys.argv[2]

# ----FUNCTIONS-----------------

# read parsed table
df_tbl = pd.read_table(
    TBL_PATH)

f = open(SELECT_TBL_OUT, 'w')
f.write("queryt  target  alifrom  alito  e_value  score\n")
f.close()


# write only those with more than one diff target
for urs in set(df_tbl["query"]):
    if len(df_tbl[df_tbl["query"] == urs]) != 1:
        if set([urs]) != set((df_tbl[df_tbl["query"] == urs])["target"]):
            f = open(SELECT_TBL_OUT, 'a')
            a = df_tbl[df_tbl["query"] == urs].to_string(header=False, index=False) + "\n"
            f.write(a)
            f.close()
