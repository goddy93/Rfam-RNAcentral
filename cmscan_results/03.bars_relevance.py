import pandas as pd
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

#------Output files----
woothsepgroups = "./plots/lato/03.bars_relevance.html"


#------Read files----
samehit = "./clean_tables/lato/df_samehit"
confhit = "./clean_tables/lato/df_confhit"
lostscan = "./clean_tables/lato/df_lostscan"
newmem = "./clean_tables/lato/df_newmem"
newfam = "./clean_tables/lato/df_newfam"

#------Dataframes-----
df_samehit = pd.read_table(
    samehit,
    low_memory=False,
    sep="\t"
    )

df_confhit = pd.read_table(
    confhit,
    low_memory=False,
    sep="\t"
    )

df_lostscan = pd.read_table(
    lostscan,
    low_memory=False,
    sep="\t"
    )

df_newmem = pd.read_table(
    newmem,
    low_memory=False,
    sep="\t"
    )

df_newfam = pd.read_table(
   newfam,
    low_memory=False,
    sep="\t"
    )


#.....Group.....
rnatype_group = {
    "rasiRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "siRNA,snRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "piRNA,other":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "miRNA,siRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "miRNA,piRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "piRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "siRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "lncRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "guide_RNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "rRNA,snRNA":"<b>RNA types</b><br><b>not to be considered for Rfam</b><br><i>(piRNA, rasiRNA, siRNA, lncRNA, etc.)</i>",
    "scRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "precursor":"<b>Unclassified</b><br><b>RNA type</b>",
    "other":"<b>Unclassified</b><br><b>RNA type</b>",
    "autocataly":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "rRNA,tRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "antisense":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "snRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "miRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "tRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "telomerase":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "lncRNA,snoRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "ribozyme":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "scRNA,SRP_RNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "RNase_MRP":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "tmRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "snoRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "snRNA,snoRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "rRNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "RNase_P_RN":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "vault_RNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "SRP_RNA":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>",
    "hammerhead":"<b>RNA types</b><br><b>considered for Rfam</b><br><i>(rRNA, tRNA, ribozyme, snRNA, etc.)</i>"
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

rnatype_table = rnatype_table.set_index(["rna_type"])
rnatype_table.columns = ["samehit", "confhit", "lostscan", "newmem", "newfam"]
rnatype_table = rnatype_table.fillna(0)
rnatype_table["sum"] = rnatype_table.samehit + rnatype_table.confhit + rnatype_table.lostscan + rnatype_table.newmem + rnatype_table.newfam
rnatype_table = rnatype_table.sort_values(by="sum", ascending = [0])

sig_types = rnatype_table['sum'] > 20
sig_rnatype_table = rnatype_table[sig_types]

#.....percentages
sig_rnatype_table = sig_rnatype_table.copy()
sig_rnatype_table["samehit_per"] = sig_rnatype_table["samehit"] / sig_rnatype_table["sum"]
sig_rnatype_table["confhit_per"] = sig_rnatype_table["confhit"]/sig_rnatype_table["sum"]
sig_rnatype_table["lostscan_per"] = sig_rnatype_table["lostscan"]/sig_rnatype_table["sum"]
sig_rnatype_table["newmem_per"] = sig_rnatype_table["newmem"]/sig_rnatype_table["sum"]
sig_rnatype_table["newfam_per"] = sig_rnatype_table["newfam"]/sig_rnatype_table["sum"]

sens = round((sig_rnatype_table["samehit_per"].iloc[0] + sig_rnatype_table["confhit_per"].iloc[0] + sig_rnatype_table["newmem_per"].iloc[0])*100,1)
spec = round((sig_rnatype_table["newfam_per"].iloc[1] + sig_rnatype_table["lostscan_per"].iloc[1])*100,1)


#=====GRAPHICAL OUTPUTS=====
def plotbars ( df_name, group1, group2, group3, group4, group5, filename ):
    dict_colors = {group1: "rgb(215,25,28)",
       group2: "rgb(214, 105, 23)",
       group3: "rgb(135, 16, 16)",
       group4:  "rgb(19,46,131)",
       group5: "rgb(25, 148, 146)"
        }

    trace1 = Bar(
            x = df_name.index,
            y = df_name[group1],
            hoverinfo = "y+name",
            marker = Marker(
                color = dict_colors[group1]
        ),
        name = "Same hit",
        opacity = 1
        )

    trace2 = Bar(
             x = df_name.index,
             y = df_name[group2],
             hoverinfo = "y+name",
             marker = Marker(
             color = dict_colors[group2],
                ),
             name = 'Conflicting hit',
             opacity = 1
             )

    trace3 = Bar(
            x = df_name.index,
            y = df_name[group3],
            hoverinfo = "y+name",
            marker = Marker(
            color = dict_colors[group3]
         ),
        name = 'Lost in scan',
        opacity = 1
        )

    trace4 = Bar(
            x = df_name.index,
            y = df_name[group4],
            hoverinfo = "y+name",
            marker = Marker(
            color = dict_colors[group4],
        ),
        name = 'New members',
        opacity = 1
        )

    trace5 = Bar(
            x = df_name.index,
            y = df_name[group5],
            hoverinfo = "y+name",
            marker = Marker(
            color = dict_colors[group5],
        ),
        name = 'New family',
        opacity = 1
        )

    data = Data([trace1, trace2, trace4, trace3, trace5])
    layout = {
  "annotations": [
    {
      "x": 0.445, 
      "y": 50, 
      "font": {
        "color": "rgba(42, 42, 42, 1)", 
        "size": 16
      }, 
      "showarrow": False, 
      "text": "<i>Sensitivity</i>: " + str(sens) +"%", 
      "textangle": -90, 
      "xref": "x", 
      "yref": "y"
    }, 
    {
      "x": 1.44, 
      "y": 50, 
      "font": {
        "color": "rgba(42, 42, 42, 1)", 
        "size": 16
      },
      "showarrow": False, 
      "text": "<i>Specificity</i>: " + str(spec) +"%", 
      "textangle": -90, 
      "xref": "x", 
      "yref": "y"
    },
    {
      "align": "right",
      "font": {
        "color": "rgba(42, 42, 42, 1)", 
        "size": 10
      }, 
      "showarrow": False, 
      "text": "<b>NEGATIVES:</b><br>RNAs that don't get hit with Rfam CM", 
      "textangle": 0, 
      "xref": "paper", 
      "x": 1.21,
      "xanchor": "auto",
      "yref": "paper",
      "y":0.99,
      "yanchor":"auto"
    },
    {
      "align": "right",
      "font": {
        "color": "rgba(42, 42, 42, 1)", 
        "size": 10
      }, 
      "showarrow": False, 
      "text": "<b>POSITIVES:</b><br>RNAs that get hit with Rfam CM", 
      "textangle": 0, 
      "xref": "paper", 
      "x": 1.21,
      "xanchor": "auto",
      "yref": "paper",
      "y":0.9381530984204132,
      "yanchor":"auto"
    }
  ], 
  "autosize": True, 
  "barmode": "stack", 
  "barnorm": "percent", 
  "font": {"family": "Arial"}, 
  "height": 1123, 
  "hovermode": "closest", 
  "legend": {
            "font": {"family": "Arial"}, 
            "bgcolor": "rgba(42, 42, 42, 0)",
            "x": 1.2089955031770143,
            "xanchor": "left",
            "y": 0.9951397326852977,
            "yanchor": "auto"
            }, 
  "margin": {"b": 200}, 
  "plot_bgcolor": "#EFECEA", 
  "shapes": [
    {
      "fillcolor": "rgba(161, 70, 70, .3)", 
      "layer": "below",
      "line": {
        "color": "rgb(194, 7, 7, 1)", 
        "dash": "dot", 
        "width": 1
      }, 
      "opacity": 1, 
      "type": "rectangle", 
      "x0": -0.47, 
      "x1": 0.47, 
      "xref": "x", 
      "y0": 0, 
      "y1": sens, 
      "yref": "y"
    }, 
    {
      "fillcolor": "rgba(192, 190, 190, .3)",
      "layer": "below", 
      "line": {
        "color": "rgba(68, 68, 68, 1)", 
        "dash": "dot", 
        "width": 1
      }, 
      "opacity": 1, 
      "type": "rectangle", 
      "x0": -0.47, 
      "x1": 0.47, 
      "xref": "x", 
      "y0": sens, 
      "y1": 100, 
      "yref": "y"
    }, 
    {
      "fillcolor": "rgba(192, 190, 190, .3)",
      "layer": "below", 
      "line": {
        "color": "rgba(68, 68, 68, 1)", 
        "dash": "dot", 
        "width": 1
      }, 
      "opacity": 1, 
      "type": "rectangle", 
      "x0": 0.53, 
      "x1": 1.47, 
      "xref": "x", 
      "y0": 100, 
      "y1": 100-spec, 
      "yref": "y"
    }, 
    {
      "fillcolor": "rgba(161, 70, 70, .3)",
      "layer": "below", 
      "line": {
        "color": "rgb(194, 7, 7, 1)", 
        "dash": "dot", 
        "width": 1
      }, 
      "opacity": 1, 
      "type": "rectangle", 
      "x0": 0.53, 
      "x1": 1.47, 
      "xref": "x", 
      "y0": 100-spec, 
      "y1": 0, 
      "yref": "y"
    },
    {
      "fillcolor": "rgba(192, 190, 190, .2)",
      "layer": "below", 
      "line": {
        "color": "rgba(68, 68, 68, 1)", 
        "dash": "dot", 
        "width": 1
      }, 
      "opacity": 1, 
      "type": "rectangle", 
      "x0": 1.0176524953789283, 
      "x1": 1.35, 
      "xref": "paper", 
      "y0": 0.943, 
      "y1": 0.99, 
      "yref": "paper"
    },
    {
      "fillcolor": "rgba(161, 70, 70, .2)",
      "layer": "below", 
      "line": {
        "color": "rgba(194, 7, 7, 1)", 
        "dash": "dot", 
        "width": 1
      }, 
      "opacity": 1, 
      "type": "rectangle", 
      "x0": 1.0176524953789283, 
      "x1": 1.35, 
      "xref": "paper", 
      "y0": 0.943, 
      "y1": 0.87, 
      "yref": "paper"
    }
  ], 
  "title": "", 
  "titlefont": {"family": "Arial"}, 
  "width": 1328, 
  "xaxis": {
    "autorange": True, 
    "gridcolor": "#FFFFFF", 
    "range": [-0.5, 2.5], 
    "showgrid": False, 
    "tickangle": 0, 
    "tickfont": {"family": "Arial"}, 
    "title": "", 
    "type": "category"
  }, 
  "yaxis": {
    "dtick": 10, 
    "gridcolor": "#FFFFFF", 
    "range": [0, 100], 
    "showgrid": True, 
    "title": "%", 
    "type": "linear", 
    "zeroline": False
  }
}
    fig = Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename = filename)

plotbars( sig_rnatype_table, "samehit_per", "confhit_per", "lostscan_per", "newmem_per", "newfam_per", woothsepgroups)
