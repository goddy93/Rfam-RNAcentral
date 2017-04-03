import sys
import pandas as pd

TBL_PATH = sys.argv[1]
BESTMARK_OUT = sys.argv[2]
COUNT_OUT = "./03.c.count.out"

# read parsed table
df_select = pd.read_table(
    TBL_PATH,
    delim_whitespace=True)

# add columns with length and sequence name
seqalen = abs(df_select["alifrom"] - df_select["alito"])
df_select["seqalen"] = seqalen
df_select["seq_name"] = df_select["target"] + "/" + df_select["alifrom"].map(str) + "-" + df_select["alito"].map(str)
df_select["selected"] = None

# select best per query
m = 1
for i in set(df_select["query"]):
    # -- all sequences related to a query
    allseqs = df_select[df_select["query"] == i]["target"]
    # -- if the size and the set are the same: no repeats, mark all as selected
    if len(allseqs) == len(set(allseqs)):
        df_select.set_value((allseqs.index.tolist()), "selected", "*")
    # -- if they are different, there are repeats: group repeats and mark longest
    else:
        for j in set(df_select[df_select["query"] == i]["target"]):
            repeats = df_select[(df_select["query"] == i) & (df_select["target"] == j)]
            nonred = repeats.nlargest(1, "seqalen")
            df_select.set_value((nonred.index.tolist()[0]), "selected", "*")
    out = "query %d of %d \n" % (m, len(set(df_select["query"])))
    f = open(COUNT_OUT, 'a')
    f.write(out)
    f.close()
    m = m + 1

# cleanup
df_bestmark = df_select[["query", "seq_name", "selected"]]

# ----OUTPUT--------------------
df_bestmark.to_csv(BESTMARK_OUT, sep='\t', index=False)
