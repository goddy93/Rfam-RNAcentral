import pandas as pd
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

#------Output files----
rna_type_order_samehit = "./plots/lato/02.a.bar_rnatype(sh).html"
rna_type_order_newfam = "./plots/lato/02.a.bar_rnatype(nf).html"

#Alternative orders
#rna_type_order_lostscan = "./plots/2.a.bar_rnatype(ls).html"
#rna_type_order_newmem = "./plots/2.a.bar_rnatype(nm).html"

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

#=====GRAPHICAL OUTPUTS=====
dict_colors = {"samehit": "rgb(215,25,28)",
        "confhit": "rgb(186, 73, 72)",
        "lostscan": "rgb(135, 16, 16)",
        "newmem":  "rgb(19,46,131)",
        "newfam": "rgb(25, 148, 146)"
        }

#-----Bar graphs with percentage per rna_type
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

#.....Plot ordered bars
sig_rnatype_table["samehit_per"] = sig_rnatype_table["samehit"]/sig_rnatype_table["sum"]
sig_rnatype_table["confhit_per"] = sig_rnatype_table["confhit"]/sig_rnatype_table["sum"]
sig_rnatype_table["lostscan_per"] = sig_rnatype_table["lostscan"]/sig_rnatype_table["sum"]
sig_rnatype_table["newmem_per"] = sig_rnatype_table["newmem"]/sig_rnatype_table["sum"]
sig_rnatype_table["newfam_per"] = sig_rnatype_table["newfam"]/sig_rnatype_table["sum"]

def plotbars ( df_name, group1, group2, group3, group4, group5, filename ):
    dict_colors = {group1: "rgb(215,25,28)",
       group2: "rgb(186, 73, 72)",
       group3: "rgb(135, 16, 16)",
       group4:  "rgb(19,46,131)",
       group5: "rgb(25, 148, 146)"
        }

    trace1 = Bar(
            x = df_name.index,
            y = df_name[group1],
            hoverinfo = "value",
            marker = Marker(
                color = dict_colors[group1],
            line = Line(
                color = dict_colors[group1]
            )
        ),
        name = "Same hit",
        opacity = 1
        )

    trace2 = Bar(
             x = df_name.index,
             y = df_name[group2],
             hoverinfo = "value",
             marker = Marker(
             color = dict_colors[group2],
                line = Line(
                 color = dict_colors[group2]
                )
                ),
             name = 'Conflicting hit',
             opacity = 1
             )

    trace3 = Bar(
            x = df_name.index,
            y = df_name[group3],
            hoverinfo = "value",
            marker = Marker(
            color = dict_colors[group3],
            line = Line(
                color = dict_colors[group3]
            )
         ),
        name = 'Lost in scan',
        opacity = 1
        )

    trace4 = Bar(
            x = df_name.index,
            y = df_name[group4],
            hoverinfo = "value",
            marker = Marker(
            color = dict_colors[group4],
            line = Line(
                color = dict_colors[group4]
            )
        ),
        name = 'New members',
        opacity = 1
        )

    trace5 = Bar(
            x = df_name.index,
            y = df_name[group5],
            hoverinfo = "value",
            marker = Marker(
            color = dict_colors[group5],
            line = Line(
                color = dict_colors[group5]
            )
        ),
        name = 'New family',
        opacity = 1
        )

    trace6 = Scatter(
            x = df_name.index,
            y = df_name["sum"],
            yaxis = "y2",

            hoverinfo = "value",
            marker = Marker(
            color = 'rgb(0, 0, 0)',
        ),
        name = 'Number of URS',
        opacity = 1,
        mode = 'markers'
        )

    data = Data([trace1, trace2, trace3, trace4, trace5, trace6])

    layout = go.Layout(
        barmode = 'stack',
        barnorm = 'percent',
        margin = Margin(
            b = 200,
        ),
        title = 'RNA type in groups',
        xaxis = dict(
            title = 'rna_type',
            tickangle = 45
        ),
        yaxis = dict(
            title = '%',
            zeroline = False,
            range = [0, 100],
            showgrid = False
        ),
        yaxis2 = dict(
            title = 'Number of URS',
            overlaying = 'y',
            side = 'right',
            color = 'rgb(255, 255, 255)',
            showticklabels = False,
            zeroline = False,
            autorange = True,
            showgrid = False
        ),
    )

    fig = go.Figure(data = data, layout = layout)
    plotly.offline.plot(fig, filename = filename)

#order_lostscan = sig_rnatype_table.sort_values(by=["lostscan_per"], ascending=0)
#plotbars( order_lostscan, "samehit_per", "confhit_per", "lostscan_per", "newmem_per", "newfam_per", rna_type_order_lostscan)
#order_newmem = sig_rnatype_table.sort_values(by=["newmem_per"], ascending=0)
#plotbars( order_newmem, "samehit_per", "confhit_per", "lostscan_per", "newmem_per", "newfam_per", rna_type_order_newmem)

order_samehit = sig_rnatype_table.sort_values(by=["samehit_per"], ascending=0)
plotbars( order_samehit, "samehit_per", "confhit_per", "lostscan_per", "newmem_per", "newfam_per", rna_type_order_samehit)
order_newfam = sig_rnatype_table.sort_values(by=["newfam_per"], ascending=0)
plotbars( order_newfam, "samehit_per", "confhit_per", "lostscan_per", "newmem_per", "newfam_per", rna_type_order_newfam)
