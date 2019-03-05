import requests, re

def quick_go(Uniprot_id,go_aspect,output_file):
	"""
	Fonction : quick_go
	But : Récupérer les GO
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying QuickGo with aspect= ",go_aspect,"...\n")
	Go_name=[]
	i = 0
	if Uniprot_id != "No_data":
		i = 0
		requestURL = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&aspect={}".format(go_aspect)+"&geneProductId={}".format(Uniprot_id[0])
		r = requests.get(requestURL, headers={ "Accept" : "application/json"})
		decoded = r.json()
		if decoded["numberOfHits"] == 0:
			output_file.write("<td>No_data<br>\n</td>\n")
		else:
			while i < len(decoded["results"]):
				if i == 0:
					output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
				if decoded["results"][i]["goName"] not in Go_name: #On ne garde pas les doublons
					output_file.write(decoded["results"][i]["goName"]+"<br><br>\n")
					Go_name.append(decoded["results"][i]["goName"])
				if i == len(decoded["results"])-1:
					output_file.write("</div></td>\n")
				i = i + 1
	else:
		output_file.write("<td>No_data<br>\n</td>\n")
	return()
