autoRfam README
===============

Workflow
********
00. Get sequences
~~~~~~~~~~~~~~~~~

00.a. Get group of interest and filter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

00.b. Fetch ``.fasta`` sequences from RNAcentral
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Description:
  Takes file of RNAcentral URSs (non species-specific, one URS per line), fetches the sequence in ``.fasta`` file and makes file with all of the sequences.

+---------+-------------------------+-------------------------+
|**IN:**  | ``newfam_list.tsv``     | list of RNAcentral URSs |
+---------+-------------------------+-------------------------+
|*script:*| 00.b.get_fasta.py_                                |
+---------+-------------------------+-------------------------+
|*use:*   | ``python 00.b.get_fasta.py <IN.tsv> <OUT.fasta>`` |
+---------+-------------------------+-------------------------+
|**OUT:** |``newfam_seq.fasta``     | fasta file              |
+---------+-------------------------+-------------------------+

.. _00.b.get_fasta.py: https://github.com/nataquinones/Rfam-RNAcentral/blob/master/new_fams/nhmmer_approach2/00.get_fasta.py


01. Use ``nhmmer`` to compare all vs all
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
