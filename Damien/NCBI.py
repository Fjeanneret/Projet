import requests
import re

def NCBI_id(symbol,species,output_file):
	"""
	Fonction : NCBI_id
	But : Récupérer les id (Gene access number) de la naque gene du NCBI
	Méthode : requests.get 
	Retourne : La liste les id de la banque gene du NCBI
	"""
	print("Querying NCBI for id...\n")
	url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term={}[ORGN]+{}[GENE]&idtype=acc&retmode=json".format(species,symbol)
	r = requests.get(url)
	result = r.json() # On décode le résultat en json
	i = 0
	NCBI_id = []
	while i < len(result["esearchresult"]["idlist"]):
		if i == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
		if i >= 0:
			NCBI_id.append(result["esearchresult"]["idlist"][i])
			output_file.write('<a href="https://www.ncbi.nlm.nih.gov/gene/{}'.format(NCBI_id[i])+'">'+NCBI_id[i]+'</a><br>')
		if i == len(result["esearchresult"]["idlist"])-1:
			output_file.write("</div></td>\n")
		i = i + 1
	return(NCBI_id)

def NCBI_name(N_id,symbol,species,output_file):
	"""
	Fonction : NCBI_name
	But : Récupérer le nom de la protéine sur le NCBI
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying NCBI for official name...\n")
	output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">')
	if len(N_id) == 0:
		output_file.write('No_data')
	for N_id in N_id:
		url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id={}&retmode=json".format(N_id)
		r = requests.get(url)
		result = r.json() # On décode le résultat en json
		NCBI_name = result["result"][N_id]["nomenclaturename"]
		if NCBI_name == "":
			output_file.write('No_data<br>')
		else:
			output_file.write(NCBI_name+'<br>')
	output_file.write('</div></td>')
	return()

def NCBI_transcripts(symbol,species,output_file):
	"""
	Fonction : NCBI_transcripts
	But : Récupérer le RNA access number sur le RefSeq
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying NCBI for transcripts id...\n")
	url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term={}[ORGN]+{}[GENE]&idtype=acc&retmode=json".format(species,symbol)
	r = requests.get(url)
	result = r.json() # On décode le résultat en json
	NCBI_list_NM = result["esearchresult"]["idlist"]
	NCBI_list_NM = ','.join(NCBI_list_NM)
	i = 0
	NCBI_NM = re.findall('(NM_\d{0,10}.\d{0,2})',NCBI_list_NM)
	if len(NCBI_NM) == 0:
		output_file.write('<td>No_data</td>')
	while i < len(NCBI_NM):
		if i == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">')
		if i >= 0:
			output_file.write('<a href="https://www.ncbi.nlm.nih.gov/nuccore/{}'.format(NCBI_NM[i])+'">'+NCBI_NM[i]+'</a><br>')
			output_file.write('<a href="http://genome.ucsc.edu/cgi-bin/hgTracks?org={}&position={}'.format(species, NCBI_NM[i])+'"> 	Genome Browser</a><br>')
		if i == len(NCBI_NM)-1:
			output_file.write('</div></td>')
		i = i + 1
	return()
		
		
def NCBI_proteins(symbol,species,output_file):
	"""
	Fonction : NCBI_proteins
	But : Récupérer le Protein acces number
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying NCBI for protein id...\n")
	url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term={}[ORGN]+{}[GENE]&idtype=acc&retmode=json".format(species,symbol)
	r = requests.get(url)
	result = r.json() # On décode le résultat en json
	NCBI_list_NP = result["esearchresult"]["idlist"]
	NCBI_list_NP = ','.join(NCBI_list_NP)
	NCBI_NP = re.findall('(NP_\d{0,10}.\d{0,2})',NCBI_list_NP)
	j = 0
	if len(NCBI_NP) == 0:
		output_file.write('<td>No_data</td>')
	while j < len(NCBI_NP):
		if j == 0:
			output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">')
		if j >= 0:
			output_file.write('<a href="https://www.ncbi.nlm.nih.gov/nuccore/{}'.format(NCBI_NP[0])+'">'+NCBI_NP[0]+'</a><br>')
		if j == len(NCBI_NP)-1:
			output_file.write('</div></td>')
		j = j + 1
	return()


