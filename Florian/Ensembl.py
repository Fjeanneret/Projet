import requests


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
			</div></div><br>""".format(summary,viewer,ortho)

	file.write(case)



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
	data = r.json()

	return data


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

	if len(data["data"]) == 0: #could be in ensemblgenomes server
		request = "https://rest.ensemblgenomes.org/homology/id/{}?format=condensed;type=orthologues&content-type=application/json".format(geneID)
		data = requests.get(request, headers={ "Content-Type" : "application/json"}) 
		data = data.json()
	
	indexTest = data["data"][0]["homologies"]
	if len(indexTest): #if the JSON content is not null we have ortholog information 
		orthologsExist = True

	return orthologsExist


def EnsEMBL_database(Species, geneID, urlTarget):
	"""
	Determine database where specie information are and return specific url
	"""

	dbList = ["www","plants","fungi","Bacteria","Protists","Metazoa"]

	for dataBase in dbList:
		# Summary url let to test if page exists, in case of 404 error another database is tested
		geneSummary_url = "https://{}.ensembl.org/{}/Gene/Summary?db=core;g={};".format(dataBase,Species, geneID)
		r = requests.get(geneSummary_url, headers = {"Content-Type" : "application/json"})
		if r.ok: break # If database is correct, iteration is broken

	urlBase = "https://{}.ensembl.org/{}/".format(dataBase, Species)
	url = urlBase + urlTarget

	return url


def EnsEMBL_url_building(Species, geneID,file):
	"""
	Url building function with HTML tag given to a bootstrap() function
	to improve appearance in result document
	"""

	HTMLtag = "<a class='{}' href={}>{}</a><br>"

	# Gene Summary url
	urlSummaryTarget = "/Gene/Summary?db=core;g={};".format(geneID)
	geneSummary_url = EnsEMBL_database(Species, geneID, urlSummaryTarget)

	# Genome Viewer url
	urlLocationTarget =  "/Location/View?db=core;g={};".format(geneID) 
	location_url = EnsEMBL_database(Species, geneID, urlLocationTarget)

	# Orthologs list url according to orthologs list exists or not. 
	if orthologsTest(geneID) == True : 
		urlOrthologTarget = '/Gene/Compara_Ortholog?db=core;g={};'.format(geneID)
		ortholog_url = EnsEMBL_database(Species, geneID, urlOrthologTarget) 
		tagOrtholog_url = HTMLtag.format('btn btn-warning', ortholog_url, "Liste des orthologues")

	else : 
		ortholog_url = ""
		tagOrtholog_url = "Pas d'orthologues\n"

	# Create HTML tags
	tagGeneSummary_url = HTMLtag.format('card-header', geneSummary_url,geneID)
	tagLocation_url = HTMLtag.format('btn btn-info', location_url, "genomeViewer")

	# Open and write in file with bootstrap function.
	bootstrap(tagGeneSummary_url,tagLocation_url,tagOrtholog_url,file)



## Essential functions to fetch ensEMBL information

def geneID_fetch(Species, GeneSymbols, file, txt):
	"""
	Get gene EnsEMBL ID with genesymbol and specie
	"""

	print("EnsEMBL...")
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
		i+=1

	file.write("</td>")

	return genesList


def TranscriptID_ProtID_fetch(Species, geneIDs,file):
	"""
	Get transcript and protein EnsEMBL ID with geneID and specie
	"""

	proteinList=[]
	HTMLtag = "<a class='list-group-item' href={}>{}</a><br>"
	"""	
	Transcipt and protein list fetching then url building and written
	"""

	file.write("<td><ul class='list-group'>")

	for geneID in geneIDs:
		ext = "/lookup/id/{}?expand=1".format(geneID)
		dataGet = dataFetchingRequest(ext)

		i=0
		while i<len(dataGet["Transcript"]): # Transcript information are at "Transcript" key
			transcript_ID = dataGet["Transcript"][i]["id"]
			urlTranscriptTarget = "/Transcript/Summary?db=core;t={}".format(transcript_ID)
			transcript_url = EnsEMBL_database(Species, geneID, urlTranscriptTarget)
			tagTranscript_url = HTMLtag.format(transcript_url, transcript_ID)
			file.write(tagTranscript_url)

			# Looking for protein ID only if transcript is protein coding in json file get
			if dataGet["Transcript"][i]["biotype"] == "protein_coding": # Check if proteins exist
				transcript_ID = dataGet["Transcript"][i]["id"]
				proteinID = dataGet["Transcript"][i]["Translation"]["id"] #
				proteinList.append(proteinID)

			i+=1

		file.write("<hr>") # spliting blocks in case of numerous gene ID

	# Write in result file proteins
	file.write("</ul></td>\n")
	file.write("<td><ul class='list-group'>")

	protein_url_list = []
	for protein_ID in proteinList:
		urlProteinTarget = "/Transcript/Sequence_Protein?db=core;t={}".format(protein_ID, protein_ID)
		protein_url = EnsEMBL_database(Species, geneID, urlProteinTarget)
		tagProtein_url = HTMLtag.format(protein_url, protein_ID)

		file.write(tagProtein_url)
		file.write("<br>")

	file.write("<hr>")
	file.write("</ul></td>\n")
	