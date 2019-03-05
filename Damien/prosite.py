import requests

def prosite(Uniprot_id,output_file):
	"""
	Fonction : prosite
	But : Récupérer les motifs et domaines protéiques sur prosite
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying prosite...\n")
	requestURL="https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}&output=json".format(Uniprot_id[0])
	r = requests.get(requestURL)
	result = r.json()
	i = 0
	pro_id_list = []
	if result["n_match"] != 0: # On vérifie qu'il y a bien des résultats
		while i < len(result["matchset"]):
			prosite_id = result["matchset"][i]["signature_ac"]
			if i == 0:
				output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">')
			if prosite_id not in pro_id_list: # On ne prend pas les doublons
				pro_id_list.append(prosite_id)
				output_file.write('<a href="https://prosite.expasy.org/{}'.format(prosite_id)+'">'+prosite_id+'</a><br>\n')
				output_file.write('{}'.format(result["matchset"][i]["signature_id"])+'<br>')
				output_file.write('<a href="https://prosite.expasy.org/cgi-bin/prosite/PSView.cgi?ac={}&onebyarch=1&hscale=0.6'.format(prosite_id)+'">  '+"Graphical_view"+'</a><br><br>\n')
			if i == len(result["matchset"])-1:
				output_file.write('</div></td>')
			i = i + 1
	else:
		output_file.write('<td>No_data</td>')
	
	return()
