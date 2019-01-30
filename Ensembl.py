#Ensembl

#for nombre de trucs
	
#main^

import requests, sys

def geneID(GeneSymbols,Species):
	
	server = "https://rest.ensembl.org"
	#ext = "/xrefs/symbol/homo_sapiens/BRCA2?"
	ext = "/xrefs/symbol/{}/{}".format(Species,GeneSymbols)
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	 
	if not r.ok:
		server = "https://rest.ensemblgenomes.org"
		ext = "/xrefs/symbol/{}/{}?".format(Species,GeneSymbols)
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
		
	  #r.raise_for_status()
	  #sys.exit()
	
	decoded = r.json()
	#gerer les plusieurs noms??
	ID_ENSG=[]
	j=0
	#si len(decoded)>1 ? faire .join ?  
	while j<len(decoded):
		
		ID_ENSG.append(decoded[j]["id"])
		#ecrire dans fichier plutot ?
		
		j+=1
	
	print(ID_ENSG)


geneID("BRCA2","homo_sapiens")
	#pour chaque element de Gene_id construire url
#main : ???
'''
def RNA_ID():
	

def PROT_name():
	
'''


#ncbi  ??? https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=brca2

#id
#https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=(brca2[Gene%20Name])%20AND%20homo_sapiens[Organism]

#ortho? 
#https://www.ncbi.nlm.nih.gov/gene/?Term=ortholog_gene_675[group]
