import sys
import pandas as pd
from scipy.sparse import dok_matrix
import networkx as nx
import pickle

TBL_PATH = sys.argv[1]
COMPONENTS_OUT = sys.argv[2]
CLIQUES_OUT = sys.argv[3]

# read parsed table
df_tbl = pd.read_table(
    TBL_PATH,
    delim_whitespace=True)

# map urs to int
map_dict = {}
qs = list(set(df_tbl["query"]))
for i in range(0, len(qs)):
    map_dict[qs[i]] = i

# drop lines where target not in query
df_tbl = df_tbl[df_tbl["target"].isin(qs)]
# make matrix
sparse = dok_matrix((len(qs), len(qs)))
# fill sparse matrix
for urs in qs:
    i = map_dict[urs]
    for target in df_tbl[df_tbl["query"] == urs]["target"]:
        j = map_dict[target]
        sparse[i, j] = 1

graph = nx.from_scipy_sparse_matrix(sparse)
components_set = list(nx.connected_components(graph))
cliques = list(nx.find_cliques(graph))

components = []
for i in range(0, len(components_set)):
    components.append(list(components_set[i]))

# replace components with names
rev_map_dict = {v: k for k, v in map_dict.items()}

components_names = []
for i in range(0, len(components)):
    sublist = []
    for j in components[i]:
        sublist.append(rev_map_dict[j])
    components_names.append(sublist)

cliques_names = []
for i in range(0, len(cliques)):
    sublist = []
    for j in cliques[i]:
        sublist.append(rev_map_dict[j])
    cliques_names.append(sublist)

# save
with open(COMPONENTS_OUT, 'wb') as f:
    pickle.dump(components_names, f)

with open(CLIQUES_OUT, 'wb') as f:
    pickle.dump(cliques_names, f)
