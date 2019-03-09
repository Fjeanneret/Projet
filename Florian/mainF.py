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


def progressState(txt, widgetTextLines, state):
	"""
	Show beside gene symbol and specie line state of fetching
	"""
	
	lineIndex = "{}.end".format(widgetTextLines)
	txt.tag_config("Current", foreground="green")
	txt.insert(lineIndex, state, ('Current'))
	txt.update()	
	txt.delete("%s.first" % 'Current', "%s.last" % 'Current' ) 


def mainF(windows, data, result, txt):
	"""
	Parsing of data given in input to use gene symbol and specie names
	and call of annontation fetching functions
	"""

	widgetTextLines = 1
	collapseValue = 0



	lines = data.splitlines()
	for line in lines:
		print("\n------------------------- Gene suivant -----------------------------\n")

		line = line.rstrip(' ').replace(" ", "_")
		GeneSymbolAndSpecie =  line.split("\t")
		GeneSymbol = GeneSymbolAndSpecie[0]
		Specie = GeneSymbolAndSpecie[1]

		
		result.write("""<tr><td><span class='alert alert-success rounded-pill'>{}</span></td>\n<td>
		<span class='alert alert-success'>{}</span></td>""".format(Specie,GeneSymbol))

		# extractions des annotations

		# Start with EnsEMBL
		progressState(txt, widgetTextLines, ' EnsEMBL...',)

		genesList =  geneID_fetch(Specie, GeneSymbol, result, txt)	
		TranscriptID_ProtID_fetch(Specie, genesList, result)

		# Start with NCBI
		progressState(txt, widgetTextLines, ' NCBI...')
		NCBI_geneID = NCBIFetcher(Specie, GeneSymbol, result)

		progressState(txt, widgetTextLines, ' Refseq...')
		RefseqFetcher(NCBI_geneID, Specie, GeneSymbol, result)

		progressState(txt, widgetTextLines, ' KEGG...')
		kegg(NCBI_geneID, result)

		# Start with Uniprot
		progressState(txt, widgetTextLines, ' Uniprot...')
		UniprotID = proteinName_ID(Specie, GeneSymbol, result)

		progressState(txt, widgetTextLines, ' PDB...')
		PDB_ID(UniprotID, result)

		progressState(txt, widgetTextLines, ' GO...')
		qGO(UniprotID, result, collapseValue)

		progressState(txt, widgetTextLines, ' STRING...')
		interactionNetwork(UniprotID, result)

		progressState(txt, widgetTextLines, ' Pfam...')
		Pfam(UniprotID, result)

		progressState(txt, widgetTextLines, ' Prosite...')
		Prosite(UniprotID, result)
		
		result.write("</tr>")
		
		collapseValue += 100 # Using of unique identifier for collapse buttons

		# Progress visualiqation in text widget
		lineIndex = "{}.60".format(widgetTextLines)
		txt.tag_add("start", "1.0", lineIndex) 
		txt.tag_config("start", foreground="blue") # gene and specie text in red if fetching finished
		txt.update()
		widgetTextLines+=1
	
	txt.configure(foreground='#47ADA0') # gene and specie text in blue if entire fetching finished


	print("\n------------------------- Fin du processus -----------------------------\n")