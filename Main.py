import requests, re
from Ensembl import * 
from uniprot_pdb import * 



GeneSymbols = []
Species=[]

with open("GeneSymbols.txt") as f:
    lines = f.read().splitlines() 

for line in lines:
	line = line.replace(" ", "_") #penser a gerer l'espace a la fin du premier Homo_sapiens
	GeneSymbolAndSpecie =  line.split("\t")
	GeneSymbols = GeneSymbolAndSpecie[0]
	Species = GeneSymbolAndSpecie[1]

	result = open("result.html", "a")
	result.write("<tr><td>{}</td>\n<td>{}</td>".format(Species,GeneSymbols))
	result.close()

	# extractions des annotations
	## EnsEMBL
	genesList =  geneID_fetch(Species,GeneSymbols)	
	print(genesList)
	TranscriptID_ProtID_fetch(Species, genesList)
	#Uniprot
	#prot = proteinName_ID(Species,GeneSymbols)
	#fromUniprotToPDB_ID(prot)

	print("---------------------------------------------------------------------------")
	
	


