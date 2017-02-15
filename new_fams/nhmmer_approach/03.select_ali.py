import os
import sys
import pandas as pd
import networkx as nx

TBL_PATH = "/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_clust/test402/402.tbl"
ALI_PATH = "/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_clust/test402/402/"
ALISTAT_PATH = "/Users/nquinones/Documents/infernal-1.1.2/easel/miniapps/esl-alistat"
OUTFILE = "./sample.tsv"

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
    df_tbl = df_tbl[[0, 2, 12, 13]]
    df_tbl.columns = ['target', 'query', 'e_value', 'score']
    # make dictonary, unique values in query as keys, fill with value
    matrix_dic = {}
    q_keys = set(df_tbl["query"])
    for item in q_keys:
        matrix_dic[item] = {}
    for index, row in df_tbl.iterrows():
        matrix_dic[row["query"]][row["target"]] = row["e_value"]
    # make matrix
    matrix = pd.DataFrame(matrix_dic).T.fillna("None")
    return matrix


def make_boolmatrix(matrix):
    """
    Takes matrix from function *parsetbl_makematrix(infile)*
    and changes significant (<0.05) to 1
    and non-significant (>0.05) and "None" to 0
    """
    matrix_bool = matrix.copy()
    matrix_bool[matrix_bool >= 0.05] = "None"
    matrix_bool[matrix_bool < 0.05] = int(1)
    matrix_bool.replace("None", int(0), inplace=True)
    return matrix_bool


def make_groups(matrix_bool):
    """
    Takes binary square matrix from function *make_boolmatrix(matrix)*
    and computes connected components with networkx.
    Returns list with sublists of connected rows (queries)
    """
    # make matrix readable for networkx
    matrix_bool_np = matrix_bool.as_matrix()
    # group with networkx
    graph = nx.from_numpy_matrix(matrix_bool_np)
    groups = list(nx.connected_components(graph))
    # make list of sets into list of integers
    groups_list = []
    for i in range(0, len(groups)):
        groups_list.append(list(groups[i]))
    # dictonary relating row number to URS
    line_query_dict = {}
    for i in range(0, len(matrix_bool)):
        line_query_dict[i] = matrix_bool.index[i]
    # replace row numbers with URS
    groups_withurs = []
    for i in groups_list:
        list_temp = []
        for j in i:
            list_temp.append(line_query_dict[j])
        groups_withurs.append(list_temp)
    return groups_withurs


def make_alistatsum(nonred_list):
    """
    Takes list of URSs from function *make_groups(matrix_bool)*
    that should point to .sto files (in *ALI_PATH*), and passes
    them through easel's alifold to return table with
    statistics per alignment.
    """
    info_table = pd.DataFrame()
    for i in range(0, len(nonred_list)):
        for j in nonred_list[i]:
            # run alstat
            ex_string = ALISTAT_PATH + " --rna " + ALI_PATH + "%s.sto" % j
            b = os.popen(ex_string).readlines()
            values = []
            # extract last element which corresponds to value
            for line in b:
                values.append(line.split()[-1])
            num_seq = int(values[2])
            alen = float(values[3])
            diff = float(values[6]) - float(values[5])
            avlen = float(values[7])
            lenalen_ratio = avlen / alen
            avid = int(values[8].strip("%"))
            table_line = [i,
                          j,
                          num_seq,
                          alen,
                          diff,
                          avlen,
                          lenalen_ratio,
                          avid]
            info_table = info_table.append([table_line])
    info_table.columns = ["group",
                          "urs",
                          "num_seq",
                          "alen",
                          "diff",
                          "avlen",
                          "lenalen_ratio",
                          "avid"]
    info_table = info_table.reset_index(drop=True)
    return info_table


def select_best(ali_table):
    """
    Takes table from function *make_alistatsum(nonred_list)*,
    orders it to select the best representative per group.
    """
    clean_table = ali_table.copy()
    clean_table = clean_table[clean_table["num_seq"] != 1]
    clean_table = clean_table[clean_table["avid"] != 100]  # unnecessary
    clean_table.sort_values(
        by=["group", "num_seq", "lenalen_ratio"],
        ascending=[1, 0, 0]
        )
    clean_table = clean_table.drop_duplicates(subset="group", keep="first")
    return clean_table


def selected_folder(sel_table):
    newdir = os.path.join(ALI_PATH, "SELECTED")
    os.mkdir(newdir)
    for urs in sel_table["urs"]:
        file = urs + ".sto"
        os.rename(os.path.join(ALI_PATH, file), os.path.join(newdir, file))

# ----PROCESS-------------------
RAW_MATRIX = parsetbl_makematrix(TBL_PATH)
BOOL_MATRIX = make_boolmatrix(RAW_MATRIX)
GROUPS_LIST = make_groups(BOOL_MATRIX)
FULL_TABLE = make_alistatsum(GROUPS_LIST)
SELECTED_TABLE = select_best(FULL_TABLE)

# ----OUTPUT--------------------
# ...table...
PRIORITY_TABLE = SELECTED_TABLE.sort_values(
    by=["num_seq", "lenalen_ratio"],
    ascending=[0, 0]
    )
del PRIORITY_TABLE["group"]
PRIORITY_TABLE.to_csv(OUTFILE, sep='\t', index=False)
# ...put into dir...
selected_folder(SELECTED_TABLE)
