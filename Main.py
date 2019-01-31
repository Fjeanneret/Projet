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
	GeneSymbols.append(GeneSymbolAndSpecie[0])
	Species.append(GeneSymbolAndSpecie[1])

#print(GeneSymbols,Species)
	
j=0 
while j<len(GeneSymbols):
	geneIDs =  geneID_fetch(Species[j],GeneSymbols[j])
	prot = proteinName_ID(Species[j],GeneSymbols[j])
	fromUniprotToPDB_ID(prot)
	#transcript and protein ID fetching
	for ID in geneIDs:
		TranscriptID_ProtID_fetch(ID)
	print("---------------------------------------------------------------------------")
	j+=1

