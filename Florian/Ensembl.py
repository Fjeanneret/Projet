import requests

## Function to help information fetching and writing

def dataFetchingRequest(ext):
	"""
	Let to make a request in ensembl rest API
	What we want to fetch is provide by ext element

	First request with ensembl.org then ensemblegenomes.org
	in case of empty answer.
	"""

	server = "https://rest.ensembl.org"
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

	if not r.ok:
		
		server = "https://rest.ensemblgenomes.org"
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	Data = r.json()
	return Data


def orthologsTest(geneID):
	"""
	Let to know if an orthologs list exists.

	Return True or False
	"""

	orthologsExist = None

	# Make homology list request
	request = "https://rest.ensembl.org/homology/id/{}?format=condensed;type=orthologues&content-type=application/json".format(geneID)
	data = requests.get(request, headers={ "Content-Type" : "application/json"}) 
	data = data.json()

	if len(data["data"]) == 0:
		request = "https://rest.ensemblgenomes.org/homology/id/{}?format=condensed;type=orthologues&content-type=application/json".format(geneID)
		data = requests.get(request, headers={ "Content-Type" : "application/json"}) 
		data = data.json()

	

	# Test of relevant indexes of data fetched in json format
	#if len(data["data"]) == 0:
	#orthologsExist = False
	
	
	indexTest = data["data"][0]["homologies"]
	
	if len(indexTest):
		orthologsExist = True

	return orthologsExist


def EnsEMBL_url_building(Species, geneID,file):
	dbList = ["www","plants","fungi","Bacteria","Protists","Metazoa"]

	for dataBase in dbList:
		geneSummary_url = "https://{}.ensembl.org/{}/Gene/Summary?db=core;g={};".format(dataBase,Species, geneID)
		r = requests.get(geneSummary_url, headers = {"Content-Type" : "application/json"})
		if r.ok: break

	urlBase = "https://{}.ensembl.org/{}/".format(dataBase, Species)
	location_url = urlBase + "/Location/View?db=core;g={};".format(geneID) 

	# Orthologs list url according to orthologs list exists or not. 
	if orthologsTest(geneID) == True : 
		ortholog_url = urlBase + "/Gene/Compara_Ortholog?db=core;g={};".format(geneID)
		tagOrtholog_url = "<a class='btn btn-warning' href={}>Liste des orthologues</a><br>\n".format(ortholog_url)
	else : 
		ortholog_url = ""
		tagOrtholog_url = "Pas d'orthologues\n"

	# Create HTML tags
	tagGeneSummary_url = "<a class='card-header' href={}>{}</a><br>".format(geneSummary_url,geneID)
	tagLocation_url = "<a class='btn btn-info' href={}>{}</a><br>".format(location_url, "genomeViewer")

	# Open and write in file with bootstrap function.
	bootstrap(tagGeneSummary_url,tagLocation_url,tagOrtholog_url,file)
	

## Esthetic functions

def bootstrap(summary,viewer,ortho,file):
	"""
	Add bootstrap element to enhance form and write 
	in table file
	"""

	case = """<div class="card text-center">
		{}
		<br>
			<div class="card-body">{}
			<br><br>
				{}
			</div>

	</div><br>""".format(summary,viewer,ortho)

	file.write(case)


## Essential functions to fetch ensEMBL information

def geneID_fetch(Species,GeneSymbols,file):
	"""
	Get gene EnsEMBL ID with genesymbol and specie
	"""

	genesList=[]
	ext = "/xrefs/symbol/{}/{}".format(Species,GeneSymbols)
	geneData = dataFetchingRequest(ext)

	# Create td tag with data fetched
	i=0
	
	file.write("<td>")
	
	while i<len(geneData):
		geneID = geneData[i]["id"]
		genesList.append(geneID)	 
		EnsEMBL_url_building(Species,geneID,file)
		#result.write("<br>")
		i+=1
	
	file.write("</td>")
	

	return genesList


def TranscriptID_ProtID_fetch(Species, geneIDs,file):
	"""
	Get transcript and protein EnsEMBL ID with geneID and specie
	"""

	proteinList=[]
	
	file.write("<td><ul class='list-group'>")

	for ID in geneIDs:
		ext = "/lookup/id/{}?expand=1".format(ID)
		dataGet = dataFetchingRequest(ext)

		i=0
		while i<len(dataGet["Transcript"]): 
			transcript_ID = dataGet["Transcript"][i]["id"]
			file.write("""<a  class='list-group-item' 
			href=http://www.ensembl.org/{}/Transcript/Summary?db=core;t={}>{}</a><br>""".format(Species,transcript_ID,transcript_ID))

			# Looking for protein ID only if transcript is protein coding in json file get
			if dataGet["Transcript"][i]["biotype"] == "protein_coding":
				transcript_ID = dataGet["Transcript"][i]["id"]
				proteinID = dataGet["Transcript"][i]["Translation"]["id"] 
				proteinList.append(proteinID)
			
			i+=1
		file.write("<hr>")

	file.write("</ul></td>\n")
	print(proteinList)
	file.write("<td><ul class='list-group'>")

	protein_url_list = []
	for proteinID in proteinList:
		file.write("<a class='list-group-item' href=http://www.ensembl.org/{}/Transcript/Sequence_Protein?db=core;t={}>{}</a><br>".format(Species,proteinID, proteinID))
		file.write("<br>")

	file.write("<hr>")
	file.write("</ul></td>\n")
	