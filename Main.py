#Main.py

import requests, sys
import Ensembl

GeneSymbols = []
Species=[]
ID_ENSG=[]
'''
fichier = open("GeneSymbols.txt")
lignes = fichier.readlines()
print(lignes)'''

with open("GeneSymbols.txt") as f:
    lines = f.read().splitlines() 


#voir pour asso nom du gne et espce sinon doublon 
#un dictio avec cles / entrees pour a puis autres pour data ?
for line in lines:
	line = line.replace(" ", "_") #penser a gerer l'espace a la fin du premier Homo_sapiens
	GeneSymbolAndSpecie =  line.split("\t")
	GeneSymbols.append(GeneSymbolAndSpecie[0])
	Species.append(GeneSymbolAndSpecie[1])
print(GeneSymbols,Species)

for GeneSymbol in GeneSymbols:
	print(geneID(BRCA2,Homo_sapiens))
	
	
