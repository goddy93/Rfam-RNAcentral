import re
import requests
import pandas as pd
import os
import sys

# ..............PATHS...............
STOPATH = sys.argv[1]
OUT_HTML = STOPATH + ".html"
ALINAME = os.path.basename(STOPATH)
ALISTAT_PATH = "/Users/nquinones/Documents/hmmer-3.1b2/easel/miniapps/esl-alistat"

# ..............PARAMS...............#=GS\sURS.{10}\/.*DE\s
TIME_OUT = 10
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
DESC_TBL["seq_num"] = DESC_TBL.index
# ........join description and xrefs tables
FULL_TBL = DESC_TBL.set_index("urs").join(XREFS_TBL.set_index("urs"))
# ........clean
FULL_TBL_OUT = FULL_TBL[["seq_num", "urs_link", "description", "db_link", "rna_type", "product", "tax_id", "species"]]
FULL_TBL_OUT = FULL_TBL_OUT.set_index(["seq_num"])
FULL_TBL_OUT = FULL_TBL_OUT.sort_index()
del FULL_TBL_OUT.index.name
# ........to html
FULL_TBL_OUT_HTML = FULL_TBL_OUT.to_html(header=True, index=True, escape=False, classes='df')

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
    </head>
    <body>
""" % ALINAME

STYLE = """
<style>
h1{color: #7a0606;
    font-family: helvetica;
    font-size: 300%}
h2, h3 {color: #822424;
    font-family: helvetica;}
p  {font-family: helvetica;}

.df
    th {text-align: left;
        background-color: #822424;
        color: white;
        font-family:helvetica;}
    table {border-collapse: collapse;}
    table, th, td {border: 1px solid black;
                  font-family:monospace;
                  font-size:12px;
                  padding:5px 10px;
                  border-style:solid;
                  border-width:1px;}
    tr:hover {background-color: #e8e5e5}
</style>
"""

FOOTER = """
    </body>
</html>
"""

# ....Writing File
with open(OUT_HTML, 'w') as f:
    f.write(HEADER)
    f.write(STYLE)
    f.write("<h1>ALIGNMENT <b>%s</b></h1>" % ALINAME)
    f.write("<h2>Alignment statistics</h2>")
    f.write(EASEL_TBL_HTML)
    f.write("<h2>Publications</h2>")
    f.write(PUB_TBL_HTML)
    f.write("<h2>Database annotations</h2>")
    f.write(DBANNOT_TBL_HTML)
    f.write("<h2>RNA type annotations</h2>")
    f.write(TYPEANNOT_TBL_HTML)
    f.write("<br>")
    f.write("<h2>Full information</h2>")
    f.write(FULL_TBL_OUT_HTML)
    f.write(FOOTER)
