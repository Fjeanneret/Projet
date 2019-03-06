import requests, re
from Florian.Ensembl import * 
from Florian.Uniprot import * 
from Florian.ncbi import *
from Florian.PDB import *
from Florian.Pfam import * 
from Florian.Prosite import * 
from Florian.KEGG import * 
from Florian.qGO import * 
from Florian.String import * 
from tkinter import *
from tkinter.filedialog import *

	
def mainF(windows, data, result, txt):

	truc = 1
	arbitraryValue = 0
	GeneSymbols = []
	Species=[]

	lines = data.splitlines()
	for line in lines:
		print("------------------------- Gene suivant -----------------------------")

		line = line.replace(" ", "_") #penser a gerer l'espace a la fin du premier Homo_sapiens
		GeneSymbolAndSpecie =  line.split("\t")
		GeneSymbol = GeneSymbolAndSpecie[0]
		Specie = GeneSymbolAndSpecie[1]

		
		result.write("""<tr><td><span class='alert alert-success rounded-pill'>{}</span></td>\n<td>
		<span class='alert alert-success'>{}</span></td>""".format(Specie,GeneSymbol))

		# extractions des annotations

		# Start with EnsEMBL
		genesList =  geneID_fetch(Specie,GeneSymbol,result)	
		TranscriptID_ProtID_fetch(Specie, genesList,result)

		# Start with NCBI"""
		NCBI_geneID = NCBIFetcher(Specie,GeneSymbol,result)
		RefseqFetcher(NCBI_geneID, Specie, GeneSymbol, result)
		kegg(NCBI_geneID,result)

		# Start with Uniprot
		UniprotID = proteinName_ID(Specie,GeneSymbol,result)
		PDB_ID(UniprotID,result)

		qGO(UniprotID, result, arbitraryValue)
		interactionNetwork(UniprotID,result)
		Pfam(UniprotID,result)
		Prosite(UniprotID,result)
		
		result.write("</tr>")
		
		
		
		arbitraryValue += 100  
		#if truc < len(lines):
		t2="{}.60".format(truc)
		txt.tag_add("start", "1.0", t2)
		txt.tag_config("start", foreground="red")
		txt.update()
		truc+=1
	print("------------------------- Fin du processus -----------------------------")
	t2="{}.60".format(truc+1)
	txt.tag_add("start", "1.0", t2)
	txt.tag_config("start", foreground="#47ADA0")