Group queries
========================
+----------------------------------------------------------+----------------------------------+
| Rfam                                                     | No Rfam                          |
+---------------------------------------+------------------+-----------------+----------------+
| Hits                                  | No hits          | Hits            | No hits        |
+-----------------+---------------------+                  |                 |                |
| Same            | Not-same            |                  |                 |                |
+-----------------+---------------------+------------------+-----------------+----------------+
| **SAME HIT**    | **CONFLICTING HIT** | **LOST IN SCAN** | **NEW MEMBERS** | **NEW FAMILY** |
+-----------------+---------------------+------------------+-----------------+----------------+

1. SAME HIT
-----------

*RNAcentral sequence is in Rfam, has a hit that is the same as the Rfam annotation.*

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



2. CONFLICTING HIT
------------------

*RNAcentral sequence is in Rfam, has a hit that is not the same as the Rfam annotation.*

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

3. LOST IN SCAN
---------------

*RNAcentral sequence is in Rfam, but had no hits in cmscan.*

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


4. NEW MEMBERS
--------------

*RNAcentral sequence is not Rfam, but had hits.*


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

5. NEW FAMILY
-------------

*RNAcentral sequence is not Rfam, and had hits.*

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

Filter:

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

	AND uc.rna_type NOT LIKE 'tRNA%'
	AND uc.rna_type NOT LIKE 'rRNA%'
	AND uc.rna_type NOT LIKE 'piRNA%'
	AND ur.len > 30
	AND ur.len < 200

	ORDER BY uc.db

Overcounting issue
------------------
TOTAL:

+--------------------------+-----------+
| id_mapping               | 9 386 122 |
+--------------------------+-----------+
| rnacentral_nhmmer.fasta  | 9 386 112 |
+--------------------------+-----------+

All groups should be mutually exclusive, but with the previous queries there'll be redundancy in `SAME HIT` and `CONFLICTING HIT` caused by multiple hits in a same RNAcentral sequence:

+----+----------+----------+-----------------+
| id | rfam_acc | hit_rfam | GROUP           |
+====+==========+==========+=================+
| 1  | A        | A        | SAME HIT        |
+----+----------+----------+-----------------+
| 2  | A        | B        | CONFLICTING HIT |
+----+----------+----------+-----------------+
| 3  | A        | A        | SAME HIT        |
+----+----------+----------+-----------------+
| 3  | A        | B        | CONFLICTING HIT |
+----+----------+----------+-----------------+
| 4  | A        | A        | SAME HIT        |
+----+----------+----------+-----------------+
| 4  | A        | B        | CONFLICTING HIT |
+----+----------+----------+-----------------+
| 4  | A        | C        | CONFLICTING HIT |
+----+----------+----------+-----------------+

.. code::

	G1 + G2 = TOTAL - (G3 + G4 + G5)

To discern bewteen G1 and G2, multiple hits can be collapsed:

.. code:: SQL

	SELECT
		ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families
	FROM cmscan_hits ch 
	GROUP BY ch.id
