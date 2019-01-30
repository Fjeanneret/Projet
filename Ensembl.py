#Ensembl

#for nombre de trucs
	
#main^

import requests

def geneID_fetch(GeneSymbols,Species):
	ensembl_server = None 
	ID_ENSG=[]
	server = "https://rest.ensembl.org"
	ext = "/xrefs/symbol/{}/{}".format(Species,GeneSymbols)
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	ensembl_server = True

	if not r.ok:
		ensembl_server = False
		server = "https://rest.ensemblgenomes.org"
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	
	decoded = r.json()
	
	i=0  
	while i<len(decoded):
		#ecrire dans fichier à la place
		ID_ENSG.append(decoded[i]["id"])		
		i+=1
		
	print(ID_ENSG)

	#gerer si plant,fungi...

	#Orthologs fetching
	j=0
	while j <len(ID_ENSG):

		if ensembl_server == True:
			geneSummary_url = "https://www.ensembl.org/{}/Gene/Summary?db=core;g={};".format(Species,ID_ENSG[j])
			ortholog_url = "https://www.ensembl.org/{}/Location/View?db=core;g={};".format(Species,ID_ENSG[j])
		else: 
			serverIndex=0
			serversList = ["plants","fungi","Bacteria","Protists","Metazoa"]
			ortholog_url = "https://{}.ensembl.org/{}/Gene/Compara_Ortholog?db=core;g={};".format(serversList[serverIndex],Species, ID_ENSG[j])
			r = requests.get(ortholog_url, headers={ "Content-Type" : "application/json"})
			print("plant")

			if not r.ok:
				serverIndex +=1
				ortholog_url = "https://{}.ensembl.org/{}/Gene/Compara_Ortholog?db=core;g={};".format(serversList[serverIndex],Species, ID_ENSG[j])
				r = requests.get(ortholog_url, headers={ "Content-Type" : "application/json"})
				
				print("fungi")
				if not r.ok:
					serverIndex +=1					
					ortholog_url = "https://{}.ensembl.org/{}/Gene/Compara_Ortholog?db=core;g={};".format(serversList[serverIndex],Species, ID_ENSG[j])
					r = requests.get(ortholog_url, headers={ "Content-Type" : "application/json"})
					
					print("Protists")
					if not r.ok:
						erverIndex +=1	
						ortholog_url = "https://{}.ensembl.org/{}/Gene/Compara_Ortholog?db=core;g={};".format(serversList[serverIndex],Species, ID_ENSG[j])
						r = requests.get(ortholog_url, headers={ "Content-Type" : "application/json"})
						
						print("Bacteria")
						if not r.ok:
							erverIndex +=1	
							ortholog_url = "https://{}.ensembl.org/{}/Gene/Compara_Ortholog?db=core;g={};".format(serversList[serverIndex],Species, ID_ENSG[j])
							r = requests.get(ortholog_url, headers={ "Content-Type" : "application/json"})
							print("Metazoa")
			geneSummary_url = "http://{}.ensembl.org/{}/Gene/Summary?g={};".format(serversList[serverIndex], Species, ID_ENSG[j])
		print(ortholog_url,"\n",geneSummary_url)
		j+=1

	return ID_ENSG


def TranscriptID_ProtID_fetch(ID):

	server = "https://rest.ensembl.org"
	ext = "/lookup/id/{}?expand=1".format(ID)
	print("Recherche dans ensembl...")
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

	if not r.ok:
		print("Recherche dans ensemblgenomes...")
		server = "https://rest.ensemblgenomes.org"
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	
	decoded = r.json()

	i=0
	for transcript in decoded["Transcript"]:
		
		if decoded["Transcript"][i]["biotype"]=="protein_coding":
			print("ARN : ",decoded["Transcript"][i]["id"])
			print("Proteine : ",decoded["Transcript"][i]["Translation"]["id"])
		i=i+1
	#liens des transcripts : http://www.ensembl.org/Homo_sapiens/Transcript/ProteinSummary?
	#db=core;g=ENSG00000139618;r=13:32315474-32400266;t=ENST00000380152

	#liens des prots : ""...

	#a ecrire dans le fichier html 
