import requests

def Prosite(UniprotID,file):
	'''
	Get protein families fetching Prosite database thanks to Uniprot ID and represent a protein 
	and its families in the html output file. 
	'''

	print("Prosite...")
	file.write("<td>")

	# API request
	prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}".format(UniprotID)
	r = requests.get(prosite_url + "&output=json")
	prosite_JSON_File = r.json()

	
	i=0
	while i < len(prosite_JSON_File["matchset"]):

		signature_ac = prosite_JSON_File["matchset"][i]["signature_ac"]
		signature_id = prosite_JSON_File["matchset"][i]["signature_id"]

		# url, tag building and writing
		Prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?{}".format(signature_ac)
		tag_Prosite_url = "<a href='{}' class='btn btn-danger rounded-pill'>{}</a>".format(Prosite_url,signature_id) # btn-danger = red button

		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>") # protein skeletton
		file.write(tag_Prosite_url) # protein family
		i+=1

	file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>") #protein end
	file.write("<a href='{}'>view</a>".format(prosite_url))
	file.write("</td>")