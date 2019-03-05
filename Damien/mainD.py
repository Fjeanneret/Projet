from .Uniprot import *
from .ensembl import *
from .PDB import *
from .NCBI import *
from .QuickGO import *
from .String import *
from .Kegg import *
from .prosite import *
from .pfam import *
import re
import tkinter as Tk
from tkinter.filedialog import *
import webbrowser

def mainD(interface, data, output_file, txt):
	"""
	Fonction : Main
	But : Appeler les différents programme et créer le fichier de résultat en html
	Retourne : //
	"""
	"""	fichier = open(fichier_input,"r") #Ouvre le fichier input en lecture
	output_file=open("result.html","w") #Ouvre le fichier result_projet.html en écriture
	"""
	#liste=fichier.readlines()
	l2=[] # liste intermédiaire
	symbol = []
	species=[]
	#"Parsage" du fichier et intégration des données dans deux listes : symbol (pour les GeneSymbol) et species.
	lines = data.splitlines()
	for line in lines:
		l2 = line.split("\t")
		l2[-1]=l2[-1].rstrip('\n')
		l2[-1]=l2[-1].rstrip(' ')
		l2[1] = re.sub('\s','_',l2[1])
		symbol.append(l2[0])
		species.append(l2[1])

	#output_file.write(template.read()) #On écrit dans le fichier result le template

	len_symbol = len(symbol)
	go_aspect=['biological_process','molecular_function','cellular_component'] #Liste qui sera utilisée par la fonction QuickGO
	z=0 #Utilisé par la boucle while qui appel les programmes
	print("\n")
	while z < len_symbol:
		print("Species = ",species[z],"Gene = ",symbol[z],"\n")
		if z < len_symbol:
			output_file.write("<tr><td>"+symbol[z]+"</td>\n")
		if z == len_symbol:
			output_file.write("<tr><td>"+symbol[z]+"</td>\n</tr>")
		output_file.write("<td>"+species[z]+"</td>\n")
		# Uniprot
		try:
			Uni_id = Uniprot_id(symbol[z],species[z],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			Uniprot_name(symbol[z],species[z],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		# PDB
		try:
			pdb(Uni_id,output_file)
		except:
			output_file.write('<td>**Error**</td>')
		# QuickGo
		try:
			quick_go(Uni_id,go_aspect[0],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			quick_go(Uni_id,go_aspect[1],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			quick_go(Uni_id,go_aspect[2],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		# Pfam
		try:
			pfam(Uni_id,output_file)
		except:
			output_file.write('<td>**Error**</td>')
		# String
		try:
			string(Uni_id,output_file)
		except:
			output_file.write('<td>**Error**</td>')
		# Prosite
		try:
			prosite(Uni_id,output_file)
		except:
			output_file.write('<td>**Error**</td>')
		# Ensembl
		url = database(symbol[z],species[z])
		try:
			ens_id = ensembl_id(symbol[z],species[z],output_file,url)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			ensembl_genome_browser(ens_id,symbol[z],species[z],output_file,url)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			ensembl_orthologue(ens_id,symbol[z],species[z],output_file,url)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			ensembl_transcripts(ens_id,symbol[z],species[z],output_file,url)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			ensembl_protein(ens_id,symbol[z],species[z],output_file,url)
		except:
			output_file.write('<td>**Error**</td>')
		# NCBI
		try:
			N_id = NCBI_id(symbol[z],species[z],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			NCBI_name(N_id,symbol[z],species[z],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			NCBI_transcripts(symbol[z],species[z],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			NCBI_proteins(symbol[z],species[z],output_file)
		except:
			output_file.write('<td>**Error**</td>')
		# Kegg
		try:
			kegg_ID = kegg_id(N_id,output_file)
		except:
			output_file.write('<td>**Error**</td>')
		try:
			kegg_paths(kegg_ID,output_file)
		except:
			output_file.write('<td>**Error**</td>')
		##
		print("\n")
		##
		z = z + 1
	progression = "Terminé!!" #On écrit Terminé dans l'interface
	print(progression)
	output_file.write("</tbody>\n") #On écrit la fin du html
	output_file.write("</table>\n")
	output_file.write("</body>\n")
	output_file.write("</html>\n")

