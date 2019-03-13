import requests, re

def bootstrap(title,content,file):
	"""
	Add bootstrap element to enhance form and write 
	in table file
	"""

	case = """<div class="card text-center">
				{}
			<br>
			<div class="card-body">
				{}
			</div>
		</div><br>""".format(title, content)

	file.write(case)

def proteinName_ID(Species,GeneSymbols,file):
	"""
	Get first PDB ID of protein with Gene Symbol and Specie
	"""

	print("Uniprot...")

	# API request for Uniprot ID 
	r = requests.get("""https://www.uniprot.org/uniprot/?query=organism:{}+gene_exact:{}&
	reviewed:yes&columns=id,protein%20names&format=tab""".format(Species,GeneSymbols))

	IDsAndProteinNames = r.text

	# Parsing to fetch name and ID
	lines = IDsAndProteinNames.splitlines()
	
	firstLine = lines[1]
	IDAndNamesThenOnlyNames = firstLine.split("\t")
	firstUniprotID = IDAndNamesThenOnlyNames.pop(0)
	proteinNames = IDAndNamesThenOnlyNames[0].split(" (")
	mainName = proteinNames.pop(0)
	
	file.write("<td>")

	# url building and writing
	tag_UniprotID = "<a class='card-header' href='https://www.uniprot.org/uniprot/{}'>{}</a>".format(firstUniprotID, firstUniprotID)
	tag_UniprotName = "<span>{}</span>".format(mainName)
	bootstrap(tag_UniprotID, tag_UniprotName, file)
	
	file.write("</td>")

	return firstUniprotID




