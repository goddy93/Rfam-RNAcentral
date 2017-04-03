import pandas as pd
import plotly
from plotly.graph_objs import *
from plotly.offline import plot
import plotly.graph_objs as go

# load files
IN_SAMEHIT = "./query_files/query_samehit"
IN_CONFHIT = "./query_files/query_confhit"
IN_NEWMEM = "./query_files/query_newmem"

# read files
DF_SAMEHIT = pd.read_table(
    IN_SAMEHIT,
    sep="\t",
    low_memory=False,
    names=["id",
           "len",
           "db",
           "rna_type",
           "rfam_acc",
           "tax_id",
           "hit_rfam_acc",
           "hit_clan_acc",
           "e_value"]
    )

DF_CONFHIT = pd.read_table(
    IN_CONFHIT,
    sep="\t",
    low_memory=False,
    names=["id",
           "len",
           "db",
           "rna_type",
           "rfam_acc",
           "tax_id",
           "hit_rfam_acc",
           "hit_clan_acc",
           "e_value"]
    )


DF_NEWMEM = pd.read_table(
    IN_NEWMEM,
    sep="\t",
    low_memory=False,
    names=["id",
           "len",
           "db",
           "rna_type",
           "rfam_acc",
           "tax_id",
           "hit_rfam_acc",
           "hit_clan_acc",
           "e_value"]
    )

# make full dataframe
DF_IN = pd.concat([DF_SAMEHIT, DF_CONFHIT, DF_NEWMEM])

# count hit_rfam_acc
DF_HITS = pd.DataFrame(DF_IN["hit_rfam_acc"].value_counts())
# percentage and cumulative percentage
TOTAL = DF_HITS["hit_rfam_acc"].sum()
DF_HITS["per"] = DF_HITS["hit_rfam_acc"]/TOTAL
DF_HITS["cumsum"] = DF_HITS["per"].cumsum()
DF_HITS["cumsumper"] = DF_HITS["cumsum"]*100

# PLOT ALL FAMILIES
# ..data..
x = range(0, len(DF_HITS)+1)
y1 = DF_HITS["cumsumper"].tolist()
y1.insert(0, 0)
# ..plot..
trace1 = go.Scatter(x=x, y=y1)
data = [trace1]
layout = Layout(
       paper_bgcolor='rgb(255,255,255)',
       plot_bgcolor='rgb(229,229,229)',
       xaxis=XAxis(
           range=[-10, 2281],
           title="Number of families",
           dtick=100,
           tick0=0,
           showticklabels=True,
           ticklen=4,
           tickwidth=1,
           ticks='inside',
           showline=False,
           gridcolor='rgb(255,255,255)',
           gridwidth=1,
           showgrid=False,
           zeroline=True
           ),
       yaxis=YAxis(
           range=[0, 101],
           title="Cumulative percentage of hits",
           nticks=0, 
           showticklabels=True,
           ticklen=5,
           tickwidth=1,
           ticksuffix="%",
           ticks='outside',
           showline=False,
           gridcolor='rgb(255,255,255)',
           showgrid=True,
           tick0=0,
           dtick=20,
           zeroline=True
           ),
       )
# ..draw..
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename="/Users/nquinones/Desktop/family_hitsdist_all.html")

# PLOT TOP 10
# ..data..
DF_HITSTOP10 = DF_HITS.iloc[0:10]
x = DF_HITSTOP10.index.tolist()
x.insert(0, 0)
y1 = DF_HITSTOP10["cumsumper"].tolist()
y1.insert(0, 0)
# ..plot..
trace1 = go.Scatter(x=x, y=y1)
data = [trace1]
layout = Layout(
       paper_bgcolor='rgb(255,255,255)',
       plot_bgcolor='rgb(229,229,229)',
       xaxis=XAxis(
           range=[0, 11],
           title="Families",
           dtick=1,
           tick0=0,
           showticklabels=True,
           ticklen=4,
           tickwidth=1,
           ticks='inside',
           showline=False,
           gridcolor='rgb(255,255,255)',
           gridwidth=1,
           showgrid=False,
           zeroline=True
           ),
       yaxis=YAxis(
           range=[0, 101],
           title="Cumulative percentage of hits",
           nticks=0, 
           showticklabels=True,
           ticklen=5,
           tickwidth=1,
           ticksuffix="%",
           ticks='outside',
           showline=False,
           gridcolor='rgb(255,255,255)',
           showgrid=True,
           tick0=0,
           dtick=20,
           zeroline=True
           ),
       )
# ..draw..
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename="/Users/nquinones/Desktop/family_hitsdist_top10.html")


# EXCLUDE rRNA or tRNA
# .. exclude..
EXCLUDE = ["RF00005",
           "RF00001",
           "RF02540",
           "RF02541",
           "RF00001",
           "RF00002",
           "RF02543",
           "RF02542",
           "RF00177",
           "RF01959",
           "RF01960"]
INDEX_LIST = []
for item in EXCLUDE:
    index = DF_HITS.index.get_loc(item)
    INDEX_LIST.append(index)
# ..data..
DF_NON_RT = DF_HITS
DF_NON_RT = DF_NON_RT.drop(DF_NON_RT.index[INDEX_LIST])
TOTAL_NON_RT = DF_NON_RT["hit_rfam_acc"].sum()
DF_NON_RT["per"] = DF_NON_RT["hit_rfam_acc"]/TOTAL_NON_RT
DF_NON_RT["cumsum"] = DF_NON_RT["per"].cumsum()
DF_NON_RT["cumsumper"] = DF_NON_RT["cumsum"]*100
x = range(0, len(DF_NON_RT)+1)
y1 = DF_NON_RT["cumsumper"].tolist()
y1.insert(0, 0)
# ..plot..
trace1 = go.Scatter(x=x, y=y1)
data = [trace1]
trace1 = go.Scatter(x=x, y=y1)
data = [trace1]
layout = Layout(
       paper_bgcolor='rgb(255,255,255)',
       plot_bgcolor='rgb(229,229,229)',
       xaxis=XAxis(
           range=[-10, 2271],
           title="Number of families (non rRNA or tRNA)",
           dtick=100,
           tick0=0,
           showticklabels=True,
           ticklen=4,
           tickwidth=1,
           ticks='inside',
           showline=False,
           gridcolor='rgb(255,255,255)',
           gridwidth=1,
           showgrid=False,
           zeroline=True
           ),
       yaxis=YAxis(
           range=[0, 101],
           title="Cumulative percentage of hits",
           nticks=0, 
           showticklabels=True,
           ticklen=5,
           tickwidth=1,
           ticksuffix="%",
           ticks='outside',
           showline=False,
           gridcolor='rgb(255,255,255)',
           showgrid=True,
           tick0=0,
           dtick=20,
           zeroline=True
           ),
       )
# ..draw..
fig = Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename="/Users/nquinones/Desktop/family_hitsdist_nonrt.html")
