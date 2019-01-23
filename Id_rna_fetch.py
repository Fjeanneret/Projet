import requests, sys
server = "https://rest.ensembl.org"
ext = "/lookup/id/AT2G18790?expand=1"

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
		print(decoded["Transcript"][i]["id"])
	i=i+1

# a lier avec les ID recup dans Id_gene_fetch.py
