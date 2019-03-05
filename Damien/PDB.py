import requests, re

def pdb(Uniprot_id,output_file):
	"""
	Fonction : pdb
	But : Récupérer l'id de la structure 3D de la protéine ainsi que sa description
	Méthode : requests.post et requests.get
	Retourne : //
	"""
	print("Querying PDB...\n")
	results=[]
	url = 'http://www.rcsb.org/pdb/rest/search'
	if Uniprot_id != "No_data":
		Uniprot_liste_id = ",".join(Uniprot_id) #On joint les id Uniprot d'un GeneSymbol dans un string
		queryText = """
<?xml version="1.0" encoding="UTF-8"?>

<orgPdbQuery>

<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>

<accessionIdList>"""+Uniprot_liste_id+ """</accessionIdList>

</orgPdbQuery>

"""
		header={'Content-Type':'Application/x-www-form-urlencoded'}
		r = requests.post(url, data=queryText,headers=header)
		results_int = r.text.rstrip('\n')
		results_int = re.sub("(:\d)","",results_int) #On retire le :"chiffre" en fin d'id
		results = results_int.split('\n') #On stock les id dans la liste results
		i = 0
		# Pour chaque id dans la liste on génère le lien url de la structure 3D protéique
		while i < len(results):
			if i == 0:
				output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
			if results[i] != "null":
				output_file.write("<a href="+'"'+"http://www.rcsb.org/structure/{}".format(results[i])+'"'+">"+results[i]+"</a>"+"<br>\n")
			if results[i] == "null":
				output_file.write("No_data<br>\n")
			if i == len(results)-1:
				output_file.write("</div></td>\n")
			i = i + 1
		j = 0
		# Pour chaque id dans la liste on récupère la description de la strucutre 3D
		while j < len(results):
			url_desc = "http://www.rcsb.org/pdb/rest/customReport.xml?pdbids={}".format(results[j])+"&customReportColumns=structureId,structureTitle" 
			header = {'Content-Type':'Application/x-www-form-urlencoded'}
			results_desc = requests.get(url_desc,headers=header)
			if j == 0:
				output_file.write('<td><div style="max-height:300px;width:auto;overflow-x:auto">\n')
			if results[j] != "null":
				re_inter = results_desc.text.split('\n')
				struct_desc = re.sub("(<dimStructure.structureTitle>)|(</dimStructure.structureTitle>)","",re_inter[4])
				output_file.write(re_inter[4]+"<br>\n<br>\n")
			if results[j] == "null":
				output_file.write("No_data<br>\n")
			if j == len(results)-1:
				output_file.write("</div></td>\n")
			j = j + 1
	else:
		output_file.write("<td>Pas d'id Uniprot</td>\n")
	return()
