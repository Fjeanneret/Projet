import requests

def kegg_id(N_id,output_file):
	"""
	Fonction : kegg_id
	But : Obtenir les kegg id
	Méthode : requests.get
	Retourne : le kegg id
	"""
	print("Querying Kegg for id...\n")
	Liste_id=[]
	requestURL="http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(N_id[0])
	result = requests.get(requestURL)
	liste_result = result.text.rstrip("\n").split('\t') #Split dans une liste le résultat de la recherche
	output_file.write('<td><div style="max-height:300px;width:120%;overflow-x:auto"><a href="https://www.kegg.jp/dbget-bin/www_bget?{}'.format(liste_result[1])+'">'+liste_result[1]+'</a></div></td>\n')
	return(liste_result[1])

def kegg_paths(kegg_id,output_file):
	"""
	Fonction : kegg_paths
	But : Obtenir les pathways
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying Kegg for pathways...\n")
	gene_paths = requests.get('http://rest.kegg.jp/link/pathway/{}'.format(kegg_id))
	lines = gene_paths.text.splitlines()
	paths_id = []
	for l in lines:
		if l not in paths_id: #On ne prend pas les doublons
			inter = l.split('\t')[1] #Chaque id des pathways est en deuxième position
			paths_id.append(inter.split(':')[1]) #On stocke les id pathways dans une liste	
	j = 0
	# On parcourt la liste des pathways
	# On fait une requête pour chacun d'entres eux
	while j < len(paths_id):
		if j == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">')
		if j >= 0:
			gene_paths_name = requests.get('http://rest.kegg.jp/get/{}'.format(paths_id[j]))
			# On parse le xml obtenu (on utilise une variable intermédiaire intervar)
			intervar = gene_paths_name.text.split('\n') #On split chaque ligne
			intervar = intervar[1]  #On garde le deuxième élément contenant le nom de la pathway
			intervar = intervar.split(" ") #On split en fonction des espaces
			del intervar[0:8] # On supprime les 8 premiers éléments
			del intervar[-4:] # On supprime les 4 derniers éléments
			i = 0
			pathway = " ".join(intervar) # On créé un string à partir de la liste intervar contenant le pathway
			output_file.write('<a href="https://www.kegg.jp/kegg-bin/show_pathway?{}'.format(paths_id[j])+'">'+paths_id[j]+'</a>'+" "+pathway+"</a><br>\n")
		if j == len(paths_id):
			output_file.write("</div></td>")
		j = j + 1
