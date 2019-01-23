import requests, sys

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
#print(GeneSymbols,Species)

i = 0

while i < len(GeneSymbols):


	server = "https://rest.ensembl.org"
	#ext = "/xrefs/symbol/homo_sapiens/BRCA2?"
	ext = "/xrefs/symbol/{}/{}".format(Species[i],GeneSymbols[i])
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	 
	if not r.ok:
		server = "https://rest.ensemblgenomes.org"
		ext = "/xrefs/symbol/{}/{}?".format(Species[i],GeneSymbols[i])
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
		
	  #r.raise_for_status()
	  #sys.exit()
	
	decoded = r.json()
	
	ID_ENSG.append(decoded[0]["id"])
	i+=1
	
	
print(ID_ENSG)
	
