import pandas as pd
import requests

eunewfam_in = "./files/df_eunewfam"
pseudonewfam_in = "./files/df_pseudonewfam"
eunewfam_pub_out = "./files/df_eunewfam.pub"
pseudonewfam_pub_out = "./files/df_pseudonewfam.pub"

# read full new family file
df_eunewfam = pd.read_table(
  eunewfam_in,
  low_memory=False,
  sep="\t"
  )

df_pseudonewfam = pd.read_table(
  pseudonewfam_in,
  low_memory=False,
  sep="\t"
  )

# make lists with urs
eunewfam_list = df_eunewfam["id"].tolist()
pseudonewfam_list = df_pseudonewfam["id"].tolist()

# make FASTA file with all the sequences in a list


def pubmed_id(urs_list):
    df2 = pd.DataFrame()
    for i in urs_list:
        pubmed_ids = []
        pub_ids = []
        url = "http://rnacentral.org/api/v1/rna/"+i+"/publications?page_size=50"
        r = requests.get(url, timeout=10)
        data = r.json()
        a = len(data["results"])
        # make df
        urss = [i] * a
        for j in range(0, a):
            pubmed_ids.append(data['results'][j]["pubmed_id"])
        for j in range(0, a):
            pub_ids.append(data['results'][j]["pub_id"])
        df = pd.DataFrame(urss)
        df.columns = ["URS"]
        df["pubmed_id"] = pubmed_ids
        df["pub_id"] = pub_ids
        df2 = df2.append(df)
        # check if count
        if a != data["count"]:
          df2.loc[-1] = [i, "50+", "50+"]
        # reset index
        df2.reset_index(drop=True, inplace=True)
    return df2

# run function for both lists and save tables to csvs
df_pub = pubmed_id(eunewfam_list)
df_pub.to_csv(eunewfam_pub_out, sep="\t", na_rep="None", header=True, index=False)
#pubmed_id(pseudonewfam_list).to_csv(pseudonewfam_pub_out, sep="\t", na_rep="None", header=True, index=False)
