import requests, re

def kegg(NCBI_ID, file):

	
	print("KEGG...")

	# KEGG ID fetching
	## API request
	KEGG_fetching_url = "http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(NCBI_ID)
	ID_request = requests.get(KEGG_fetching_url)
	## Data (text format) parsing
	KEGG_ID = ID_request.text.splitlines()[0].split("\t")[1]
	KEGG_ID_url = "https://www.genome.jp/dbget-bin/www_bget?{}".format(KEGG_ID)
	pathwayPrefix = KEGG_ID.split(":")[0]

	# Pathways fetching
	PATHWAYS_url = "http://rest.kegg.jp/get/{}".format(KEGG_ID)
	PATHWAYS_request = requests.get(PATHWAYS_url)
	PATHWAYS_list = re.findall("(hsa\d+\s{2}.*\n)",PATHWAYS_request.text)

	file.write("<td>")
	for PATHWAYS in PATHWAYS_list: # ID and Name for each line
		PATHWAYS_ID_Name = PATHWAYS.split("  ")
		PATHWAYS_ID = PATHWAYS_ID_Name[0]
		PATHWAYS_Name = PATHWAYS_ID_Name[1]

		# url, tag building and writing
		PathwaysNetwork_url = "https://www.genome.jp/dbget-bin/get_linkdb?-t+pathway+{}+{}".format(PATHWAYS_ID, NCBI_ID)
		tagPathways_url = "<a class='list-group-item' href='{}'>{}</a>".format(PathwaysNetwork_url, PATHWAYS_Name)
		file.write(tagPathways_url)
	file.write("<a class='card-footer text-muted' href='{}'>{}</a>".format(KEGG_ID_url,KEGG_ID))
	file.write("</td>")