#Main.py

import requests, re
from Ensembl import * 

GeneSymbols = []
Species=[]

'''
fichier = open("GeneSymbols.txt")
lignes = fichier.readlines()
print(lignes)'''

with open("GeneSymbols.txt") as f:
    lines = f.read().splitlines() 

for line in lines:
	line = line.replace(" ", "_") #penser a gerer l'espace a la fin du premier Homo_sapiens
	GeneSymbolAndSpecie =  line.split("\t")
	GeneSymbols.append(GeneSymbolAndSpecie[0])
	Species.append(GeneSymbolAndSpecie[1])
print(GeneSymbols,Species)

#for GeneSymbol in GeneSymbols:
	#print(geneID("GeneSymbol","Homo_sapiens"))
	
	
j=0
 
while j<len(GeneSymbols):
	geneIDs =  geneID_fetch(GeneSymbols[j],Species[j])
	
	#transcript and protein ID fetching
	for ID in geneIDs:
		TranscriptID_ProtID_fetch(ID)
	j+=1