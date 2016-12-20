**query_tot**

.. code:: SQL

 SELECT id
 FROM cmscan_run

 INTO OUTFILE './query_tot'
 FIELDS TERMINATED BY '\t'
 ENCLOSED BY ""
 ESCAPED BY ""
 LINES TERMINATED BY '\n';

**query_samehit**

.. code:: SQL

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

 INTO OUTFILE './query_samehit'
 FIELDS TERMINATED BY '\t'
 ENCLOSED BY ""
 ESCAPED BY ""
 LINES TERMINATED BY '\n';

**query_confhit**

.. code:: SQL

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

 INTO OUTFILE './query_confhit'
 FIELDS TERMINATED BY '\t'
 ENCLOSED BY ""
 ESCAPED BY ""
 LINES TERMINATED BY '\n';

**query_lostscan**

.. code:: SQL

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

 INTO OUTFILE './query_lostscan'
 FIELDS TERMINATED BY '\t'
 ENCLOSED BY ""
 ESCAPED BY ""
 LINES TERMINATED BY '\n';

**query_newmem**

.. code:: SQL

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

   INTO OUTFILE './query_newmem'
   FIELDS TERMINATED BY '\t'
   ENCLOSED BY ""
   ESCAPED BY ""
   LINES TERMINATED BY '\n';

**query_newfam**

.. code:: SQL

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

  INTO OUTFILE './query_newfam'
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY ""
  ESCAPED BY ""
  LINES TERMINATED BY '\n';

**query_colapsedhits**

.. code:: SQL

  SELECT ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families 
  FROM cmscan_hits ch 
  GROUP BY ch.id

  INTO OUTFILE './query_colapsedhits'
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY ""
  ESCAPED BY ""
  LINES TERMINATED BY '\n';
