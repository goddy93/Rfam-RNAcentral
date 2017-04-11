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

WHERE cr.id IS NOT NULL -- scan ran
AND uc.rfam_acc IS NULL -- not in Rfam
AND ch.hit_rfam_acc IS NULL -- no hit

-- size
AND ur.len > 40
AND ur.len < 2000
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
AND pc.title NOT LIKE "%barcod%"
AND pc.title NOT LIKE "%biogeo%"
AND pc.title NOT LIKE "%colonization%"
AND pc.title NOT LIKE "%communit%"
AND pc.title NOT LIKE "%comparative gen%"
AND pc.title NOT LIKE "%conservation gen%"
AND pc.title NOT LIKE "%conspecificity%"
AND pc.title NOT LIKE "%classification%"
AND pc.title NOT LIKE "%cryptic%"
AND pc.title NOT LIKE "differentiation of strains"
AND pc.title NOT LIKE "%discrimination%"
AND pc.title NOT LIKE "%dispersal%"
AND pc.title NOT LIKE "%distribution%"
AND pc.title NOT LIKE "%ecotype%"
AND pc.title NOT LIKE "%endemi%"
AND pc.title NOT LIKE "ETS"
AND pc.title NOT LIKE "%first re%"
AND pc.title NOT LIKE "gen. nov."
AND pc.title NOT LIKE "genetic characterization"
AND pc.title NOT LIKE "genetic distinctions"
AND pc.title NOT LIKE "genetic heterogeneity"
AND pc.title NOT LIKE "genetic identifiaction"
AND pc.title NOT LIKE "genetic lineage"
AND pc.title NOT LIKE "%genetic vari%"
AND pc.title NOT LIKE "genomic evidence"
AND pc.title NOT LIKE "%genetic vari%"
AND pc.title NOT LIKE "%genotyp%"
AND pc.title NOT LIKE "%genus%"
AND pc.title NOT LIKE "%geographic%"
AND pc.title NOT LIKE "%hybrid%"
AND pc.title NOT LIKE "%intergenic region%"
AND pc.title NOT LIKE "%interspeci%"
AND pc.title NOT LIKE "%intra-specific%"
AND pc.title NOT LIKE "%intraspecific%"
AND pc.title NOT LIKE "%invasi%"
AND pc.title NOT LIKE "%isolat%"
AND pc.title NOT LIKE "ITS%"
AND pc.title NOT LIKE "%marker%"
AND pc.title NOT LIKE "%molecular %"
AND pc.title NOT LIKE "%morpholog%"
AND pc.title NOT LIKE "%occurrence%"
AND pc.title NOT LIKE "%phyletic%"
AND pc.title NOT LIKE "%phylo%"
AND pc.title NOT LIKE "%phyly%"
AND pc.title NOT LIKE "%ploid%"
AND pc.title NOT LIKE "%population%"
AND pc.title NOT LIKE "%prevalence%"
AND pc.title NOT LIKE "%radiation%"
AND pc.title NOT LIKE "rapid identification"
AND pc.title NOT LIKE "rDNA"
AND pc.title NOT LIKE "repeat"
AND pc.title NOT LIKE "ribosomal"
AND pc.title NOT LIKE "sens."
AND pc.title NOT LIKE "sensu"
AND pc.title NOT LIKE "sp."
AND pc.title NOT LIKE "spacer"
AND pc.title NOT LIKE "%species%"
AND pc.title NOT LIKE "%synonym%"
AND pc.title NOT LIKE "%systematic%"
