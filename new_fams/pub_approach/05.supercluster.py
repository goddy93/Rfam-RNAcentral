import MySQLdb
import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine('mysql+mysqldb://root:rna@localhost/rnac_rfam')
connection = engine.connect()


def supercluster(pub_idx):
    for i in pub_idx:
        query_pub_clust = "SELECT p.id, p.pub_id FROM eu_newfam_pub p JOIN eu_newfam e ON e.id=p.id WHERE pub_id = %i AND e.rna_type NOT LIKE 'rRNA' AND e.rna_type NOT LIKE 'tRNA' AND e.rna_type NOT LIKE 'miRNA'" % (i)
        pub_clust = pd.read_sql_query(
                   query_pub_clust,
                   connection,
                   index_col=None,
                   coerce_float=True,
                   params=None,
                   parse_dates=None,
                   chunksize=None
                   )

        clust_num = pd.DataFrame()
        for urs in pub_clust["id"]:
            query_clust_num = "SELECT id, cluster FROM eu_newfam_clstr WHERE id LIKE " + "'" + urs + "'"
            clust_num = clust_num.append(pd.read_sql_query(
                    query_clust_num,
                    connection,
                    index_col=None,
                    coerce_float=True,
                    params=None,
                    parse_dates=None,
                    chunksize=None
                    ))

        super_cluster_pd = pd.DataFrame()
        for cl in clust_num["cluster"].drop_duplicates():
            super_cluster = "SELECT c.id, c.cluster, e.len, e.db, e.rna_type FROM eu_newfam_clstr c JOIN eu_newfam e ON e.id=c.id WHERE c.cluster = %i ORDER BY c.cluster" % (cl)
            super_cluster_pd = super_cluster_pd.append(pd.read_sql_query(
                    super_cluster,
                    connection,
                    index_col=None,
                    coerce_float=True,
                    params=None,
                    parse_dates=None,
                    chunksize=None
                    ))
            super_cluster_pd["rep"] = "-"
            list_urs = clust_num.id.tolist()
            super_cluster_pd.ix[super_cluster_pd.id.isin(list_urs), "rep"] = "x"
            super_cluster_pd = super_cluster_pd.sort_values(["cluster", "rep"], ascending=[True, False])
            super_cluster_pd.reset_index(drop=True, inplace=True)
            super_cluster_pd = super_cluster_pd[["cluster", "id", "rep", "rna_type", "db", "len"]]

            num_members = len(super_cluster_pd["id"].drop_duplicates())
            num_clusters = len(super_cluster_pd["cluster"].drop_duplicates())
            per_belonging = round(len(pub_clust) / float(num_members), 2)
            avg_clust_size = num_members / float(num_clusters)
            per_clustering = round(avg_clust_size / num_members, 2)
            summary_data = [num_members, num_clusters, per_belonging, per_clustering]

        print "pub_id", pub_idx
        print "[num_members, num_clusters, per_belonging, per_clustering]"
        print summary_data
        print super_cluster_pd

