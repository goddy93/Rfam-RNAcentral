SELECT
        ur.id,
        ur.len,
        uc.db,
        uc.rna_type,
        ch.hit_rfam_acc,
        pc.title
FROM urs_rnacentral ur
LEFT JOIN cmscan_run cr ON ur.id = cr.id
LEFT JOIN urs_condensed uc ON ur.id = uc.id
LEFT JOIN cmscan_hits ch ON ur.id = ch.id
LEFT JOIN urs_description_con d ON ur.id = d.id
LEFT JOIN pub_condensed pc ON ur.id = pc.id

WHERE cr.id IS NOT NULL -- ran
AND uc.rfam_acc IS NULL -- not in Rfam
AND ch.hit_rfam_acc IS NULL -- no hit

-- unwanted types NOT for Rfam
AND uc.rna_type NOT LIKE "%lncRNA%"
AND uc.rna_type NOT LIKE "%piRNA%"
AND uc.rna_type NOT LIKE "siRNA"
AND uc.rna_type NOT LIKE "%miRNA%"
AND uc.rna_type NOT LIKE "%precursor%"
AND uc.rna_type NOT LIKE "%guide_RNA%"
AND uc.rna_type NOT LIKE "%rasiRNA%"
-- unwanted types tRNA, rRNA, tmRNA
AND uc.rna_type NOT LIKE "%rRNA%"
AND uc.rna_type NOT LIKE "%tRNA%"
AND uc.rna_type NOT LIKE "%tmRNA%"
-- rna_type filters
AND d.description NOT LIKE "%tRNA%"
AND d.description NOT LIKE "%transfer%"
AND d.description NOT LIKE "%rRNA%"
AND d.description NOT LIKE "%ribosomal%"
AND d.description NOT LIKE "%miRNA%"
AND d.description NOT LIKE "%microRNA%"
AND d.description NOT LIKE "%precursor%"
AND d.description NOT LIKE "%piR%"
AND d.description NOT LIKE "%piRNA%"
-- spacers and other
AND d.description NOT LIKE "%spacer%"
AND d.description NOT LIKE "%ITS%"
AND d.description NOT LIKE "%intergenic%"
AND d.description NOT LIKE "%5'-R%"
AND d.description NOT LIKE "%synthetic construct%"
AND d.description NOT LIKE "%uncharacterized protein%"
-- publication filters
AND pc.title NOT LIKE "%ETS%"
AND pc.title NOT LIKE "%ITS%"
AND pc.title NOT LIKE "spacer"
AND pc.title NOT LIKE "%barcod%"
AND pc.title NOT LIKE "%biogeo%"
AND pc.title NOT LIKE "%colonization%"
AND pc.title NOT LIKE "%communit%"
AND pc.title NOT LIKE "%discrimination%"
AND pc.title NOT LIKE "%ecotype%"
AND pc.title NOT LIKE "%first re%"
AND pc.title NOT LIKE "%isolate%"
AND pc.title NOT LIKE "%phylo%"
AND pc.title NOT LIKE "%phyly%"
AND pc.title NOT LIKE "%population%"
AND pc.title NOT LIKE "%prevalence%"
AND pc.title NOT LIKE "%rapid identification%"
AND pc.title NOT LIKE "%ribosomal DNA%"
AND pc.title NOT LIKE "sensu."
AND pc.title NOT LIKE "sp."
AND pc.title NOT LIKE "cryptic"
-- size
AND ur.len > 40
AND ur.len < 2000