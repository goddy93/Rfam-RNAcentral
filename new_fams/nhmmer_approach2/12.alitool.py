import re
import requests
import pandas as pd
import os
import sys
import glob

# ..............PATHS...............
STOPATH = sys.argv[1]
OUT_HTML = STOPATH + ".html"
# OUT_TBL = "/nfs/production/xfam/users/nataquinones/auto_rfam/tables/TBL_selali.tsv"
OUT_TBL = sys.argv[2]
ALINAME = os.path.basename(STOPATH)
# ALISTAT_PATH = "/nfs/production/xfam/rfam/rfam_rh7/software/bin/esl-alistat"
ALISTAT_PATH = "/Users/nquinones/Documents/hmmer-3.1b2/easel/miniapps/esl-alistat"

# ..............PARAMS...............
TIME_OUT = 60
PUBLICATIONS_PAGESIZE = 10
pd.set_option('max_colwidth', -1)

# .............FUNCTIONS.............


def ali_parse(stopath):
    """
    Takes stockholm file and extracts sequence name
    and description into lists
    """
    readfile = open(stopath, "r")
    read = readfile.read()
    readfile.close()
    urs = re.findall(r"(?<=#=GS\s)(URS.{10})", read)
    desc = re.findall(r"(?<=DE\s)(.*)", read)
    return urs, desc


def request_xrefs(urs):
    """
    Takes list of urs, fetches urs info from RNAcentral
    """
    databases = pd.DataFrame()
    # fetch xrefs info for each urs
    for i in urs:
        urlxrefs = "http://rnacentral.org/api/v1/rna/%s/xrefs" % i
        try:
            req = requests.get(urlxrefs, timeout=TIME_OUT)
            data = req.json()
            # fetch the relevant parameters per xref
            num_db = len(data["results"])
            for j in range(0, num_db):
                # values for table
                urs_link = "<a href=\"http://rnacentral.org/rna/%s\" target=\"_blank\">%s</a>" % (i, i)
                db_name = str(data["results"][j]["database"])
                if data["results"][j]["is_expert_db"] == True:
                    source_url = str(data["results"][j]["accession"]["expert_db_url"])
                else:
                    source_url = str(data["results"][j]["accession"]["source_url"])
                db_link = "<a href=\"%s\" target=\"_blank\">%s</a>" % (source_url, db_name)
                rna_type = str(data["results"][j]["accession"]["rna_type"])
                product = str(data["results"][j]["accession"]["product"])
                taxid = str(data["results"][j]["taxid"])
                species = str(data["results"][j]["accession"]["species"])
                # write into line
                line = [[i,
                         urs_link,
                         db_name,
                         db_link,
                         rna_type,
                         product,
                         taxid,
                         species]]
                # append line into df
                databases = databases.append(line)

        # if timeout, add line indicating it
        except requests.exceptions.Timeout:
            line = [[i,
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout",
                     "timeout"]]
            databases = databases.append(line)
    # add column names
    databases.columns = ["urs",
                         "urs_link",
                         "db",
                         "db_link",
                         "rna_type",
                         "product",
                         "tax_id",
                         "species"]
    # clean and return
    databases = databases.reset_index(drop=True)
    return databases


def request_pub(urs):
    """
    Takes list of urs, fetches publication info from RNAcentral
    """
    publications = pd.DataFrame()
    # fetch publication info for each urs
    for i in urs:
        urlpubs = "http://rnacentral.org/api/v1/rna/%s/publications?page_size=%i" % (i, PUBLICATIONS_PAGESIZE)
        try:
            req = requests.get(urlpubs, timeout=TIME_OUT)
            data = req.json()
            # fetch the relevant parameters publication
            num_ref = len(data["results"])
            for j in range(0, num_ref):
                # values for table
                pubmed = str(data['results'][j]["pubmed_id"])
                title = str(data['results'][j]["title"])
                # write into line
                line = [[i,
                         pubmed,
                         title]]
                # only append if it has a pubmed id
                if str(data['results'][j]["pubmed_id"]) != "None":
                    publications = publications.append(line)
        # if timeout, add line indicating it
        except requests.exceptions.Timeout:
            line = [[i, "timeout", "timeout"]]
            publications = publications.append(line)
    # .. add tables titles
    if len(publications) != 0:
        publications.columns = ["urs", "pubmed_id", "title"]
        publications = publications.drop_duplicates("pubmed_id")
        publications = publications[["pubmed_id", "title"]]
    return publications


def make_alistatsum():
    """
    Takes alignment file and calculates easel stats
    """
    ex_string = ALISTAT_PATH + " --rna " + STOPATH
    b = os.popen(ex_string).readlines()
    values = []
    # extract last element which corresponds to value
    for line in b:
        values.append(line.split()[-1])
    num_seq = int(values[2])
    alen = int(values[3])
    diff = int(values[6]) - int(values[5])
    avlen = float(values[7])
    lenalen_ratio = avlen / alen
    avid = int(values[8].strip("%"))
    easelstats = pd.DataFrame([num_seq,
                               alen,
                               diff,
                               avlen,
                               round(lenalen_ratio, 2),
                               avid], dtype=object)
    easelstats["in"] = ["Number of sequences",
                        "Alignment length",
                        "Max-Min lengths",
                        "Avg. length",
                        "Length-Alignment length ratio",
                        "Avg. per. id"]
    easelstats = easelstats.set_index("in")
    del easelstats.index.name
    return easelstats


# ..............PROCESS..............
# ..STOCKHOLM FILE PARSE
URS = ali_parse(STOPATH)[0]
DESC = ali_parse(STOPATH)[1]

# ..TABLES
# ....Full Sequences Table
# ........requests
XREFS_TBL = request_xrefs(URS)
# ........description table
DESC_TBL = pd.DataFrame()
DESC_TBL["urs"] = URS
DESC_TBL["description"] = DESC
DESC_TBL.index += 1
DESC_TBL["seq"] = DESC_TBL.index
# ........join description and xrefs tables
FULL_TBL = DESC_TBL.set_index("urs").join(XREFS_TBL.set_index("urs"))
# ........clean
FULL_TBL_OUT = FULL_TBL[["seq", "urs_link", "description", "db_link", "rna_type", "product", "tax_id", "species"]]
FULL_TBL_OUT = FULL_TBL_OUT.set_index(["seq"])
FULL_TBL_OUT = FULL_TBL_OUT.sort_index()
FULL_TBL_OUT.reset_index(level=0, inplace=True)

# ........to html
FULL_TBL_OUT_HTML = FULL_TBL_OUT.to_html(header=True, index=False, escape=False, classes='sortable')

# ....Easel Stats Table
# ........generate
EASEL_TBL = make_alistatsum()
# ........to html
EASEL_TBL_HTML = EASEL_TBL.to_html(header=False, index=True, escape=False, classes='df')

# ....Publications Table
# ........request
PUB_TBL = request_pub(URS)
# ........to html
PUB_TBL_HTML = PUB_TBL.to_html(header=True, index=False, escape=False, classes='df')

# ....DB Annotation Table
# ........generate
DBANNOT_TBL = pd.DataFrame(XREFS_TBL["db"].value_counts())
# ........to html
DBANNOT_TBL_HTML = DBANNOT_TBL.to_html(header=False, index=True, escape=False, classes='df')

# ....Type Annotation Table
# ........generate
TYPEANNOT_TBL = pd.DataFrame(XREFS_TBL["rna_type"].value_counts())
# ........to html
TYPEANNOT_TBL_HTML = TYPEANNOT_TBL.to_html(header=False, index=True, escape=False, classes='df')

# ..HTML FILE
# ....Settings
HEADER = """
<html>
    <head>
        <title>%s</title>
        <script src="../../sorttable.js"></script>
    </head>
""" % ALINAME
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
                        font-size:12px;
                        font-weight:normal;
                        padding:5px 10px;
                        border-style:solid;
                        border-width:1px;}
        tr:hover {background-color: #e8e5e5}

    table.sortable th {text-align: left;
                       background-color: #822424;
                       color: white;
                       font-weight: normal;
                       font-family:helvetica;}
    table.sortable th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after { 
    content: ' \\25B9'}
  </style>
"""

FOOTER = """
    </body>
</html>
"""
# ....Other links
BROWSE_ALI = "../../HOME.html"

# ..RNAcode and RSCAPE
# ....RNAcode for table
RNACODE_PATH = "./rnacode/rnacode"
if os.path.isdir(RNACODE_PATH):
    CODINGWARN = "Yes"
else:
    CODINGWARN = "No"
# ....Rscape for table
RSCAPE_OUT_FILE = os.path.splitext(ALINAME)[0]+".out"
RSCAPE_OUT_PATH = os.path.join("./rscape/", RSCAPE_OUT_FILE)
if os.stat(RSCAPE_OUT_PATH).st_size != 0:
    if len(glob.glob("./rscape/*.cyk.R2R.sto.svg")) != 0:
        RSCAPEWARN = "Yes"
    else:
        RSCAPEWARN = "No"
else:
    RSCAPEWARN = "No"
# ....RNAcode for html
if CODINGWARN == "Yes":
    RNACODE_MSG = "<b>WARNING!</b> This alignment has coding potential. <font size='2' color='grey'> <a href=\"./rnacode/rnacode/\"><i>[Explore RNAcode results]</i></a></font>\n"
else:
    RNACODE_MSG = "No coding potential found. <font size='2' color='grey'> <a href=\"./rnacode/\"><i>[Explore RNAcode results]</i></a></font>\n"
# ....Rscape for html
if len(glob.glob("./rscape/*.cyk.R2R.sto.svg")) != 0:
    IMG_PATH = os.path.join(".", glob.glob("./rscape/*.cyk.R2R.sto.svg")[0])
    RSCAPE_IMG = "<img src=%s>" % IMG_PATH
else:
    RSCAPE_IMG = "R-scape image not available"



# ....Writing HTML File
with open(OUT_HTML, 'w') as f:
    f.write(HEADER)
    f.write(BODY)
    f.write(STYLE)
    f.write("\n")
    f.write("<div align='right'>\n")
    f.write("<font size='2' color='grey'>")
    f.write("<a href='%s'>browse alignments</a> > alignment %s \n" % (BROWSE_ALI, ALINAME))
    f.write("</font>\n")
    f.write("</div>\n")
    f.write("<h1>autoRfam\n")
    f.write("    <font size='5' color='grey'>\n")
    f.write("        <i>alignment %s</i>\n" % ALINAME)
    f.write("    </font>\n")
    f.write("</h1>\n")
    f.write("<br>\n")
    f.write("<div style='margin-left:2%'>\n")
    f.write("<h2>Alignment statistics</h2>\n")
    f.write("<hr />\n")
    f.write(EASEL_TBL_HTML + "\n")
    f.write("<br>\n")
    f.write("<br>\n")
    f.write("<h2>Publications</h2>\n")
    f.write("<hr />\n")
    f.write(PUB_TBL_HTML + "\n")
    f.write("<br>\n")
    f.write("<br>\n")
    f.write("<h2>Database annotations</h2>\n")
    f.write("<hr />\n")
    f.write(DBANNOT_TBL_HTML + "\n")
    f.write("<br>\n")
    f.write("<br>\n")
    f.write("<h2>RNA type annotations</h2>\n")
    f.write("<hr />\n")
    f.write(TYPEANNOT_TBL_HTML + "\n")
    f.write("<br>\n")
    f.write("<br>\n")
    f.write("<h2>RNAcode</h2>\n")
    f.write("<hr />\n")
    f.write(RNACODE_MSG)
    f.write("<br>\n")
    f.write("<br>\n")
    f.write("<br>\n")
    f.write("<h2>R-scape</h2>\n")
    f.write("<hr />\n")
    f.write(RSCAPE_IMG + "\n")
    f.write("<br> \n")
    f.write("<font size='2' color='grey'>")
    f.write("    <i><a href=\"./rscape/\">[Explore R-scape results]</a></i>\n")
    f.write("</font>")
    f.write("<br> \n")
    f.write("<br>\n")
    f.write("<br>\n")
    f.write("<h2>Full information</h2> \n")
    f.write("<hr />\n")
    f.write("<font size='2' color='grey'>")
    f.write("    <i><a href=\"file:%s.txt\">[Explore alignment file]</a></i>\n" %STOPATH)
    f.write("</font>")
    f.write("<br>\n")
    f.write("<br>\n")
    f.write(FULL_TBL_OUT_HTML + "\n")
    f.write("</div>")
    f.write(FOOTER)

# ....Writing table File
F_FILE = ALINAME
F_NAME = DESC[0]
F_NUM_SEQ = EASEL_TBL[0][0]
F_ALEN = EASEL_TBL[0][1]
F_AVLEN = EASEL_TBL[0][3]
F_LENALEN_RATIO = EASEL_TBL[0][4]
F_AVID = EASEL_TBL[0][5]
F_NUM_PUB = len(PUB_TBL)
F_NUM_DB = len(DBANNOT_TBL)
F_CODINGWARN = CODINGWARN
F_RSCAPE = RSCAPEWARN

LINE = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (F_FILE,
                                                         F_NAME,
                                                         F_NUM_SEQ,
                                                         F_ALEN,
                                                         F_AVLEN,
                                                         F_LENALEN_RATIO,
                                                         F_AVID,
                                                         F_NUM_PUB,
                                                         F_NUM_DB,
                                                         F_CODINGWARN,
                                                         F_RSCAPE)

with open(OUT_TBL, 'a') as f:
    f.write(LINE)
    f.close()
