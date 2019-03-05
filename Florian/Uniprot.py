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
	secondariesNames = []

	r = requests.get("""https://www.uniprot.org/uniprot/?query=organism:{}+gene_exact:{}&
	reviewed:yes&columns=id,protein%20names&format=tab""".format(Species,GeneSymbols))

	IDsAndProteinNames = r.text
	lines = IDsAndProteinNames.splitlines()
	firstLine = lines[1]
	IDAndNamesThenOnlyNames = firstLine.split("\t")
	#print(IDAndNamesThenOnlyNames)
	firstUniprotID = IDAndNamesThenOnlyNames.pop(0)
	proteinNames = IDAndNamesThenOnlyNames[0].split(" (")
	#print(IDAndNamesThenOnlyNames)
	mainName = proteinNames.pop(0)
	
	file.write("<td>")
	tag_UniprotID = "<a class='card-header' href='https://www.uniprot.org/uniprot/{}'>{}</a>".format(firstUniprotID, firstUniprotID)
	tag_UniprotName = "<span>{}</span>".format(mainName)
	bootstrap(tag_UniprotID, tag_UniprotName, file)
	#file.write(line)
	file.write("</td>")
	

	"""	i=0
	print("Nom secondaires : ")
	for i in range(0,len(proteinNames)):
		secondariesNames.append(proteinNames[i].replace(")",""))
		i+=1"""
	return firstUniprotID




