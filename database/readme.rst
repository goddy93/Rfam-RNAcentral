Rfam-RNAcentral Database
========================
Database design
---------------

Table creation
--------------

Table ``rnacentral_map``
^^^^^^^^^^^^^^^^^^^^^^^
Where ``id_mapping`` is a table generated previously from the ``id_mapping`` file in the RNAcentral FTP site:

.. code :: SQL

	CREATE TABLE rnacentral_map
	SELECT 
		im.id, 
		GROUP_CONCAT(DISTINCT im.db) AS db,
		GROUP_CONCAT(DISTINCT IF(im.db LIKE '%RFAM%',im.db_acc,NULL)) AS rfam_acc,
		GROUP_CONCAT(DISTINCT im.rna_type) AS rna_type
	FROM id_mapping im
	GROUP BY im.id

Make ``id`` primary key:

.. code :: SQL

	ALTER TABLE rnacentral_map
	ADD PRIMARY KEY (id);

Table ``cmscan_hits``
^^^^^^^^^^^^^^^^^^^^^^^
.. code :: SQL

	CREATE TABLE cmscan_hits
	(id VARCHAR(13),
	hit_rfam_acc VARCHAR(7),
	fam_name VARCHAR(30),
	hit_clan_acc VARCHAR(7),
	olp VARCHAR(1),
	e_value VARCHAR(10)
	);

Make forgein key:

.. code :: SQL

	ALTER TABLE cmscan_hits
	ADD FOREIGN KEY (id)
	REFERENCES rnacentral_map (id);

Load files into table:

.. code :: SQL

	LOAD DATA LOCAL INFILE "file_to_be_loaded.txt" INTO TABLE cmscan_hits IGNORE 1 LINES;

Loaded file should be in the output format of `parser_cmscan <https://github.com/nataquinones/Rfam-RNAcentral/tree/master/parser_cmscan>`_ 

Group queries
--------------

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
^^^^^^^^^^^

*RNAcentral sequence is in Rfam, has a hit that is the same as the Rfam annotation.*

.. code :: SQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NOT NULL -- in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- got hit
	AND rm.rfam_acc = ch.hit_rfam_acc -- same

2. CONFLICTING HIT
^^^^^^^^^^^^^^^^^^

*RNAcentral sequence is in Rfam, has a hit that is not the same as the Rfam annotation.*

.. code :: SQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NOT NULL -- in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- got hit
	AND rm.rfam_acc != ch.hit_rfam_acc -- different

3. LOST IN SCAN
^^^^^^^^^^^^^^^

*RNAcentral sequence is in Rfam, but had no hits in cmscan.*

.. code :: SQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NOT NULL -- in Rfam
	AND ch.hit_rfam_acc IS NULL -- no hit

4. NEW MEMBERS
^^^^^^^^^^^^^^^

*RNAcentral sequence is not Rfam, but had hits.*


.. code :: SQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NULL -- not in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- got hit

5. NEW FAMILY
^^^^^^^^^^^^^^^

*RNAcentral sequence is not Rfam, and had hits.*

.. code :: SQL

	SELECT
		rm.id, rm.db, rm.rna_type, rm.rfam_acc, ch.hit_rfam_acc, ch.hit_clan_acc
	FROM rnacentral_map rm
	LEFT JOIN cmscan_hits ch ON rm.id=ch.id
	WHERE rm.rfam_acc IS NULL -- not in Rfam
	AND ch.hit_rfam_acc IS NOT NULL -- no hit

Overcounting issue
------------------
Redundancy in SAME HIT and CONFLICT HIT caused by multiple hits in a same RNAcentral sequence:

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

To collapse multiple hits:

.. code :: SQL

	SELECT
		ch.id, GROUP_CONCAT(DISTINCT ch.hit_rfam_acc) AS families
	FROM cmscan_hits ch 
	GROUP BY ch.id
