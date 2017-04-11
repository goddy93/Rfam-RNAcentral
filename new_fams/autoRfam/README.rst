autoRfam README
===============

Workflow
********
00. Get sequences
~~~~~~~~~~~~~~~~~

00.a. Get group of interest and filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The first thing to do, is to define a set of RNAcentral sequences that could pontentially be clustered to build new families. To achieve this, we filtered the sequences through the following criteria:

1. The sequence has no Rfam hits (see Rfam-RNAcentral_)
2. The sequence is of an appropriate size (40-1500 nt)
3. Extra filters such as rna_type, description, and publication title, related to the sequence URS.

An example of how these filters can be set in a database is found in 00.a.filter_query.sql_. It is important to have a somehow reduced group of sequences, because clustering process will crash with large sets.

The output of this process should be a **list of RNAcentral URSs**.

.. _Rfam-RNAcentral: https://github.com/nataquinones/Rfam-RNAcentral
.. _00.a.filter_query.sql: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/autoRfam/00.a.filter_query.sql

00.b. Fetch ``.fasta`` sequences from RNAcentral
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Description:
  Takes file of RNAcentral URSs (non species-specific, one URS per line), fetches the sequence in ``.fasta`` format and makes file with all of the sequences.

+---------+-------------------------+-------------------------+
|**IN:**  | ``newfam_list.tsv``     | list of RNAcentral URSs |
+---------+-------------------------+-------------------------+
|*script:*| 00.b.get_fasta.py_                                |
+---------+-------------------------+-------------------------+
|*use:*   | ``python 00.b.get_fasta.py <IN.tsv> <OUT.fasta>`` |
+---------+-------------------------+-------------------------+
|**OUT:** |``newfam_seq.fasta``     | file with sequences     |
+---------+-------------------------+-------------------------+

.. _00.b.get_fasta.py: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/nhmmer_approach2/00.b.get_fasta.py


01. Use ``nhmmer`` to compare all vs. all
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
01.a. Run ``nhmmer``
^^^^^^^^^^^^^^^^^^^
Description:
  Runs nhmmer with options: ``-o`` ``-A`` ``--tblout`` ``--noali`` ``--rna`` ``--tformat fasta`` ``--qformat fasta``

+---------+-------------------------+------------------------------------+
|**IN:**  | ``newfam_seq.fasta``    | All sequences in ``.fasta`` format |
+---------+-------------------------+------------------------------------+
|*script:*| 01.a.newfam_nhmmer.sh_                                       |
+---------+-------------------------+------------------------------------+
|*use:*   | ``bsub < 01.a.newfam_nhmmer.sh``                             |
+---------+-------------------------+------------------------------------+
|**OUT:** |``newfam_nhmmer.out``    |  ``nhmmer`` output                 |
|         +-------------------------+------------------------------------+
|         |``newfam_nhmmer.sto``    |  concatenated stockholm file       |
|         +-------------------------+------------------------------------+
|         |``newfam_nhmmer.tbl``    | ``nhmmer`` table output            |
|         +-------------------------+------------------------------------+
|         |``newfam_nhmmer.job.out``|  job stdout                        |
|         +-------------------------+------------------------------------+
|         |``newfam_nhmmer.job.err``|  job stderr                        |
+---------+-------------------------+------------------------------------+

.. _01.a.newfam_nhmmer.sh: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/autoRfam/01.a.newfam-nhmmer.sh

(To use, change ``#PATHS``, ``#BSUB -o`` and ``#BSUB -e`` to the appropriate paths.)

01.b. Parse ``nhmmer`` table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Description:

+---------+-------------------------+------------------------------------+
| IN:     | ``newfam_nhmmer.tbl``   |  from 1.1                          |
+---------+-------------------------+------------------------------------+
| script: | 03.a.parse.py                                                |
+---------+-------------------------+------------------------------------+
| OUT:    |``newfam_nhmmer.tsv``    |                                    |
+---------+-------------------------+------------------------------------+
| use:    |``03.a.parse.py <IN.tbl> <OUT.tsv>``                          |
+---------+--------------------------------------------------------------+

.. _01.newfam-nhmmer.sh: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/nhmmer_approach2/00.get_fasta.py


1.3. Slice alignments
^^^^^^^^^^^^^^^^^^^^^
Description:

+---------+-------------------------+------------------------------------+
| **IN:** | ``newfam_nhmmer.sto``   |  from 1.1                          |
+---------+-------------------------+------------------------------------+
| script: | 02.slice_sto_nhmmer.py                                       |
+---------+--------------------------------------------------------------+
| use:    |``02.slice_sto_nhmmer.py <IN.sto>``                           |
+---------+-------------------------+------------------------------------+
| **OUT:**| ``URSxxxxxxxxxx.sto``   |                                    |
|         | ...                     |                                    |
+---------+-------------------------+------------------------------------+


2. Filter alignments
~~~~~~~~~~~~~~~~~~~~

2.1. Remove non significant
^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.2. Remove singletons
^^^^^^^^^^^^^^^^^^^^^^

3. Cluster groups
~~~~~~~~~~~~~~~~~

4. Clean alignments
~~~~~~~~~~~~~~~~~~~
4.1. Clean alignments
^^^^^^^^^^^^^^^^^^^^^
4.2. Pick best of repeated
^^^^^^^^^^^^^^^^^^^^^^^^^^

5. Select best alignment of group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
5.1. Easel cleaned alignments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
5.2. Select best
^^^^^^^^^^^^^^^^

5. Make autoRfam
~~~~~~~~~~~~~~~~
