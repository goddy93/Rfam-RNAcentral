import pandas as pd
from collections import OrderedDict
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

slicedpiechart = "./test.html"

# -----Sliced plot
# .....Data..... (see consistenct_check/for_article)
dict_allgroups = OrderedDict([
    ("<b>With Rfam annotation:<br>inconsistent matches</b>", 123542),
    ("<b>With Rfam annotation:<br>consistent matches</b>", 4592888),
    ("<b>New Rfam matches</b>", 3696474),
    ("<b>Not suitable for Rfam</b>", 490390),
    ("<b>Undetected tRNA, rRNA and tmRNA</b>", 319156),
    ("<b>Potential new Rfam families</b>", 163567)
        ])


labels = dict_allgroups.keys()
values = dict_allgroups.values()


dict_colors = OrderedDict([
    ("<b>Rfam annotation:<br>unexpected or no match</b>", "rgb(119,9,11)"),
    ("<b>Rfam annotation:<br>consistent match</b>", "rgb(215,25,29)"),
    ("<b>New Rfam matches</b>", "rgb(19,46,131)"),
    ("<b>Not suitable for Rfam</b>", "rgb(40,70,75)"),
    ("<b>Undetected tRNA, rRNA and tmRNA</b>", "rgb(11,122,117)"),
    ("<b>Potential new families</b>", "rgb(112,193,179)")
        ])

#.....Graph.....
data = Data([
    Pie(
        domain = dict(
            x = [0, 1],
            y = [0, 1]
        ),
        direction="clockwise",
        hole="0.5",
        hoverinfo='value',

        sort=False,
        labels=labels,
        marker=Marker(
            colors=dict_colors.values(),
            line=Line(
                width=1.5,
                color="rgb(255, 255, 255)"
            )
        ),
        pull = 0,
        rotation = 179,
        showlegend = False,
        textfont={"size":12},
        textinfo = 'label+percent',
        textposition = 'outside',
        values = values
    )
])
layout = Layout(
    autosize = True,
    margin = Margin(
        t = 80,
        b = 80,
    ),
    height = 633,
    width = 1332
)
fig = Figure(data = data, layout=layout)

plotly.offline.plot(fig, filename=slicedpiechart)
