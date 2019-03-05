import requests, re

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