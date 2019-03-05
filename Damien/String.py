import requests

def string(Uniprot_id,output_file):
	"""
	Fonction : string
	But : Récupérer les intéractions protéiques sur String
	Méthode : requests.get
	Retourne : //
	"""
	print("Querying String...\n")
	output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">')
	for uni_id in Uniprot_id: 
		url = "https://string-db.org/api/highres_image/network?identifiers={}".format(uni_id)
		r = requests.get(url)
		if r.ok:
			output_file.write('<a href='+'"'+url+'">'+'Interaction map '+uni_id+'</a><br><br>')
	output_file.write("</div></td>\n")
	return()

