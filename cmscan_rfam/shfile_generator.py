import sys
import os

shfiles_dir = "./shfiles"
out_dir = "/nfs/research2/nobackup/nqo/cmscan/output"
err_dir = "/nfs/research2/nobackup/nqo/cmscan/err"
tbl_dir = "/nfs/research2/nobackup/nqo/cmscan/tables"
in_dir = sys.argv[1]
os.mkdir("shfiles")
os.mkdir("output")
os.mkdir("tables")
os.mkdir("err")

a = []
for file in os.listdir(in_dir):
    if file.endswith(".fasta"):
        a.append(os.path.splitext(file)[0])

for file in a:
	shfiles_path = os.path.join(shfiles_dir, file)
	err_path = os.path.join(err_dir, file)
	out_path = os.path.join(out_dir, file)
	tbl = file + ".tbl"
	table = os.path.join(tbl_dir, tbl)
	fasta = file + ".fasta"
	in_path = os.path.join(in_dir, fasta)
	f = open(shfiles_path + ".sh",'w')
	f.write("#BSUB -q mpi-rh7\n")
	f.write("#BSUB -J " + file + "\n")
	f.write("#BSUB -o " + out_path + ".out"+"\n")
	f.write("#BSUB -e " + err_path + ".err"+"\n")
	f.write("#BSUB -M 10000\n")
	f.write('#BSUB -R "rusage[mem=10000]"\n')
	f.write("#BSUB -n 4\n")
	f.write("#BSUB -R span[hosts=1]\n")
	f.write("#BSUB -a openmpi mpiexec\n")
	f.write("#BSUB -mca btl ^openib\n")
	f.write("#BSUB -np 4\n")
	f.write("#BSUB -g /rnacrfam\n")
	f.write("\n")
	f.write("#PATHS\n")
	f.write("input_path='" + in_path + "'\n")
	f.write("tblout_path='" + table + "'\n")
	f.write('cmscan="/nfs/production/xfam/rfam/rfam_rh7/software/bin/cmscan"\n')
	f.write('clanin_path="/nfs/production/xfam/rfam/software/infernal_rh7/infernal-1.1.2/testsuite/Rfam.12.1.clanin"\n')
	f.write('cm_path="/nfs/gns/homes/nataquinones/RfamCM/Rfam.cm"\n')
	f.write("\n")
	f.write("#JOB\n")
	f.write("$cmscan --tblout $tblout_path -Z 12063.99847 --noali --rfam --cut_ga --acc --nohmmonly --notextw --cpu 4 --fmt 2 --clanin $clanin_path $cm_path $input_path")
	f.close()
