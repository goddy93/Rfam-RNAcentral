import MySQLdb
import sqlalchemy
import pandas as pd
import colorlover as cl
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *

import plotly.plotly as py

engine = sqlalchemy.create_engine('mysql+mysqldb://root:rna@localhost/rnac_rfam')
connection = engine.connect()

#TOTAL SCANNED
query_tot = "SELECT id FROM cmscan_run"
df_tot = pd.read_sql_query(query_tot, connection, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

#GROUP QUERIES
query_samehit = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NOT NULL AND ch.hit_rfam_acc IS NOT NULL AND uc.rfam_acc = ch.hit_rfam_acc"
query_confhit = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NOT NULL AND ch.hit_rfam_acc IS NOT NULL AND uc.rfam_acc != ch.hit_rfam_acc"
query_lostscan = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NOT NULL AND ch.hit_rfam_acc IS NULL"
query_newmem = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NULL AND ch.hit_rfam_acc IS NOT NULL"
query_newfam = "SELECT ur.id, ur.len, uc.db, uc.rna_type, uc.rfam_acc, uc.tax_id, ch.hit_rfam_acc, ch.hit_clan_acc, ch.e_value FROM urs_rnacentral ur LEFT JOIN cmscan_run cr ON ur.id = cr.id LEFT JOIN urs_condensed uc ON ur.id = uc.id LEFT JOIN cmscan_hits ch ON ur.id = ch.id WHERE cr.id IS NOT NULL AND uc.rfam_acc IS NULL AND ch.hit_rfam_acc IS NULL"

#DATAFRAMES
df_samehit = pd.read_sql_query(query_samehit, connection, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)
df_confhit = pd.read_sql_query(query_confhit, connection, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)
df_lostscan = pd.read_sql_query(query_lostscan, connection, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)
df_newmem = pd.read_sql_query(query_newmem, connection, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)
df_newfam = pd.read_sql_query(query_newfam, connection, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

#TO SEPARATE GROUP CONFLICTING HITS COUNT
query_colapsedhits = "SELECT ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families FROM cmscan_hits ch GROUP BY ch.id"
df_colapsedhits = pd.read_sql_query(query_colapsedhits, connection, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None)

mask = (df_colapsedhits['families'].str.len() > 7)
doublehit_list = df_colapsedhits.loc[mask]

#GRAPHS
#ALL

dict_allgroups = {"Same hit": len(df_tot) - len(doublehit_list) - len(df_lostscan) - len(df_newmem) - len(df_newfam),
		"Conflicting hits": len(doublehit_list),
		"Lost in scan": len(df_lostscan),
		"New members": len(df_newmem),
		"New families": len(df_newfam)
		}

labels = dict_allgroups.keys()
values = dict_allgroups.values()
bupu = cl.scales['5']['seq']['PuBuGn']

data = Data([
    Pie(
        domain=dict(
            x=[0, 1],
            y=[0, 1]
        ),
        hoverinfo='value',
        labels=labels,
        marker=Marker(
            colors=bupu,
            line=Line(
                width=0
            )
        ),
        name='N',
        pull=0,
        rotation=360,
        showlegend=False,
        sort=True,
        textinfo='label+percent',
        textposition='outside',
        uid='186130',
        values=values
    )
])
layout = Layout(
    autosize=True,
    height=633,
    title='URS per group',
    width=1332
)
fig = Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='my-graph.html')


