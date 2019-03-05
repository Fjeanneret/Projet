import requests

def database(symbol,species):
	"""
	Fonction : database
	But : Sélectionner la base de données correspondant à l'espèce
	Méthode : requests.get
	Retourne : L'url de la base de données sélectionnée
	"""
	databases_list=["www","plants","fungi","Bacteria","Protists","Metazoa"]
	for database in databases_list:
		url = "https://{}.ensembl.org/{}/Gene/Summary?db=core;g={};".format(database,species,symbol)
		url_bis = "https://{}.ensembl.org/{}".format(database,species)
		r_test = requests.get(url, headers = {"Content-Type" : "application/json"})
		if r_test.ok: break
	return(url_bis)

def ensembl_id(symbol,species,output_file,url):
	"""
	Fonction : ensembl_id
	But : Récupérer les id ensembl
	Méthode : requests.get
	Retourne : La liste des id ensembl
	"""
	print("Querying ensembl id...\n")
	server = "https://rest.ensembl.org"
	ext = "/xrefs/symbol/{}/{}?".format(species,symbol)
	result = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	decoded = result.json() # On décode le résultat en json
	i = 0
	ensembl_id_list=[]
	while i < len(decoded):
		j = 0
		if i == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
		if result.ok:
			ensembl_id_list.append(decoded[i]["id"])
			output_file.write("<a href="+'"'+url+"/Gene/Summary?db=core;g={}".format(decoded[i]["id"])+'"'+">"+decoded[i]["id"]+"</a>"+"<br>\n")
		if not result.ok:
			server = "https://rest.ensemblgenomes.org"
			ext = "/xrefs/symbol/{}/{}?".format(species,symbol)
			result = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
			decoded = result.json()
			ensembl_id_list.append(decoded[i]["id"])
			output_file.write("<a href="+'"'+url+"/Gene/Summary?db=core;g={}".format(decoded[i]["id"])+'"'+">"+decoded[i]["id"]+"</a>"+"<br>\n")
		if i == len(decoded)-1:
			output_file.write("</div></td>\n")
		i = i + 1
	return(ensembl_id_list)


def ensembl_orthologue(ensembl_id,symbol,species,output_file,url):
	"""
	Fonction : ensembl_orthologue
	But : Récupérer la liste des orthologues
	Méthode : génération d'un url
	Retourne : //
	"""
	print("Querying ensembl Orthologues...\n")
	z = 0
	while z < len(ensembl_id):
		if z == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
		try:
			output_file.write('<a href="'+url+'/Gene/Compara_Ortholog?db=core;g={}'.format(ensembl_id[z])+'">Orthologues</a>\n')
		except:
			output_file.write("<a href="+'"'+url+'/Gene/Compara_Ortholog?db=core;g={}'.format(species,ensembl_id[z])+'">Orthologues</a>\n')
		if z == len(ensembl_id) - 1:
			output_file.write("</div></td>\n")
		z = z + 1
	return()

def ensembl_genome_browser(ensembl_id,symbol,species,output_file,url):
	"""
	Fonction : ensembl_genome_browser
	But : Permet de générer le lien vers le genome browser
	Méthode : requests.get
	Retourne : //
	"""	
	print("Querying ensembl Genome Browser...\n")
	z = 0
	while z < len(ensembl_id):
		if z == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
		try:
			output_file.write('<a href="'+url+"/Location/View?db=core;g={}".format(ensembl_id[z])+'"'+'>Genome Browser</a><br>\n')
		except:
			server = "https://rest.ensemblgenomes.org"
			ext = "/xrefs/symbol/{}/{}?".format(species,symbol)
			result = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
			decoded = result.json() # On décode le résultat en json
			results.append(decoded[z]["id"])
			output_file.write("<a href="+'"'+url+"/Location/View?db=core;g={}".format(decoded[z]["id"])+'"'+">Genome Browser</a><br>\n")
		if z == len(ensembl_id)-1:
			output_file.write("</div></td>\n")
		z = z + 1
	return()

def ensembl_transcripts(ensembl_id,symbol,species,output_file,url):
	"""
	Fonction : ensembl_transcripts
	But : Obtenir le RNA access number d'ensembl et génération du lien
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying ensembl transcripts...\n")
	w = 0
	# On parcourt la liste des id ensembl
	while w < len(ensembl_id):
		server = "https://rest.ensembl.org"
		ext = "/lookup/id/{}?expand=1".format(ensembl_id[w])
		result = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
		decoded = result.json() # On décode le résultat en json
		j = 0
		if w == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
		while j < len(decoded):
			try:
				if result.ok:
					output_file.write("<a href="+'"'+url+"/Transcript/Summary?db=core;t={}".format(decoded["Transcript"][j]["id"])+'"'+">"+decoded["Transcript"][j]["id"]+"</a><br>\n")
				if not result.ok:
					server = "https://rest.ensemblgenomes.org"
					ext = "/lookup/id/{}?expand=1".format(ensembl_id[w])
					result = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
					decoded = result.json()
					output_file.write("<a href="+'"'+url+"/Transcript/Summary?db=core;t={}".format(decoded["Transcript"][j]["id"])+'"'+">"+decoded["Transcript"][j]["id"]+"</a><br>\n")
			except:
				if j == len(decoded)+9:
					output_file.write("</div></td>\n")
			j = j + 1
		if w == len(decoded)-1:
			output_file.write("</div></td>\n")
		w = w + 1
	return()

def ensembl_protein(ensembl_id,symbol,species,output_file,url):
	"""
	Fonction : ensembl_protein
	But : Obtenir le Protein acces number d'ensembl et génération du lien
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying ensembl proteins...\n")
	w = 0
	#On parcourt la liste des id ensembl
	while w < len(ensembl_id):
		server = "https://rest.ensembl.org"
		ext = "/lookup/id/{}?expand=1".format(ensembl_id[w])
		result = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
		decoded = result.json() # On décode le résultat en json
		j = 0
		if w == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
		while j < len(decoded):
			try:
				if result.ok:
					output_file.write("<a href="+'"'+url.format(species)+"/Transcript/ProteinSummary?db=core;p={}".format(decoded["Transcript"][j]["Translation"]["id"])+'"'+">"+decoded["Transcript"][j]["Translation"]["id"]+"</a><br>\n")
				if not result.ok:
					server = "https://rest.ensemblgenomes.org"
					ext = "/lookup/id/{}?expand=1".format(ensembl_id[w])
					result = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
					decoded = result.json()
					output_file.write("<a href="+'"'+url+"/Transcript/ProteinSummary?db=core;p={}".format(decoded["Transcript"][j]["Translation"]["id"])+'"'+">"+decoded["Transcript"][j]["Translation"]["id"]+"</a><br>\n")
			except:
				if j == len(decoded)+9:
					output_file.write("</div></td>\n")
			j = j + 1
		if w == len(decoded)-1:
			output_file.write("</div></td>\n")
		w = w + 1
	return()

