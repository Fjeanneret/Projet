import requests, re
from Ensembl import * 
from uniprot_pdb import * 
from ncbi import * 

def main(FileName):
	GeneSymbols = []
	Species=[]

	#passer le f en argument des fonctions 
	template = open("template.html","r")
	result = open("result.html","w")
	result.write(template.read())
	template.close()


	with open(FileName) as f:
	    lines = f.read().splitlines() 

	for line in lines:
		line = line.replace(" ", "_") #penser a gerer l'espace a la fin du premier Homo_sapiens
		GeneSymbolAndSpecie =  line.split("\t")
		GeneSymbols = GeneSymbolAndSpecie[0]
		Species = GeneSymbolAndSpecie[1]

		
		result.write("""<tr><td><span class='alert alert-success rounded-pill'>{}</span></td>\n<td>
		<span class='alert alert-success'>{}</span></td>""".format(Species,GeneSymbols))
		

		# extractions des annotations

		# Start with EnsEMBL
		genesList =  geneID_fetch(Species,GeneSymbols,result)	
		print(genesList)
		TranscriptID_ProtID_fetch(Species, genesList,result)

		# Start with NCBI
		NCBI_geneID = NCBIFetcher(Species,GeneSymbols,result)
		RefseqFetcher(NCBI_geneID, Species, GeneSymbols, result)


		# Start with Uniprot
		prot = proteinName_ID(Species,GeneSymbols,result)
		fromUniprotToPDB_ID(prot,result)
		interactionNetwork(prot,result)
		PfamFetcher(prot,result)
		PrositeFetcher(prot,result)


		result.write("</tr>")
		print("------------------------- Gene suivant -----------------------------")
	
	print(" Prêt à afficher ! ")


main("GeneSymbols.txt")