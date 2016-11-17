import MySQLdb
import sqlalchemy
import pandas as pd
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

allpiechart = "./files/all_pie.html"
rna_type_allbar = "./files/rna_type_allbar.html"
rna_type_sigbar = "./files/rna_type_sigbar.html"
newfamilyurs_table = "./files/newfamilyurs_table.html"

#=====DATA INPUT=====
engine = sqlalchemy.create_engine('mysql+mysqldb://root:rna@localhost/rnac_rfam')
connection = engine.connect()

#-----Group queries-----
query_tot = "SELECT id FROM cmscan_run"
query_samehit = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NOT NULL AND ch.hit_rfam_acc IS NOT NULL AND uc.rfam_acc = ch.hit_rfam_acc"
query_confhit = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NOT NULL AND ch.hit_rfam_acc IS NOT NULL AND uc.rfam_acc != ch.hit_rfam_acc"
query_lostscan = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NOT NULL AND ch.hit_rfam_acc IS NULL"
query_newmem = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NULL AND ch.hit_rfam_acc IS NOT NULL"
query_newfam = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NULL AND ch.hit_rfam_acc IS NULL"

#------Dataframes-----
df_tot = pd.read_sql_query(
    query_tot, 
    connection, 
    index_col = None, 
    coerce_float = True, 
    params = None, 
    parse_dates = None,
    chunksize = None
    )
df_samehit = pd.read_sql_query(
    query_samehit,
    connection,
    index_col = None,
    coerce_float = True,
    params = None,
    parse_dates = None,
    chunksize = None
    )
df_confhit = pd.read_sql_query(
    query_confhit,
    connection, 
    index_col = None, 
    coerce_float = True, 
    params = None, 
    parse_dates = None, 
    chunksize = None
    )
df_lostscan = pd.read_sql_query(
    query_lostscan, 
    connection, 
    index_col = None, 
    coerce_float = True, 
    params = None, 
    parse_dates = None, 
    chunksize = None
    )
df_newmem = pd.read_sql_query(
    query_newmem, 
    connection, 
    index_col = None, 
    coerce_float = True, 
    params = None, 
    parse_dates = None, 
    chunksize = None
    )
df_newfam = pd.read_sql_query(
    query_newfam, 
    connection, 
    index_col = None, 
    coerce_float = True, 
    params = None, 
    parse_dates = None, 
    chunksize = None
    )

#-----Workaround to count separately samehit and confhit-----
query_colapsedhits = "SELECT ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families FROM cmscan_hits ch GROUP BY ch.id"
df_colapsedhits = pd.read_sql_query(
    query_colapsedhits, 
    connection, 
    index_col = None, 
    coerce_float = True, 
    params = None, 
    parse_dates = None, 
    chunksize = None
    )
mask = (df_colapsedhits['families'].str.len() > 7)
doublehit_list = df_colapsedhits.loc[mask]

#=====GRAPHICAL OUTPUTS=====
#-----Pie chart, URS per group
#.....Data.....
dict_allgroups = {"Same hit": len(df_tot) - len(doublehit_list) - len(df_lostscan) - len(df_newmem) - len(df_newfam),
		"Conflicting hits": len(doublehit_list),
		"Lost in scan": len(df_lostscan),
		"New members": len(df_newmem),
		"New families": len(df_newfam)
		}
labels = dict_allgroups.keys()
values = dict_allgroups.values()
dict_colors = {"Same hit": "rgb(215,25,28)",
		"Conflicting hits": "rgb(135, 16, 16)",
		"Lost in scan": "rgb(199, 31, 30)",
		"New members":  "rgb(19,46,131)",
		"New families": "rgb(25, 148, 146)"
		}

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

plotly.offline.plot(fig, filename = allpiechart)

#-----Bar graphs with percentage per rna_type
#.....Counts.....
rnatype_samehit = df_samehit.rna_type.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
rnatype_samehit = rnatype_samehit.reset_index(level = ['rna_type'])
rnatype_samehit.columns = ['rna_type', 'count']

rnatype_confhit = df_confhit.rna_type.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
rnatype_confhit = rnatype_confhit.reset_index(level = ['rna_type'])
rnatype_confhit.columns = ['rna_type', 'count']

rnatype_lostscan = df_lostscan.rna_type.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
rnatype_lostscan = rnatype_lostscan.reset_index(level = ['rna_type'])
rnatype_lostscan.columns = ['rna_type', 'count']

rnatype_newmem = df_newmem.rna_type.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
rnatype_newmem = rnatype_newmem.reset_index(level = ['rna_type'])
rnatype_newmem.columns = ['rna_type', 'count']

rnatype_newfam = df_newfam.rna_type.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
rnatype_newfam = rnatype_newfam.reset_index(level = ['rna_type'])
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


#.....Graph with all.....
trace1 = Bar(
        x = rnatype_table.index,
        y = rnatype_table["samehit"],
        hoverinfo = "none",
        marker = Marker(
        color = 'rgb(215,25,28)',
        line = Line(
            color = 'rgb(215,25,28)'
        )
    ),
    name = 'Same hit',
    opacity = 1
    )

trace2 = Bar(
         x = rnatype_table.index,
         y = rnatype_table["confhit"],
         hoverinfo = "none",
         marker = Marker(
         color = 'rgb(135, 16, 16)',
            line = Line(
             color = 'rgb(135, 16, 16)'
            )
            ),
         name = 'Conflicting hit',
         opacity = 1
         )

trace3 = Bar(
        x = rnatype_table.index,
        y = rnatype_table["lostscan"],
        hoverinfo = "none",
        marker = Marker(
        color = 'rgb(199, 31, 30)',
        line = Line(
            color = 'rgb(199, 31, 30)'
        )
     ),
    name = 'Lost in scan',
    opacity = 1
    )

trace4 = Bar(
        x = rnatype_table.index,
        y = rnatype_table["newmem"],
        hoverinfo = "none",
        marker = Marker(
        color = 'rgb(19,46,131)',
        line = Line(
            color = 'rgb(19,46,131)'
        )
    ),
    name = 'New members',
    opacity = 1
    )

trace5 = Bar(
        x = rnatype_table.index,
        y = rnatype_table["newfam"],
        hoverinfo = "none",
        marker = Marker(
        color = 'rgb(25, 148, 146)',
        line = Line(
            color = 'rgb(25, 148, 146)'
        )
    ),
    name = 'New family',
    opacity = 1
    )

trace6 = Scatter(
        x = rnatype_table.index,
        y = rnatype_table["sum"],
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
        zeroline = False,
        color = 'rgb(255, 255, 255)',
        showticklabels = False,
        autorange = True,
        showgrid = False
    ),
)

fig = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = rna_type_allbar)

#.....Graph with only types with more than 20

trace1 = Bar(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["samehit"],
        hoverinfo = "value",
        marker = Marker(
            color = 'rgb(215,25,28)',
        line = Line(
            color = 'rgb(215,25,28)'
        )
    ),
    name = "Same hit",
    opacity = 1
    )

trace2 = Bar(
         x = sig_rnatype_table.index,
         y = sig_rnatype_table["confhit"],
         hoverinfo = "value",
         marker = Marker(
         color = 'rgb(135, 16, 16)',
            line = Line(
             color = 'rgb(135, 16, 16)'
            )
            ),
         name = 'Conflicting hit',
         opacity = 1
         )

trace3 = Bar(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["lostscan"],
        hoverinfo = "value",
        marker = Marker(
        color = 'rgb(199, 31, 30)',
        line = Line(
            color = 'rgb(199, 31, 30)'
        )
     ),
    name = 'Lost in scan',
    opacity = 1
    )

trace4 = Bar(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["newmem"],
        hoverinfo = "value",
        marker = Marker(
        color = 'rgb(19,46,131)',
        line = Line(
            color = 'rgb(19,46,131)'
        )
    ),
    name = 'New members',
    opacity = 1
    )

trace5 = Bar(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["newfam"],
        hoverinfo = "value",
        marker = Marker(
        color = 'rgb(25, 148, 146)',
        line = Line(
            color = 'rgb(25, 148, 146)'
        )
    ),
    name = 'New family',
    opacity = 1
    )

trace6 = Scatter(
        x = sig_rnatype_table.index,
        y = sig_rnatype_table["sum"],
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
plotly.offline.plot(fig, filename = rna_type_sigbar)

#-----Table with interesting New family urs
#.....Query (with filter) and dataframe.....
query_newfamfilter = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NULL AND ch.hit_rfam_acc IS NULL AND uc.rna_type NOT LIKE 'tRNA' AND uc.rna_type NOT LIKE 'rRNA' AND uc.rna_type NOT LIKE 'piRNA' AND ur.len > 30 AND ur.len < 200 ORDER BY uc.db"

df_newfamfilter = pd.read_sql_query(
    query_newfamfilter,
    connection,
    index_col = None,
    coerce_float = True,
    params = None,
    parse_dates = None,
    chunksize = None
    )

#.....Table with links.....
df_newfamfilter = df_newfamfilter.sort(["db", "rna_type", "len"], ascending = [0,0,0])
table_out = df_newfamfilter[["id","len","db","rna_type"]]

urs = list(df_newfamfilter["id"])
d_urs = {}
for x in urs:
        d_urs[x] = '<a href="http://rnacentral.org/rna/{0}">{0}</a>'.format(x)

table_out['id'].replace(d_urs, inplace = True)
table = FF.create_table(table_out)
plotly.offline.plot(table, filename = newfamilyurs_table)

#-----Pie charts per group
#.....Same hit pie.....
data = Data([
    Pie(
        hoverinfo = 'label+percent+value',
        sort = True,
        textinfo = "none",
        name = "Same hit",
        labels = sig_rnatype_table.index,
        values = sig_rnatype_table["samehit"]
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 180,
        b = 50,
    ),
    height = 633,
    title = 'Same hit group',
    width = 1332,
    showlegend = False
)
fig = Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = "pie_confhit.html")

#.....Conflicting hit pie.....
data = Data([
    Pie(
        hoverinfo = 'label+percent+value',
        sort = True,
        textinfo = "none",
        name = "Conflicting hit",
        labels = sig_rnatype_table.index,
        values = sig_rnatype_table["confhit"]
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 180,
        b = 50,
    ),
    height = 633,
    title = 'Conflicing hit group',
    width = 1332,
    showlegend = False
)
fig = Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = "pie_confhit.html")

#.....Lost in scan pie.....
data = Data([
    Pie(
        hoverinfo = 'label+percent+value',
        sort = True,
        textinfo = "none",
        name = "Lost in scan",
        labels = sig_rnatype_table.index,
        values = sig_rnatype_table["lostscan"]
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 180,
        b = 50,
    ),
    height = 633,
    title = 'Lost in scan group',
    width = 1332,
    showlegend = False
)
fig = Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = "pie_lostscan.html")

#.....New members pie.....
data = Data([
    Pie(
        hoverinfo = 'label+percent+value',
        sort = True,
        textinfo = "none",
        name = "New members",
        labels = sig_rnatype_table.index,
        values = sig_rnatype_table["newmem"]
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 180,
        b = 50,
    ),
    height = 633,
    title = 'New members group',
    width = 1332,
    showlegend = False
)
fig = Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = "pie_newmem.html")

#.....New family pie.....
data = Data([
    Pie(
        hoverinfo = 'label+percent+value',
        sort = True,
        textinfo = "none",
        name = "New family",
        labels = sig_rnatype_table.index,
        values = sig_rnatype_table["newfam"]
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 180,
        b = 50,
    ),
    height = 633,
    title = 'New family group',
    width = 1332,
    showlegend = False
)
fig = Figure(data = data, layout = layout)
plotly.offline.plot(fig, filename = "pie_newfam.html")
