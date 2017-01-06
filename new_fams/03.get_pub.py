import pandas as pd
import requests

eunewfam_in = "./files/df_eunewfam"
eunewfam_pub_out = "./files/df_eunewfam.pub"

# read full new family file
df_eunewfam = pd.read_table(
  eunewfam_in,
  low_memory=False,
  sep="\t"
  )

# make lists with urs
eunewfam_list = df_eunewfam["id"].tolist()


def pubmed_id(urs_list, page_size, time_out):
    f = open(eunewfam_pub_out, "w")
    # write header
    f.write("URS\tpubmed_id\tpub_id\n")
    # search for each
    for i in urs_list:
        url = "http://rnacentral.org/api/v1/rna/"+i+"/publications?page_size="+str(page_size)
        try:
            r = requests.get(url, timeout=time_out)
            data = r.json()
            a = len(data["results"])
            for j in range(0, a):
                pubmed = str(data['results'][j]["pubmed_id"])
                pubid = str(data['results'][j]["pub_id"])
                f.write(i+"\t"+pubmed+"\t"+pubid+"\n")
            if a != data["count"]:
                f.write(i+"\t"+"err("+str(page_size)+"+)"+"\t"+"err("+str(page_size)+"+)"+"\n")
        except requests.exceptions.Timeout:
            f.write(i+"\terr(timeout)\terr(timeout)\n")
    f.close()

pubmed_id(eunewfam_list, 50, 10)
