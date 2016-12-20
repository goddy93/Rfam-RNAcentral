
#DATAFLOW GENERAL
1. Guardar las queries como archivos
2. Correr los scripts de count
3. Correr el (los) script(s) de graficar



#1. GUARDAR LAS QUERIES COMO ARCHIVOS
cd Desktop
mysqllocal
USE rnac_rfam;

#Correr queries (abajo)

#Abrir y guardar bien con:
cd Desktop/tmp/

 /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /tmp/newfam

#------------------------------------------------
#query_tot
SELECT id
FROM cmscan_run

INTO OUTFILE '/tmp/query_tot'
FIELDS TERMINATED BY '\t'
ENCLOSED BY ""
ESCAPED BY ""
LINES TERMINATED BY '\n';

#------------------------------------------------
#query_samehit
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

AND uc.rfam_acc IS NOT NULL -- in Rfam
AND ch.hit_rfam_acc IS NOT NULL -- got hit
AND uc.rfam_acc = ch.hit_rfam_acc -- same

INTO OUTFILE '/tmp/query_samehit'
FIELDS TERMINATED BY '\t'
ENCLOSED BY ""
ESCAPED BY ""
LINES TERMINATED BY '\n';

#------------------------------------------------
#query_confhit
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

AND uc.rfam_acc IS NOT NULL -- in Rfam
AND ch.hit_rfam_acc IS NOT NULL -- got hit
AND uc.rfam_acc != ch.hit_rfam_acc -- different

INTO OUTFILE '/tmp/query_confhit'
FIELDS TERMINATED BY '\t'
ENCLOSED BY ""
ESCAPED BY ""
LINES TERMINATED BY '\n';
#------------------------------------------------
#query_lostscan
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

AND uc.rfam_acc IS NOT NULL -- in Rfam
AND ch.hit_rfam_acc IS NULL -- no hit

INTO OUTFILE '/tmp/query_lostscan'
FIELDS TERMINATED BY '\t'
ENCLOSED BY ""
ESCAPED BY ""
LINES TERMINATED BY '\n';

#------------------------------------------------
#query_newmem
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
AND ch.hit_rfam_acc IS NOT NULL -- got hit

INTO OUTFILE '/tmp/query_newmem'
FIELDS TERMINATED BY '\t'
ENCLOSED BY ""
ESCAPED BY ""
LINES TERMINATED BY '\n';

#------------------------------------------------
#query_newfam
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

INTO OUTFILE '/tmp/query_newfam'
FIELDS TERMINATED BY '\t'
ENCLOSED BY ""
ESCAPED BY ""
LINES TERMINATED BY '\n';

#------------------------------------------------
#query_colapsedhits
SELECT ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families 
FROM cmscan_hits ch 
GROUP BY ch.id

INTO OUTFILE '/tmp/query_colapsedhits'
FIELDS TERMINATED BY '\t'
ENCLOSED BY ""
ESCAPED BY ""
LINES TERMINATED BY '\n';
