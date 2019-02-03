import requests

def dataFetchingRequest(ext):
	server = "https://rest.ensembl.org"
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

	if not r.ok:
		
		server = "https://rest.ensemblgenomes.org"
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	Data = r.json()
	return Data

def orthologsTest(geneID):
	#a faire avec /homologies
	orthologsExist = None
	ext = "/homology/id/{}?format=condensed;type=orthologues".format(geneID)
	data = dataFetchingRequest(ext)
	if len(data["data"]) != 0:
		indexTest = data["data"][0]["homologies"]
	else : indexTest = data["data"]
	if len(indexTest) > 1:
		orthologsExist = True
	return orthologsExist

def EnsEMBL_url_building(Species, geneID):
	dbList = ["www","plants","fungi","Bacteria","Protists","Metazoa"]

	for dataBase in dbList:
		geneSummary_url = "https://{}.ensembl.org/{}/Gene/Summary?db=core;g={};".format(dataBase,Species, geneID)
		r = requests.get(geneSummary_url, headers={ "Content-Type" : "application/json"})
		if r.ok: break
	urlBase = "https://{}.ensembl.org/{}/".format(dataBase, Species)
	geneSummary_url = urlBase + "/Gene/Summary?g={};".format(geneID)
	location_url = urlBase + "/Location/View?db=core;g={};".format(geneID) 

	if orthologsTest(geneID) == True : 
		ortholog_url = urlBase + "/Gene/Compara_Ortholog?db=core;g={};".format(geneID)
		balise22 = "<a href={}>Liste des orthologues</a><br><br>".format(ortholog_url)
	else : 
		ortholog_url = ""
		balise22 = "Pas d'orthologues\n"

	balise = "<a href={}>{}</a><br>".format(geneSummary_url,geneID)
	balise2 = "<a href={}>{}</a><br>".format(location_url, "genomeViewer")

	result = open("result.html", "a")
	result.write(balise)
	result.write(balise2)
	result.write(balise22)
	result.close()


def geneID_fetch(Species,GeneSymbols):
	#requete pour obtenir le fichier des genes id via le gene symbol et l'espece
	genesList=[]
	ext = "/xrefs/symbol/{}/{}".format(Species,GeneSymbols)
	geneData = dataFetchingRequest(ext)
	i=0
	result = open("result.html", "a")
	result.write("<td>")
	result.close()
	while i<len(geneData):
		geneID = geneData[i]["id"]
		genesList.append(geneID)	
		#fct qui genere les liens relatifs 
		EnsEMBL_url_building(Species,geneID)
		#result.write("<br>")
		i+=1
	result = open("result.html", "a")
	result.write("</td>")
	result.close()
	return genesList


def TranscriptID_ProtID_fetch(Species, geneIDs):
	proteinList=[]
	result = open("result.html", "a")
	result.write("<td>")
	for ID in geneIDs:
		ext = "/lookup/id/{}?expand=1".format(ID)
		dataGet = dataFetchingRequest(ext)

		i=0
		while i<len(dataGet["Transcript"]): #chacun des transcrits du fichier . . . avec 2 fct ? pour rna et prot ? puis affichage
			transcript_ID = dataGet["Transcript"][i]["id"]
			#print(transcript_ID)
			#gerer database differente
			result.write("<a href=http://www.ensembl.org/{}/Transcript/Summary?db=core;t={}>{}</a><br>".format(Species,transcript_ID,transcript_ID))

			if dataGet["Transcript"][i]["biotype"]=="protein_coding":
				transcript_ID = dataGet["Transcript"][i]["id"]
				#print(decoded["Transcript"][i]["biotype"])
				#print(decoded["Transcript"])
				#print("ARN : ",decoded["Transcript"][i]["id"])
				proteinID = dataGet["Transcript"][i]["Translation"]["id"] #mus musculus ENSM ...1547 :/
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