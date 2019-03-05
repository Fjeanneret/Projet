import requests
import re


def pfam(Uniprot_id,output_file):
	"""
	Fonction : pfam
	But : Obtenir les informations sur les domaines protéiques ainsi que le Graphical view
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying pfam for id...\n")
	requestURL="https://pfam.xfam.org/protein/{}?output=xml".format(Uniprot_id[0])
	r = requests.get(requestURL) #On récupère un XML
	match_acc = re.findall('(PF\d\d\d\d\d)',r.text) #On récupère tous les id pfam : il commence par PF suivi de 5 chiffres
	iden = re.findall('(id="\D.*"\s)',r.text) #On récupère le nom de l'id
	output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">')
	# On génère le lien du graphical View de pfam
	output_file.write('<a href="https://pfam.xfam.org/protein/{}'.format(Uniprot_id[0])+'">Graphical view</a><br><br>\n')
	i = 0
	# Pour chaque id pfam obtenu, on génère le lien de id pfam et sa description
	while i < len(match_acc):
		output_file.write('<a href="https://pfam.xfam.org/family/{}'.format(match_acc[i])+'">'+match_acc[i]+"</a><br>\n")
		output_file.write(iden[i]+"</a><br><br>\n")
		i = i + 1
	output_file.write("</div></td>")
	

	
	
	

