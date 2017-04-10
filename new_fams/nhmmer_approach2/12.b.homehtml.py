import pandas as pd
import sys

# ..............PATHS...............
TABLE_PATH = sys.argv[1]
OUT_HTML = "./HOME.html"
ALIPATH = sys.argv[2]

pd.set_option('max_colwidth', -1)

# ..............PROCESS..............
MAIN_TBL = pd.read_csv(TABLE_PATH, sep="\t", header=0)
del MAIN_TBL.index.name
MAIN_TBL["num_seq"] = MAIN_TBL["num_seq"].astype(int)
MAIN_TBL["alen"] = MAIN_TBL["alen"].astype(int)
MAIN_TBL["avlen"] = MAIN_TBL["avlen"].astype(int)
MAIN_TBL["avid"] = MAIN_TBL["avid"].astype(int)
MAIN_TBL["avid"] = MAIN_TBL["avid"].astype(str) + "%"
MAIN_TBL["name"] = MAIN_TBL["name"].str.replace(r"\[subseq from\]", "")
MAIN_TBL["path"] = MAIN_TBL["file"].str.replace(r".cl.sto", "").astype(str)
MAIN_TBL["path"] = MAIN_TBL["path"].str.replace(r".sto", "").astype(str)
MAIN_TBL["path"] = ALIPATH + "/" + MAIN_TBL["path"] + "/" + MAIN_TBL["file"].astype(str) + ".html"

MAIN_TBL["file"] = "<a href=\"" + MAIN_TBL["path"] + "\">" + MAIN_TBL["file"] + "</a>"
del MAIN_TBL["path"]
MAIN_TBL.columns = ["Alignment",
                    "Selected description",
                    "Number of<br>sequences",
                    "Alignment<br>length",
                    "Avg. sequence<br>length",
                    "Lengths<br>ratio",
                    "Avg. id",
                    "Number of<br>publications",
                    "Number of<br>databases",
                    "RNAcode<br>warning",
                    "R-scape<br>sig."]


MAIN_TBL_HTML = MAIN_TBL.to_html(header=True, index=False, escape=False, classes='sortable')


# ..HTML FILE
# ....Settings
HEADER = """
<html>
    <head>
        <title>autoRfam</title>
        <script src="./sorttable.js"></script>
    </head>
"""
BODY = """
    <body style="font-family:'helvetica';
                 margin-top: 1%;
                 margin-bottom: 1%;
                 margin-right: 4%;
                 margin-left: 2%;"
          link="#3366BB"
          vlink="#663366">
"""

STYLE = """
  <style>
      h1{color: #7a0606;
         font-family: helvetica;
         font-weight:normal;
         font-size: 350%}
      h2, h3 {color: #822424;
              font-family: helvetica;
              font-weight:normal;
              display: inline;}
     .df
         th {text-align: left;
             background-color: #822424;
             color: white;
             font-family:helvetica;}
         table {border-collapse: collapse;}
         table, th, td {border: 1px solid black;
                        font-family: monospace;
                        text-align: right;
                        font-size:12px;
                        font-weight:normal;
                        padding:5px 10px;
                        white-space: nowrap;
                        border-style:solid;
                        border-width:1px;}
        tr:hover {background-color: #e8e5e5}

    table.sortable th {text-align: left;
                       background-color: #822424;
                       color: white;
                       font-family:helvetica;}
                   th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after { 
    content: ' \\25B9'}
  </style>
"""

FOOTER = """
    </body>
</html>
"""

# ....Writing HTML File
with open(OUT_HTML, 'w') as f:
    f.write(HEADER)
    f.write(BODY)
    f.write(STYLE)
    f.write("\n")
    f.write("<div align='right'>\n")
    f.write("<font size='2' color='grey'>")
    f.write("[ <a href='./help.html'>help</a> ]&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;browse alignments")
    f.write("</font>\n")
    f.write("</div>\n")
    f.write("<h1>autoRfam\n")
    f.write("    <font size='5' color='grey'>\n")
    f.write("        <i>BROWSE ALIGNMENTS</i>\n")
    f.write("    </font>\n")
    f.write("</h1>\n")
    f.write("<br>\n")
    f.write(MAIN_TBL_HTML+"\n")
    f.write(FOOTER)
