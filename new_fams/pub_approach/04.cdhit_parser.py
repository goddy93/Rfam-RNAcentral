import pandas as pd

cluster_file = open("./files/cd-hit-clusters/eunewfam-clustered3.fasta.clstr", 'r')
cluster_list = cluster_file.read()
output_file = "./files/db_clust"


def read_clusters(cluster_list):
    """
    Modified from 
    https://github.com/GordonLab/metagenomic-pipeline/blob/master/Modules/tools/cdhit_parse.py
    This version makes a table that relates each FASTA
    title > in the .clstr output to its cluster number
    """
    cluster_db = {}
    cluster_db_count = {}

    unique_list = []

    # Split the file so that each cluster is it's own line
    clusters = cluster_list.split('>Cluster ')

    # Go through the cluster
    for line in clusters:
        # Take off the end newline
        line = line.rstrip('\n')

        sequences = []
        count = 0

        # If it's a cluster
        if len(line) > 0:

            # split at the newlines, so each sequence is on its own line
            hits = line.split('\n')

            # For each hit split it to get the sequence name
            for i in hits:
                # Split at the spaces
                new = i.split(' ')

                # If the length of the line is 1, it's the name of the cluster,
                # what we're using as the key
                if len(new) == 1:
                    key = new[0]
                # If the third column is a *, it's the reference
                elif new[2] == '*':
                    reference = new[1]
                    reference = reference[:-3]
                    reference = reference.lstrip('>')
                    count = count + 1
                    unique_list.append(reference)
                    #  sequences = sequences.append(new[1])
                # If the third column is 'at', it's one of the sequences in the cluster
                elif len(new) == 4:
                    seq = new[1]
                    seq = seq[:-3]
                    seq = seq.lstrip('>')
                    sequences.append(seq)
                    count = count + 1

            sequences.insert(0, reference)

            cluster_db[key] = sequences
            cluster_db_count[key] = count

    return cluster_db

a = read_clusters(cluster_list)
df = pd.DataFrame()

for j in range(0, len(a)):
    b = []
    for i in range(0, len(a[str(j)])):
        b.append([a[str(j)][i], j])
    df = df.append(b)

df.to_csv(output_file, sep='\t', index=False)
