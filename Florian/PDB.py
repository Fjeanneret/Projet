import requests

def PDB_Structure_Fetcher(PDB_ID,file):
	'''
	Get Structure ID with PDB ID
	'''

	r = requests.get("""https://www.rcsb.org/pdb/rest/customReport.xml?pdbids={}&customReportColumns=structureTitle&service=wsfile&format=csv""".format(PDB_ID))
	
	wholeFile = r.text 
	linesFile = wholeFile.splitlines()

	if len(linesFile)>1: 	#first lines is colonne names

		PDBid_Name_Structure = linesFile[1].split(",") 
		Name_Structure, Def_Structure = PDBid_Name_Structure[0], PDBid_Name_Structure[1]
		Structure_case = Name_Structure  + " : " + Def_Structure

		file.write(Structure_case)
		file.write("<br>\n")

	else : 
		file.write("Pas de Structure 3D disponible")
		file.write("<br>\n")

def PDB_ID(firstUniprotID,file):
	'''
	Convert Uniprot ID to PDB ID
	'''

	url = "https://www.rcsb.org/pdb/rest/search"
	data= """ 
	<orgPdbQuery>
	<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
	<accessionIdList>{}</accessionIdList>
	</orgPdbQuery>""".format(firstUniprotID) #xml query accept by search rest tool

	r = requests.post(url, data=data ,headers={"Content-Type":"application/x-www-form-urlencoded"})

	wholeFileIDs = r.text
	linesPDB_ID = wholeFileIDs.splitlines()

	file.write("<td>")
	
	PDB_ID = linesPDB_ID[0].split(":")[0] # format is "structure name : version", we take only name
	PDB_Structure_Fetcher(PDB_ID, file)

	file.write("</td>")

