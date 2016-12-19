import pandas as pd
from collections import OrderedDict
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

#------Global path----

#------Output files----
allpiechart = "./plots/01.a.pie_all.html"
slicedpiechart = "./plots/01.b.pie_sliced.html"

#------Read files----
samehit = "./clean_tables/df_samehit"
confhit = "./clean_tables/df_confhit"
lostscan = "./clean_tables/df_lostscan"
newmem = "./clean_tables/df_newmem"
newfam = "./clean_tables/df_newfam"
query_tot = "./query_files/query_tot"
query_colapsedhits = "./query_files/query_colapsedhits"

#------Dataframes-----
df_tot = pd.read_table(
    query_tot,
    sep="\t",
    names=["id"]
    )

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

#-----Workaround to count separately samehit and confhit-----
# query_colapsedhits = "SELECT ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families FROM cmscan_hits ch GROUP BY ch.id"
df_colapsedhits = pd.read_table(
    query_colapsedhits,
    sep="\t",
    names=["id", "families"]
    )

mask = (df_colapsedhits['families'].str.len() > 7)
doublehit_list = df_colapsedhits.loc[mask]

#=====GRAPHICAL OUTPUTS=====
#-----All pie chart, URS per group
#.....Data.....
dict_allgroups = OrderedDict([
    ("Conflicting hits", len(doublehit_list)),
    ("Same hit", len(df_tot) - len(doublehit_list) - len(df_lostscan) - len(df_newmem) - len(df_newfam)),
    ("New members", len(df_newmem)),
    ("New families", len(df_newfam)),
    ("Lost in scan", len(df_lostscan))
        ])

labels = dict_allgroups.keys()
values = dict_allgroups.values()

dict_colors = OrderedDict([
    ("Conflicting hits", "rgb(186, 73, 72)"),
    ("Same hit", "rgb(215,25,28)"),
    ("New members", "rgb(19,46,131)"),
    ("New families", "rgb(25, 148, 146)"),
    ("Lost in scan", "rgb(135, 16, 16)")
        ])

data = Data([
    Pie(
        domain = dict(
            x = [0, 1],
            y = [0, 1]
        ),
        hoverinfo = 'value',
        sort = False,
        labels = labels,
        marker = Marker(
            colors = dict_colors.values(),
            line = Line(
                width = 0
            )
        ),
        pull = 0,
        rotation = 360,
        showlegend = False,
        textinfo = 'label+percent',
        textposition = 'outside',
        values = values
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 180,
        b = 50,
    ),
    height = 633,
    title = 'URS in each group',
    width = 1332
)
fig = Figure(data = data, layout = layout)

plotly.offline.plot(fig, filename = allpiechart)

#-----Sliced
#.....Counts.....
rnatype_newfam = pd.DataFrame(df_newfam["rna_type"].value_counts())
rnatype_newfam.reset_index(level=0, inplace=True)
rnatype_newfam.columns = ['rna_type', 'count']

count_lncRNA1 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "lncRNA", 'count'])
count_lncRNA2 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "lncRNA,snoRNA", 'count'])
count_lncRNA3 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "lncRNA,other", 'count'])
count_miRNA1 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "miRNA", 'count'])
count_miRNA2 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "miRNA,other", 'count'])
count_miRNA3 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "miRNA,siRNA", 'count'])
count_miRNA4 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "miRNA,piRNA", 'count'])
count_piRNA1 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "piRNA", 'count'])
count_piRNA2 = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "piRNA,other", 'count'])
count_rasiRNA = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "rasiRNA", 'count'])
count_guideRNA = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "guide_RNA", 'count'])
count_siRNA = int(rnatype_newfam.loc[rnatype_newfam['rna_type'] == "siRNA", 'count'])

never_rfam = count_lncRNA1 + count_lncRNA2 + count_lncRNA3 + count_miRNA1 + count_miRNA2 + count_miRNA3 + count_miRNA4 + count_piRNA1 + count_piRNA2 + count_rasiRNA + count_guideRNA + count_siRNA 

#.....Data.....
dict_allgroups = OrderedDict([
    ("Conflicting hits", len(doublehit_list)),
    ("Same hit", len(df_tot) - len(doublehit_list) - len(df_lostscan) - len(df_newmem) - len(df_newfam)),
    ("New members", len(df_newmem)),
    ("Not for Rfam (lncRNA, miRNA, piRNA, rasiRNA, guideRNA, siRNA", never_rfam),
    ("New families", len(df_newfam) - never_rfam),
    ("Lost in scan", len(df_lostscan))
        ])


labels = dict_allgroups.keys()
values = dict_allgroups.values()

dict_colors = OrderedDict([
    ("Conflicting hits", "rgb(186, 73, 72)"),
    ("Same hit", "rgb(215,25,28)"),
    ("New members", "rgb(19,46,131)"),
    ("Not for Rfam (lncRNA, miRNA, piRNA, rasiRNA, guideRNA, siRNA)", "rgb(16, 89, 88)"),
    ("New families", "rgb(25, 148, 146)"),
    ("Lost in scan", "rgb(135, 16, 16)")
        ])

#.....Graph.....
data = Data([
    Pie(
        domain = dict(
            x = [0, 1],
            y = [0, 1]
        ),
        hoverinfo = 'value',
        sort = False,
        labels = labels,
        marker = Marker(
            colors = dict_colors.values(),
            line = Line(
                width = 0
            )
        ),
        pull = 0,
        rotation = 360,
        showlegend = False,
        textinfo = 'label+percent',
        textposition = 'outside',
        values = values
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 180,
        b = 50,
    ),
    height = 633,
    title = 'URS in each group',
    width = 1332
)
fig = Figure(data = data, layout = layout)

plotly.offline.plot(fig, filename = slicedpiechart)



