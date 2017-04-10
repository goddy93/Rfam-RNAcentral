import pandas as pd

TBL_PATH = "/Users/nquinones/Dropbox/EMBL-EBI/Rfam-RNAcentral/new_fams/nhmmer_approach2/files/above40sorted.tsv"

sort = pd.read_table(
    TBL_PATH)


def group(g_input):
    sel = sort[sort["group"] == g_input]
    print sel


def init():
    print ""
    print "Which group to fetch"
    print "[integer/exit]"
    input1 = raw_input(">")
    input1 = str(input1)
    if input1.isdigit() == True:
        number = int(input1)
        group(number)
        init()
    elif input1 == "exit":
        "Ok, bye."
        exit()
    elif input1.isdigit() == False:
        print "Invalid input. Try again."
        init()

init()
