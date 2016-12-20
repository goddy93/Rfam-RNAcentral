import pandas as pd
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

#------Output files----
wothsep = "./plots/lato/03.b.w_oth_sep.html"
wothjoin = "./plots/lato/03.b.w_oth_join.html"
woothsep = "./plots/lato/03.a.wo_oth_sep.html"
woothjoin = "./plots/lato/03.a.wo_oth_join.html"


#------Read files----
samehit = "./clean_tables/lato/df_samehit"
confhit = "./clean_tables/lato/df_confhit"
lostscan = "./clean_tables/lato/df_lostscan"
newmem = "./clean_tables/lato/df_newmem"
newfam = "./clean_tables/lato/df_newfam"

#------Dataframes-----
df_samehit = pd.read_table(
    samehit,
    sep="\t"
    )

df_confhit = pd.read_table(
    confhit,
    sep="\t"
    )

df_lostscan = pd.read_table(
    lostscan,
    sep="\t"
    )

df_newmem = pd.read_table(
    newmem,
    sep="\t"
    )

df_newfam = pd.read_table(
   newfam,
    sep="\t"
    )


#.....Group.....
rnatype_group = {
    "rasiRNA":"RNA types<br>not to be considered for Rfam",
    "siRNA,snRNA":"RNA types<br>not to be considered for Rfam",
    "piRNA,other":"RNA types<br>not to be considered for Rfam",
    "miRNA,siRNA":"RNA types<br>not to be considered for Rfam",
    "miRNA,piRNA":"RNA types<br>not to be considered for Rfam",
    "piRNA":"RNA types<br>not to be considered for Rfam",
    "siRNA":"RNA types<br>not to be considered for Rfam",
    "lncRNA":"RNA types<br>not to be considered for Rfam",
    "guide_RNA":"RNA types<br>not to be considered for Rfam",
    "rRNA,snRNA":"RNA types<br>not to be considered for Rfam",
    "scRNA":"RNA types<br>considered for Rfam",
    "precursor":"Unclassified<br>RNA type",
    "other":"Unclassified<br>RNA type",
    "autocataly":"RNA types<br>considered for Rfam",
    "rRNA,tRNA":"RNA types<br>considered for Rfam",
    "antisense":"RNA types<br>considered for Rfam",
    "snRNA":"RNA types<br>considered for Rfam",
    "miRNA":"RNA types<br>considered for Rfam",
    "tRNA":"RNA types<br>considered for Rfam",
    "telomerase":"RNA types<br>considered for Rfam",
    "lncRNA,snoRNA":"RNA types<br>considered for Rfam",
    "ribozyme":"RNA types<br>considered for Rfam",
    "scRNA,SRP_RNA":"RNA types<br>considered for Rfam",
    "RNase_MRP":"RNA types<br>considered for Rfam",
    "tmRNA":"RNA types<br>considered for Rfam",
    "snoRNA":"RNA types<br>considered for Rfam",
    "snRNA,snoRNA":"RNA types<br>considered for Rfam",
    "rRNA":"RNA types<br>considered for Rfam",
    "RNase_P_RN":"RNA types<br>considered for Rfam",
    "vault_RNA":"RNA types<br>considered for Rfam",
    "SRP_RNA":"RNA types<br>considered for Rfam",
    "hammerhead":"RNA types<br>considered for Rfam"
}

df_samehit["rna_type"].replace(rnatype_group, inplace=True)
df_confhit["rna_type"].replace(rnatype_group, inplace=True)
df_lostscan["rna_type"].replace(rnatype_group, inplace=True)
df_newmem["rna_type"].replace(rnatype_group, inplace=True)
df_newfam["rna_type"].replace(rnatype_group, inplace=True)

#.....Counts.....
rnatype_samehit = pd.DataFrame(df_samehit["rna_type"].value_counts())
rnatype_samehit.reset_index(level=0, inplace=True)
rnatype_samehit.columns = ['rna_type', 'count']

rnatype_confhit = pd.DataFrame(df_confhit["rna_type"].value_counts())
rnatype_confhit.reset_index(level=0, inplace=True)
rnatype_confhit.columns = ['rna_type', 'count']

rnatype_lostscan = pd.DataFrame(df_lostscan["rna_type"].value_counts())
rnatype_lostscan.reset_index(level=0, inplace=True)
rnatype_lostscan.columns = ['rna_type', 'count']

rnatype_newmem = pd.DataFrame(df_newmem["rna_type"].value_counts())
rnatype_newmem.reset_index(level=0, inplace=True)
rnatype_newmem.columns = ['rna_type', 'count']

rnatype_newfam = pd.DataFrame(df_newfam["rna_type"].value_counts())
rnatype_newfam.reset_index(level=0, inplace=True)
rnatype_newfam.columns = ['rna_type', 'count']

#.....Big table.....
rnatype_table = pd.merge(rnatype_samehit, rnatype_confhit, on="rna_type", how="outer")
rnatype_table = pd.merge(rnatype_table, rnatype_lostscan, on="rna_type", how="outer")
rnatype_table = pd.merge(rnatype_table, rnatype_newmem, on="rna_type", how="outer")
rnatype_table = pd.merge(rnatype_table, rnatype_newfam, on="rna_type", how="outer")

rnatype_table.columns = ["rna_type", "samehit", "confhit", "lostscan", "newmem", "newfam"]
rnatype_table = rnatype_table.set_index(["rna_type"])
rnatype_table = rnatype_table.fillna(0)
rnatype_table["sum"] = rnatype_table.samehit + rnatype_table.confhit + rnatype_table.lostscan + rnatype_table.newmem + rnatype_table.newfam
rnatype_table = rnatype_table.sort(["sum"], ascending = [0])

sig_types = rnatype_table['sum'] > 20
sig_rnatype_table = rnatype_table[sig_types]

#=====GRAPHICAL OUTPUTS=====
dict_colors = {"samehit": "rgb(215,25,28)",
        "confhit": "rgb(186, 73, 72)",
        "lostscan": "rgb(135, 16, 16)",
        "newmem":  "rgb(19,46,131)",
        "newfam": "rgb(25, 148, 146)"
        }

#.....Bars to plot
sig_rnatype_table["in_rfam"] = (sig_rnatype_table["samehit"] + sig_rnatype_table["confhit"] + sig_rnatype_table["lostscan"]) / sig_rnatype_table["sum"]
sig_rnatype_table["pot_in_rfam"] = sig_rnatype_table["newmem"] / sig_rnatype_table["sum"]
sig_rnatype_table["no_rfam"] = sig_rnatype_table["newfam"] / sig_rnatype_table["sum"]
#grouped
sig_rnatype_table["yes_rfam"] = sig_rnatype_table["in_rfam"] + sig_rnatype_table["pot_in_rfam"]

dict_colors = {"in_rfam": "rgb(135, 16, 16)",
   "pot_in_rfam": "rgb(215,25,28)",
   "no_rfam": "rgb(161, 173, 173)",
   "yes_rfam": "rgb(135, 16, 16)"
    }

#3 Bars: want, no want and other, 3 groups: in Rfam, pot_Rfam and not hit
trace1 = Bar(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["in_rfam"],
        hoverinfo = 'y',
        marker = Marker(
            color = dict_colors["in_rfam"],
        line = Line(
            color = dict_colors["in_rfam"]
        )
    ),
    name = "Hit by Rfam CM (in Rfam)",
    opacity = 1
    )

trace2 = Bar(
         x = sig_rnatype_table.index,
         y = sig_rnatype_table["pot_in_rfam"],
         hoverinfo = 'y',
         marker = Marker(
         color = dict_colors["pot_in_rfam"],
            line = Line(
             color = dict_colors["pot_in_rfam"]
            )
            ),
         name = 'Hit by Rfam CM (potentially in Rfam)',
         opacity = 1
         )

trace3 = Bar(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["no_rfam"],
        hoverinfo = 'y',
        marker = Marker(
        color = dict_colors["no_rfam"],
        line = Line(
            color = dict_colors["no_rfam"]
        )
     ),
    name = 'Not hit by Rfam CM',
    opacity = 1
    )

data = Data([trace1, trace2, trace3])

layout = go.Layout(
    barmode = 'stack',
    barnorm = 'percent',
    margin = Margin(
        b = 200,
    ),
    title = '',
    xaxis = dict(
        title = '',
        tickangle = 0
    ),
    yaxis = dict(
        title = '%',
        zeroline = False,
        range = [0, 100],
        showgrid = False
    )
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = wothsep)

#3 Bars: want, no want and other, 2 groups: hit and not hit
trace1 = Bar(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["yes_rfam"],
        hoverinfo = 'y',
        marker = Marker(
            color = dict_colors["yes_rfam"],
        line = Line(
            color = dict_colors["yes_rfam"]
        )
    ),
    name = "Hit by Rfam CM",
    opacity = 1
    )

trace2 = Bar(
         x = sig_rnatype_table.index,
         y = sig_rnatype_table["no_rfam"],
         hoverinfo = 'y',
         marker = Marker(
         color = dict_colors["no_rfam"],
            line = Line(
             color = dict_colors["no_rfam"]
            )
            ),
         name = 'Not hit by Rfam CM',
         opacity = 1
         )

data = Data([trace1, trace2])

layout = go.Layout(
    barmode = 'stack',
    barnorm = 'percent',
    margin = Margin(
        b = 200,
    ),
    title = '',
    xaxis = dict(
        title = '',
        tickangle = 0
    ),
    yaxis = dict(
        title = '%',
        zeroline = False,
        range = [0, 100],
        showgrid = False
    )
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = wothjoin)

#2 Bars: want, no want, 3 groups: in Rfam, pot_Rfam and not hit
trace1 = Bar(
        x = sig_rnatype_table.index[0:2],
        y = sig_rnatype_table["in_rfam"],
        hoverinfo = 'y',
        marker = Marker(
            color = dict_colors["in_rfam"],
        line = Line(
            color = dict_colors["in_rfam"]
        )
    ),
    name = "Hit by Rfam CM (in Rfam)",
    opacity = 1
    )

trace2 = Bar(
         x = sig_rnatype_table.index[0:2],
         y = sig_rnatype_table["pot_in_rfam"],
         hoverinfo = 'y',
         marker = Marker(
         color = dict_colors["pot_in_rfam"],
            line = Line(
             color = dict_colors["pot_in_rfam"]
            )
            ),
         name = 'Hit by Rfam CM (potentially in Rfam)',
         opacity = 1
         )
trace3 = Bar(
        x = sig_rnatype_table.index[0:2],
        y = sig_rnatype_table["no_rfam"],
        hoverinfo = 'y',
        marker = Marker(
        color = dict_colors["no_rfam"],
        line = Line(
            color = dict_colors["no_rfam"]
        )
     ),
    name = 'Not hit by Rfam CM',
    opacity = 1
    )

data = Data([trace1, trace2, trace3])

layout = go.Layout(
    barmode = 'stack',
    barnorm = 'percent',
    margin = Margin(
        b = 200,
    ),
    title = '',
    xaxis = dict(
        title = '',
        tickangle = 0
    ),
    yaxis = dict(
        title = '%',
        zeroline = False,
        range = [0, 100],
        showgrid = False
    )
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = woothsep)

#2 Bars: want, no want, 2 groups: hit and not hit
trace1 = Bar(
        x = sig_rnatype_table.index[0:2],
        y = sig_rnatype_table["yes_rfam"],
        hoverinfo = 'y',
        marker = Marker(
            color = dict_colors["yes_rfam"],
        line = Line(
            color = dict_colors["yes_rfam"]
        )
    ),
    name = "Hit by Rfam CM",
    opacity = 1
    )

trace2 = Bar(
         x = sig_rnatype_table.index[0:2],
         y = sig_rnatype_table["no_rfam"],
         hoverinfo = 'y',
         marker = Marker(
         color = dict_colors["no_rfam"],
            line = Line(
             color = dict_colors["no_rfam"]
            )
            ),
         name = 'Not hit by Rfam CM',
         opacity = 1
         )

data = Data([trace1, trace2])

layout = go.Layout(
    barmode = 'stack',
    barnorm = 'percent',
    margin = Margin(
        b = 200,
    ),
    title = '',
    xaxis = dict(
        title = '',
        tickangle = 0
    ),
    yaxis = dict(
        title = '%',
        zeroline = False,
        range = [0, 100],
        showgrid = False
    )
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = woothjoin)
