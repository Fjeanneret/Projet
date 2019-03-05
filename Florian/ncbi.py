import requests, re

def bootstrap(summary,viewer,ortho, geneName, file):
	"""
	Add bootstrap element to enhance form and write 
	in table file
	"""

	case = """
	<td>
	<div class="card text-center">
		{}
		<br>
			<div class="card-body">{}
			<br>
				{}
			</div>
	</div>
	<div class="card-footer text-muted">
    {}
  	</div>
	</td>""".format(summary,viewer,ortho, geneName)

	file.write(case)

def NCBIorthologsTest(NCBI_ID):
	"""

	"""

	orthologsExist = None
	APIserver = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	NMtool = "esearch.fcgi?db=GENE&term=ortholog_gene_{}[group]&retmode=json".format(NCBI_ID)
	Orthologs_response = requests.get(APIserver+NMtool, headers={ "Content-Type" : "application/json"})

	if len(Orthologs_response.json()["esearchresult"]["idlist"]) != 0:	
		orthologsExist = True
		#ecrire url dans card

	return orthologsExist


def NCBIFetcher(Species,GeneSymbols,file):
	"""
	Get gene EnsEMBL ID with genesymbol and specie
	"""

	APIserver = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	tool = "esearch.fcgi?db=gene&term={}[ORGN]+{}[GENE]&idtype=acc&retmode=json".format(Species,GeneSymbols) #get id
	ID_response = requests.get(APIserver+tool, headers={ "Content-Type" : "application/json"})
	if ID_response.ok:
		NCBI_ID = ID_response.json()["esearchresult"]["idlist"][0] #0 only ? 
		print(NCBI_ID) # construire et ecrire lien
		geneSummary_url = "https://www.ncbi.nlm.nih.gov/gene/{}".format(NCBI_ID)

		tool = "esummary.fcgi?db=gene&id={}&retmode=json".format(NCBI_ID)
		Summary_response = requests.get(APIserver+tool, headers={ "Content-Type" : "application/json"})

		if Summary_response.ok:
			CompleteGeneName = Summary_response.json()["result"][NCBI_ID]["nomenclaturename"]
			print(CompleteGeneName) # ecrire

		else : print("no summary information")

		if NCBIorthologsTest(NCBI_ID) == True :
			Ortholog_url = "https://www.ncbi.nlm.nih.gov/gene/?Term=ortholog_gene_675[group]"
			tagOrtholog_url = "<a class='btn btn-warning' href={}>Liste des orthologues</a><br>".format(Ortholog_url)
		else : 
			ortholog_url = ""
			tagOrtholog_url = "Pas d'orthologues\n"

		tagGeneSummary_url = "<a class='card-header' href={}>{}</a><br>".format(geneSummary_url,NCBI_ID)

		Location_url = "https://www.ncbi.nlm.nih.gov/genome/gdv/browser/?context=gene&acc={}".format(NCBI_ID)
		tagLocation_url = "<a class='btn btn-info' href={}>{}</a><br>".format(Location_url, "genomeViewer")

		bootstrap(tagGeneSummary_url,tagLocation_url,tagOrtholog_url, CompleteGeneName, file)

	else :
		print("no id")
		bootstrap("no data","no data","no data", "no data", file)
	return NCBI_ID


def RefseqFetcher(NCBI_ID, Species, GeneSymbols, file):
	"""

	"""
	# a fonctionnaliser
	APIserver = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	NMtool = "esearch.fcgi?db=nucleotide&term=homo_sapiens[ORGN]+brca2[GENE]&idtype=acc&retmode=json".format(Species,GeneSymbols) #get id
	Transcripts_response = requests.get(APIserver+NMtool, headers={ "Content-Type" : "application/json"})

	file.write("<td>")
	if Transcripts_response.ok:
		list_ID = Transcripts_response.json()["esearchresult"]["idlist"] 
		for ID in list_ID:
			if "NM" in ID:
				print(ID) # construire et ecrire lien
				Transcript_url = "https://www.ncbi.nlm.nih.gov/nuccore/{}".format(ID)
				tagTranscript_url = "<a  class='list-group-item' href='{}'>{}</a><br>".format(Transcript_url, ID)
				file.write(tagTranscript_url)

	file.write("</td>")
	
	NPtool = "esearch.fcgi?db=protein&term=homo_sapiens[ORGN]+brca2[GENE]&idtype=acc&retmode=json".format(Species,GeneSymbols)
	#NPtool = "elink.fcgi?dbfrom=gene&db=protein&id=675&idtype=acc&retmode=text".format(NCBI_ID)	
	Proteins_response = requests.get(APIserver+NPtool, headers={ "Content-Type" : "application/json"})

	file.write("<td>")
	if Proteins_response.ok:
		list_ID = Proteins_response.json()["esearchresult"]["idlist"] 
		for proteinID in list_ID:
			if "P" in proteinID:
				Protein_url = "https://www.ncbi.nlm.nih.gov/protein/{}".format(proteinID)
				tagProtein_url = "<a class='list-group-item' href='{}'>{}</a>".format(Protein_url, proteinID)
				file.write(tagProtein_url)
	else : file.write("no protein data")
	file.write("</td>")

def kegg(NCBI_ID, file):

	
	#import requests, re

	# KEGG ID fetching
	KEGG_fetching_url = "http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(NCBI_ID)
	ID_request = requests.get(KEGG_fetching_url)
	KEGG_ID = ID_request.text.splitlines()[0].split("\t")[1]
	KEGG_ID_url = "https://www.genome.jp/dbget-bin/www_bget?{}".format(KEGG_ID)
	pathwayPrefix = KEGG_ID.split(":")[0]

	# Pathways fetching
	PATHWAYS_url = "http://rest.kegg.jp/get/{}".format(KEGG_ID)
	PATHWAYS_request = requests.get(PATHWAYS_url)
	PATHWAYS_list = re.findall("(hsa\d+\s{2}.*\n)",PATHWAYS_request.text)

	file.write("<td>")
	for PATHWAYS in PATHWAYS_list:
		PATHWAYS_ID = PATHWAYS.split("  ")[0]
		PATHWAYS_Name = PATHWAYS.split("  ")[1]
		PathwaysNetwork_url = "https://www.genome.jp/dbget-bin/get_linkdb?-t+pathway+{}+{}".format(PATHWAYS_ID, NCBI_ID)
		tagPathways_url = "<a class='list-group-item' href='{}'>{}</a>".format(PathwaysNetwork_url, PATHWAYS_Name)
		file.write(tagPathways_url)
	file.write("<a class='card-footer text-muted' href='{}'>{}</a>".format(KEGG_ID_url,KEGG_ID))
	file.write("</td>")

