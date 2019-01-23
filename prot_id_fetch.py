#protein summary : 


import requests, sys
server = "https://rest.ensembl.org"
ext = "/lookup/id/ENSG00000157764?expand=1"

r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
if not r.ok:
	server = "https://rest.ensemblgenomes.org"
	ext = "/lookup/id/{}?expand=1".format("AT2G18790")
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	#r.raise_for_status()
	#sys.exit()
 
decoded = r.json()
#print(repr(decoded))

i=0
for element in decoded["Transcript"]:
	
	if decoded["Transcript"][i]["biotype"]=="protein_coding":
		print(decoded["Transcript"][i]["Translation"]["id"])
	i=i+1

# a lier avec les ID recup dans Id_gene_fetch.py


# http://www.ensembl.org/Homo_sapiens/Transcript/ProteinSummary?
#db=core;g=ENSG00000157764;p=ENSP00000496776;
