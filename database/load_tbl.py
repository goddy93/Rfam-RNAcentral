import sqlalchemy
import os

files = os.listdir(".")

engine = sqlalchemy.create_engine('mysql+mysqldb://root:rna@localhost/rnac_rfam')
connection = engine.connect()
for file in files:
	connection.execute("load data local infile '%s' into table cmscan_hits ignore 1 lines;" % file)
