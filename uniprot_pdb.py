import requests

#choix de prendre la premiere prot /!\, voir avec liste des prots ensembl ?
def proteinName_ID(Species,GeneSymbols):

	r = requests.get("https://www.uniprot.org/uniprot/?query=organism:{}+gene_exact:{}&reviewed:yes&columns=id,protein%20names&format=tab".format(Species,GeneSymbols))

	IDsAndProteinNames = r.text
	lines = IDsAndProteinNames.splitlines()
	firstLine = lines[1]
	IDAndNamesThenOnlyNames = firstLine.split("\t")
	#print(IDAndNamesThenOnlyNames)
	firstUniprotID = IDAndNamesThenOnlyNames.pop(0)
	proteinNames = IDAndNamesThenOnlyNames[0].split(" (")
	#print(IDAndNamesThenOnlyNames)
	mainName = proteinNames.pop(0)
	secondariesNames = []
	print("UniprotID : ", firstUniprotID)
	print("Nom principal : ", mainName,"\n")

	i=0
	print("Nom secondaires : ")
	for i in range(0,len(proteinNames)):
		secondariesNames.append(proteinNames[i].replace(")",""))
		print(secondariesNames[i])
		i+=1
	return firstUniprotID

def fromUniprotToPDB_ID(firstUniprotID):

	#r = requests.get("https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&columns=id&format=tab")

	url = "https://www.rcsb.org/pdb/rest/search"
	data= """ 
	<orgPdbQuery>
	<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
	<accessionIdList>{}</accessionIdList>
	</orgPdbQuery>""".format(firstUniprotID)

	r = requests.post(url, data=data ,headers={"Content-Type":"application/x-www-form-urlencoded"})

	wholeFileIDs = r.text
	lines = wholeFileIDs.splitlines()

	#gerer le "...:2" avec regex puis construction du lien
	i=0
	for i in range(0,len(lines)):
		a=lines[i].split(":")[0]
		#protList.append(a)
		
		#print(protList)

		r = requests.get("https://www.rcsb.org/pdb/rest/customReport.xml?pdbids={}&customReportColumns=structureTitle&service=wsfile&format=csv".format(a))
		
		
		i+=1
		wholeFile = r.text
		#print(wholeFile)
		linesFile = wholeFile.splitlines()
		if len(linesFile)>1: 
			PDBid_Name_Structure = linesFile[1]
			#print("\n",PDBid_Name_Structure)
			Name_Structure = PDBid_Name_Structure.split(",")[1]
			Structure = Name_Structure.split(" (").pop(0)
			print("Structure : ", Structure)

	#pour chaque nom, si noms =/=, afficher liens Strings et de Structure