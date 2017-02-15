SELECT
        ur.id,
        ur.len,
        uc.db,
        uc.rna_type,
        uc.rfam_acc,
        uc.tax_id,
        ch.hit_rfam_acc,
        ch.hit_clan_acc,
        ch.e_value
FROM urs_rnacentral ur
LEFT JOIN cmscan_run cr ON ur.id = cr.id
LEFT JOIN urs_condensed uc ON ur.id = uc.id
LEFT JOIN cmscan_hits ch ON ur.id = ch.id

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
-- size
AND ur.len > 45
AND ur.len < 2200