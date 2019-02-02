import requests

def geneID_fetch(Species,GeneSymbols):
	
	#requete pour obtenir le fichier des genes id via le gene symbol et l'espece
	ensembl_dataBase = None #inutile ?

	genesList=[]
	server = "https://rest.ensembl.org"
	ext = "/xrefs/symbol/{}/{}".format(Species,GeneSymbols)
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	print(r)
	ensembl_server = True

	if not r.ok:
		ensembl_dataBase = False
		server = "https://rest.ensemblgenomes.org"
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

	geneData = r.json()


	def EnsEMBL_url_building(Species, geneID):
		#mettre en fction 
		#server = simplifier cette fonction , url etc
		'''if ensembl_dataBase == True:
			geneSummary_url = "https://www.ensembl.org/{}/Gene/Summary?db=core;g={};".format(Species,geneID)
			location_url = "https://www.ensembl.org/{}/Location/View?db=core;g={};".format(Species,geneID) 
			ortholog_url = "https://www.ensembl.org/{}/Gene/Compara_Ortholog?db=core;g={};".format(Species, geneID) #verifier si orthologues existent, autre fct pour autre td ?
			balise = "<a href={}>{}</a>".format(geneSummary_url,geneID)
			balise2 = "<a href={}>{}</a>".format(location_url, "genomeViewer")
			balise22 = "<a href={}>Liste des orthologues</a>".format(ortholog_url)
			print(balise)'''
		#else: 
		serversList = ["www","plants","fungi","Bacteria","Protists","Metazoa"]

		for dataBase in serversList:
			geneSummary_url = "https://{}.ensembl.org/{}/Gene/Summary?db=core;g={};".format(dataBase,Species, geneID)
			r = requests.get(geneSummary_url, headers={ "Content-Type" : "application/json"})
			if r.ok: break

		geneSummary_url = "https://{}.ensembl.org/{}/Gene/Summary?g={};".format(dataBase, Species, geneID)
		location_url = "https://{}.ensembl.org/{}/Location/View?db=core;g={};".format(dataBase, Species,geneID) 
		ortholog_url = "https://{}.ensembl.org/{}/Gene/Compara_Ortholog?db=core;g={};".format(dataBase, Species, geneID)
		#result.write("<a href={}>Liste des orthologues</a><br>".format(ortholog_url))
		#result.write("<br>")
		balise = "<a href={}>{}</a><br>".format(geneSummary_url,geneID)
		balise2 = "<a href={}>{}</a><br>".format(location_url, "genomeViewer")
		balise22 = "<a href={}>Liste des orthologues</a><br>".format(ortholog_url)
		print(balise)
		result.write(balise)
		result.write(balise2)
		result.write(balise22)

		#return {"Summary": geneSummary_url,"MapViewer": location_url, "Orthologs" : ortholog_url}
	#les differents id du fichier sont recuperes

	i=0  
	result = open("result.html", "a")
	result.write("<td>")

	while i<len(geneData):
		geneID = geneData[i]["id"]
		
		genesList.append(geneData[i]["id"])	
		#fct qui genere les liens relatifs 
		EnsEMBL_url_building(Species,geneID)

		#write summary et localisation puis br
		
		i+=1
		result.write("<br>")
	result.write("</td>\n")

	result.close()
	return genesList



def TranscriptID_ProtID_fetch(Species, geneIDs):
	proteinList=[]
	result = open("result.html", "a")
	result.write("<td>")
	for ID in geneIDs:

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
		
		while i<len(decoded["Transcript"]): #chacun des transcrits du fichier . . . avec 2 fct ? pour rna et prot ? puis affichage
			transcript_ID = decoded["Transcript"][i]["id"]
			#print(transcript_ID)
			#gerer database differente
			result.write("<a href=http://www.ensembl.org/{}/Transcript/Summary?db=core;t={}>{}</a><br>".format(Species,transcript_ID,transcript_ID))

			if decoded["Transcript"][i]["biotype"]=="protein_coding":
				transcript_ID = decoded["Transcript"][i]["id"]
				#print(decoded["Transcript"][i]["biotype"])
				#print(decoded["Transcript"])
				#print("ARN : ",decoded["Transcript"][i]["id"])
				proteinID = decoded["Transcript"][i]["Translation"]["id"] #mus musculus ENSM ...1547 :/
				proteinList.append(proteinID)
			i+=1
		result.write("<br>")
		print(proteinList)
	result.write("</td>\n")
	print(proteinList)
	result.write("<td>")
	for proteinID in proteinList:
		result.write("<a href=http://www.ensembl.org/{}/Transcript/Sequence_Protein?db=core;t={}>{}</a><br>".format(Species,proteinID, proteinID))
		result.write("<br>")
	result.write("</td>\n")
	result.close()

'''
#def protURL(proteinList)
	result.write("<td>")
	for proteinID in proteinList:
		result.write("<a href=http://www.ensembl.org/{}/Transcript/Sequence_Protein?db=core;t={}>{}</a><br>".format(Species,transcript_ID, proteinID))
		result.write("<br>")
	result.write("</td>\n")
	result.close()'''

	#liens des transcripts : http://www.ensembl.org/Homo_sapiens/Transcript/Summary?
	#db=core;g=ENSG00000139618;

	#liens des prots : ""...

	#a ecrire dans le fichier html 



# gerer creation lien orthologues selon si existent

# virer gene symbol et species si deja existentes