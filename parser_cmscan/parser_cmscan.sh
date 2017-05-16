#BSUB -J tblparse
#BSUB -o /nfs/research2/nobackup/nqo/cmscan_parser/two/tblparse.out
#BSUB -e /nfs/research2/nobackup/nqo/cmscan_parser/two/tblparse.err

#JOB
source /nfs/research2/nobackup/nqo/cmscan_parser/venv-parser/bin/activate
cd /nfs/research2/nobackup/nqo/cmscan/tables/
for file in *.tbl
	do python /nfs/research2/nobackup/nqo/cmscan_parser/two/parser_cmscan.py "/nfs/research2/nobackup/nqo/cmscan/tables/"$file "/nfs/research2/nobackup/nqo/cmscan_parser/two/p_tables/"$file".par"
done