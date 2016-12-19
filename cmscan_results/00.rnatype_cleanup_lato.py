import pandas as pd

#------Output files----
df_c_samehit = "./clean_tables/lato/df_samehit"
df_c_confhit = "./clean_tables/lato/df_confhit"
df_c_lostscan = "./clean_tables/lato/df_lostscan"
df_c_newmem = "./clean_tables/lato/df_newmem"
df_c_newfam = "./clean_tables/lato/df_newfam"

#------Query files----
query_samehit = "./query_files/query_samehit"
query_confhit = "./query_files/query_confhit"
query_lostscan = "./query_files/query_lostscan"
query_newmem = "./query_files/query_newmem"
query_newfam = "./query_files/query_newfam"

#------Dataframes-----
df_samehit = pd.read_table(
    query_samehit,
    sep="\t",
    names=["id", "len", "db", "rna_type", "rfam_acc", "tax_id", "hit_rfam_acc", "hit_clan_acc", "e_value"]
    )

df_confhit = pd.read_table(
    query_confhit,
    sep="\t",
    names=["id", "len", "db", "rna_type", "rfam_acc", "tax_id", "hit_rfam_acc", "hit_clan_acc", "e_value"]
    )

df_lostscan = pd.read_table(
    query_lostscan,
    sep="\t",
    names=["id", "len", "db", "rna_type", "rfam_acc", "tax_id", "hit_rfam_acc", "hit_clan_acc", "e_value"]
    )

df_newmem = pd.read_table(
    query_newmem,
    sep="\t",
    names=["id", "len", "db", "rna_type", "rfam_acc", "tax_id", "hit_rfam_acc", "hit_clan_acc", "e_value"]
    )

df_newfam = pd.read_table(
    query_newfam,
    sep="\t",
    names=["id", "len", "db", "rna_type", "rfam_acc", "tax_id", "hit_rfam_acc", "hit_clan_acc", "e_value"]
    )

#------rna_type cleanup-----
rnatype_cleanup = {
    "rRNA":"rRNA",
    "tRNA":"tRNA",
    "piRNA":"piRNA",
    "lncRNA":"lncRNA",
    "misc_RNA":"other",
    "other":"other",
    "miRNA":"miRNA",
    "SRP_RNA":"SRP_RNA",
    "snRNA":"snRNA",
    "snoRNA":"snoRNA",
    "siRNA":"siRNA",
    "hammerhead":"hammerhead",
    "precursor_":"precursor",
    "antisense_":"antisense",
    "RNase_P_RN":"RNase_P_RN",
    "lncRNA,antisense_":"lncRNA",
    "antisense_,lncRNA":"lncRNA",
    "piRNA,misc_RNA":"piRNA,other",
    "tmRNA":"tmRNA",
    "misc_RNA,piRNA":"piRNA",
    "tmRNA,other":"tmRNA",
    "ribozyme":"ribozyme",
    "autocataly":"autocataly",
    "scRNA":"scRNA",
    "miRNA,precursor_":"miRNA",
    "other,misc_RNA":"other",
    "RNase_MRP_":"RNase_MRP",
    "rRNA,misc_RNA":"rRNA",
    "vault_RNA":"vault_RNA",
    "precursor_,miRNA":"miRNA",
    "siRNA,snRNA":"siRNA,snRNA",
    "misc_RNA,rRNA":"rRNA",
    "snRNA,siRNA":"siRNA,snRNA",
    "misc_RNA,other":"other",
    "rasiRNA":"rasiRNA",
    "other,tmRNA":"tmRNA",
    "telomerase":"telomerase",
    "snoRNA,misc_RNA":"snoRNA",
    "miRNA,misc_RNA":"miRNA",
    "other,lncRNA":"lncRNA",
    "RNase_P_RN,misc_RNA":"RNase_P_RN",
    "snoRNA,snRNA":"snRNA,snoRNA",
    "misc_RNA,RNase_P_RN":"RNase_P_RN",
    "miRNA,siRNA":"miRNA,siRNA",
    "precursor_,misc_RNA":"other",
    "guide_RNA":"guide_RNA",
    "misc_RNA,snoRNA":"snoRNA",
    "other,antisense_":"other",
    "antisense_,other":"other",
    "lncRNA,other":"lncRNA",
    "rRNA,precursor_":"rRNA",
    "precursor_,rRNA":"rRNA",
    "snRNA,snoRNA":"snRNA,snoRNA",
    "tmRNA,misc_RNA":"tmRNA",
    "SRP_RNA,misc_RNA":"SRP_RNA",
    "misc_RNA,miRNA":"miRNA",
    "antisense_,misc_RNA":"other",
    "siRNA,miRNA":"miRNA,siRNA",
    "snoRNA,lncRNA":"lncRNA,snoRNA",
    "misc_RNA,precursor_":"other",
    "tmRNA,other,misc_RNA":"tmRNA",
    "other,snRNA":"snRNA",
    "SRP_RNA,scRNA":"scRNA,SRP_RNA",
    "tRNA,rRNA":"rRNA,tRNA",
    "miRNA,piRNA":"miRNA,piRNA",
    "tRNA,misc_RNA":"tRNA",
    "lncRNA,snoRNA":"lncRNA,snoRNA",
    "miRNA,precursor_,misc_RNA":"miRNA",
    "misc_RNA,SRP_RNA":"SRP_RNA",
    "tmRNA,misc_RNA,other":"tmRNA",
    "rRNA,other":"rRNA",
    "telomerase,misc_RNA":"telomerase",
    "snRNA,other":"snRNA",
    "tRNA,other":"tRNA",
    "misc_RNA,telomerase":"telomerase",
    "lncRNA,misc_RNA":"lncRNA",
    "miRNA,siRNA,snRNA":"other",
    "hammerhead,misc_RNA":"hammerhead",
    "snRNA,misc_RNA":"snRNA",
    "other,rRNA":"rRNA",
    "other,scRNA":"scRNA",
    "miRNA,misc_RNA,precursor_":"miRNA",
    "other,tmRNA,misc_RNA":"tmRNA",
    "snoRNA,other":"snoRNA",
    "other,antisense_,misc_RNA":"other",
    "scRNA,SRP_RNA":"scRNA,SRP_RNA",
    "antisense_,other,misc_RNA":"other",
    "misc_RNA,tmRNA,other":"other",
    "SRP_RNA,lncRNA":"lncRNA,SRP_RNA",
    "scRNA,other":"scRNA",
    "misc_RNA,antisense_":"other",
    "precursor_,miRNA,misc_RNA":"miRNA",
    "antisense_,misc_RNA,other":"other",
    "ribozyme,hammerhead":"ribozyme",
    "other,tRNA":"tRNA",
    "misc_RNA,hammerhead":"hammerhead,other",
    "rRNA,tRNA":"rRNA,tRNA",
    "RNase_P_RN,other":"RNase_P_RN",
    "lncRNA,SRP_RNA":"lncRNA,SRP_RNA",
    "other,snoRNA":"snoRNA",
    "snoRNA,miRNA":"miRNA,snoRNA",
    "other,Y_RNA":"Y_RNA,other",
    "scRNA,other,misc_RNA":"scRNA",
    "other,misc_RNA,antisense_":"other",
    "other,RNase_P_RN":"RNase_P_RN",
    "misc_RNA,guide_RNA,snoRNA":"other",
    "SRP_RNA,snRNA":"snRNA,SRP_RNA",
    "snRNA,RNase_MRP_":"RNase_MRP,other",
    "hammerhead,ribozyme":"ribozyme",
    "snoRNA,snRNA,lncRNA":"other",
    "miRNA,snoRNA":"miRNA,snoRNA",
    "RNase_P_RN,lncRNA":"lncRNA,RNase_P_RN",
    "misc_RNA,ribozyme":"ribozyme,other",
    "other,misc_RNA,scRNA":"scRNA",
    "vault_RNA,misc_RNA":"vault_RNA,other",
    "vault_RNA,scRNA":"vault_RNA,scRNA",
    "misc_RNA,miRNA,precursor_":"miRNA",
    "misc_RNA,antisense_,other":"other",
    "precursor_,misc_RNA,miRNA":"miRNA",
    "other,scRNA,misc_RNA":"scRNA",
    "snoRNA,snRNA,guide_RNA":"other",
    "SRP_RNA,other":"SRP_RNA",
    "other,misc_RNA,tmRNA":"tmRNA",
    "other,SRP_RNA":"SRP_RNA",
    "snoRNA,lncRNA,snRNA":"other",
    "tRNA,antisense_":"tRNA",
    "lncRNA,RNase_P_RN":"lncRNA,RNase_P_RN",
    "snoRNA,misc_RNA,other":"snoRNA",
    "scRNA,vault_RNA":"scRNA,vault_RNA",
    "snoRNA,guide_RNA":"guide_RNA,snoRNA",
    "scRNA,snRNA":"scRNA,snRNA",
    "snRNA,lncRNA":"lncRNA,snRNA",
    "RNase_MRP_,snRNA":"RNase_MRP,snRNA",
    "snoRNA,misc_RNA,snRNA":"snRNA,snoRNA",
    "snoRNA,guide_RNA,snRNA":"snRNA,snoRNA",
    "misc_RNA,scRNA,other":"scRNA",
    "misc_RNA,snRNA":"snRNA",
    "misc_RNA,other,antisense_":"other",
    "snoRNA,piRNA":"piRNA,snoRNA",
    "other,scRNA,rRNA":"other",
    "tRNA,precursor_":"tRNA",
    "snRNA,snoRNA,guide_RNA":"other",
    "scRNA,Y_RNA,other":"other",
    "scRNA,rRNA":"rRNA,scRNA",
    "snRNA,SRP_RNA":"snRNA,SRP_RNA",
    "miRNA,precursor_,lncRNA":"other",
    "snoRNA,lncRNA,snRNA,guide_RNA":"other",
    "other,miRNA":"miRNA",
    "RNase_P_RN,misc_RNA,other":"RNase_P_RN",
    "other,misc_RNA,rRNA":"rRNA",
    "scRNA,other,Y_RNA":"other",
    "telomerase,lncRNA":"lncRNA,telomerase",
    "other,antisense_,lncRNA":"lncRNA",
    "other,snoRNA,misc_RNA":"snoRNA",
    "snoRNA,lncRNA,guide_RNA":"other",
    "snRNA,miRNA":"miRNA,snRNA",
    "miRNA,precursor_,misc_RNA,lncRNA":"other",
    "lncRNA,snoRNA,guide_RNA,snRNA":"other",
    "snoRNA,snRNA,misc_RNA":"snRNA,snoRNA",
    "RNase_MRP_,RNase_P_RN":"RNase_MRP,RNase_P_RN",
    "ribozyme,misc_RNA":"ribozyme,other",
    "guide_RNA,snoRNA,lncRNA,snRNA":"other",
    "snRNA,misc_RNA,snoRNA":"snRNA,snoRNA",
    "snoRNA,guide_RNA,snRNA,lncRNA":"other",
    "snRNA,lncRNA,snoRNA":"other",
    "snRNA,SRP_RNA,scRNA":"other",
    "miRNA,lncRNA,misc_RNA":"other",
    "misc_RNA,other,tmRNA":"tmRNA",
    "tmRNA,other,snoRNA,misc_RNA":"other",
    "snRNA,RNase_P_RN":"RNase_P_RN,snRNA",
    "scRNA,misc_RNA,other":"scRNA",
    "lncRNA,RNase_MRP_":"lncRNA,RNase_MRP",
    "RNase_P_RN,snRNA":"RNase_P_RN,snRNA",
    "tmRNA,other,misc_RNA,scRNA":"other",
    "snRNA,antisense_":"snRNA",
    "telomerase,other":"telomerase",
    "tRNA,rRNA,misc_RNA":"rRNA,tRNA",
    "misc_RNA,snoRNA,lncRNA":"other",
    "misc_RNA,tRNA":"tRNA",
    "Y_RNA,other":"Y_RNA,other",
    "other,siRNA":"siRNA",
    "lncRNA,snRNA":"lncRNA,snRNA",
    "misc_RNA,RNase_MRP_":"RNase_MRP,other",
    "RNase_P_RN,SRP_RNA":"RNase_P_RN,SRP_RNa",
    "misc_RNA,vault_RNA":"vault_RNA,other",
    "misc_RNA,precursor_,miRNA":"miRNA",
    "guide_RNA,snoRNA,lncRNA":"other",
    "antisense":"antisense",
    "RNase_MRP":"RNase_MRP",
    "miRNA,other":"miRNA",
    "hammerhead,other":"hammerhead,other",
    "RNase_MRP,other":"RNase_MRP,other",
    "ribozyme,other":"ribozyme,other",
    "vault_RNA":"vault_RNA",
    "vault_RNA,other":"vault_RNA,other",
    "guide_RNA,snoRNA":"guide_RNA,snoRNA",
    "RNase_MRP,snRNA":"RNase_MRP,snRNA",
    "piRNA,snoRNA":"piRNA,snoRNA",
    "rRNA,scRNA":"rRNA,scRNA",
    "lncRNA,telomerase":"lncRNA,telomerase",
    "miRNA,snRNA":"miRNA,snRNA",
    "RNase_MRP,RNase_P_RN":"RNase_MRP,RNase_P_RN",
    "scRNa,other":"scRNA",
    "lncRNA,RNase_MRP":"lncRNA,RNase_MRP",
    "siRNA,other":"siRNA",
    "RNase_P_RN,SRP_RNa":"RNase_P_RN,SRP_RNA",
    "misc_RNA,lncRNA":"lncRNA",
    "RNA,lncRNA":"lncRNA",
    "siRNA,misc_RNA":"siRNA",
    "misc_RNA,autocataly":"autocataly,other",
    "siRNA,miRNA,snRNA":"other",
    "RNA":"other",
    "miRNA,misc_RNA,piRNA":"other",
    "autocataly,misc_RNA":"autocataly,other",
    "rasiRNA,piRNA":"piRNA,rasiRNA",
    "antisense_,lncRNA,misc_RNA":"lncRNA",
    "rRNA,siRNA,snRNA":"other",
    "scRNA,misc_RNA":"scRNA",
    "snRNA,rRNA,siRNA":"other",
    "miRNA,siRNA,snRNA,misc_RNA":"other",
    "SRP_RNA,snoRNA":"snoRNA,SRP_RNA",
    "vault_RNA,scRNA":"scRNA,vault_RNA",
    "snRNA,miRNA,siRNA":"other",
    "rRNA,snRNA,siRNA":"other",
    "SRP_RNA,misc_RNA,other":"SRP_RNA",
    "misc_RNA,snRNA,siRNA":"other",
    "miRNA,misc_RNA,siRNA,snRNA":"other",
    "siRNA,miRNA,misc_RNA":"other",
    "siRNA,rRNA,snRNA":"other",
    "piRNA,misc_RNA,miRNA":"other",
    "miRNA,snRNA,misc_RNA,siRNA":"other",
    "scRNA,misc_RNA,SRP_RNA":"other",
    "antisense_,misc_RNA,lncRNA":"lncRNA",
    "RNase_MPR,misc_RNA":"RNase_MPR,other",
    "miRNA,siRNA,misc_RNA,snRNA":"other",
    "misc_RNA,lncRNA,miRNA":"other",
    "RNase_P_RN,misc_RNA,snoRNA":"other",
    "misc_RNA,SRP_RNA,scRNA":"other",
    "lncRNA,misc_RNA,antisense_":"lncRNA",
    "misc_RNA,rRNA,other":"rRNA",
    "lncRNA,antisense_,misc_RNA":"other",
    "SRP_RNA,other,misc_RNA":"SRP_RNA",
    "RNase_P_RN,scRNA,misc_RNA":"other",
    "SRP_RNA,rRNA":"rRNA,SRP_RNA",
    "SRP_RNA,other,scRNA":"scRNA,SRP_RNA",
    "misc_RNA,tRNA,rRNA":"other",
    "rRNA,tmRNA":"other",
    "snoRNA,RNase_MRP_,snRNA":"other",
    "misc_RNA,Y_RNA,scRNA":"other",
    "rRNA,miRNA":"other",
    "miRNA,snRNA,siRNA":"other",
    "misc_RNA,tmRNA":"tmRNA",
    "precursor_,lncRNA":"lncRNA",
    "misc_RNA,siRNA":"siRNA",
    "piRNA,miRNA":"miRNA,piRNA",
    "lncRNA,RNA":"lncRNA",
    "snRNA,rRNA":"rRNA,snRNA",
    "siRNA,rRNA":"other",
    "siRNA,snRNA,miRNA":"other",
    "rRNA,siRNA":"other",
    "miRNA,piRNA,misc_RNA":"miRNA,piRNA",
    "misc_RNA,miRNA,piRNA":"miRNA,piRNA",
    "snRNA,siRNA,miRNA":"other",
    "tRNA,siRNA":"siRNA,tRNA"

}

df_samehit["rna_type"].replace(rnatype_cleanup, inplace=True)
df_confhit["rna_type"].replace(rnatype_cleanup, inplace=True)
df_lostscan["rna_type"].replace(rnatype_cleanup, inplace=True)
df_newmem["rna_type"].replace(rnatype_cleanup, inplace=True)
df_newfam["rna_type"].replace(rnatype_cleanup, inplace=True)

df_samehit.to_csv(df_c_samehit, sep="\t", na_rep="None", header=True, index=False)
df_confhit.to_csv(df_c_confhit, sep="\t", na_rep="None", header=True, index=False)
df_lostscan.to_csv(df_c_lostscan, sep="\t", na_rep="None", header=True, index=False)
df_newmem.to_csv(df_c_newmem, sep="\t", na_rep="None", header=True, index=False)
df_newfam.to_csv(df_c_newfam, sep="\t", na_rep="None", header=True, index=False)