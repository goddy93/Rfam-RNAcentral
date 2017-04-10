import shutil
import sys
import pandas as pd

TBL_PATH = sys.argv[1]
ALI_PATH = sys.argv[2]
SEL_ALI_PATH = sys.argv[3]

# read parsed table
DF_BESTMARK = pd.read_table(
    TBL_PATH)

# select unmarked sequences to delete
TO_DEL = DF_BESTMARK[DF_BESTMARK["selected"] != "*"]
# select seq_names to delete lines, in and out file names
for urs in set(TO_DEL["query"]):
    bad_seqs = TO_DEL[TO_DEL["query"] == urs]["seq_name"].tolist()
    ali_file = ALI_PATH + urs + ".sto"
    clean_ali_file = SEL_ALI_PATH + urs + ".cl.sto"
    # process to delete lines with bad seqs
    with open(ali_file) as oldfile, open(clean_ali_file, 'w') as newfile:
        for line in oldfile:
            if not any(seq in line for seq in bad_seqs):
                newfile.write(line)

# select files that need no modifications to copy
TO_MOVE = set(DF_BESTMARK["query"]) - set(TO_DEL["query"])
for urs in TO_MOVE:
    move_from = ALI_PATH + urs + ".sto"
    move_to = SEL_ALI_PATH + urs + ".sto"
    shutil.copy(move_from, move_to)
