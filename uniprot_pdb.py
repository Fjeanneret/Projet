import requests, re

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
	
	print("UniprotID : ", firstUniprotID)
	print("Nom principal : ", mainName,"\n")
	file.write("<td>")
	line = firstUniprotID + ' : ' + mainName
	file.write(line)
	file.write("</td>")
	

	i=0
	print("Nom secondaires : ")
	for i in range(0,len(proteinNames)):
		secondariesNames.append(proteinNames[i].replace(")",""))
		print(secondariesNames[i])
		i+=1
	return firstUniprotID

def PDB_Structure_Fetcher(PDB_ID,file):
	r = requests.get("""https://www.rcsb.org/pdb/rest/customReport.xml?pdbids={}
		&customReportColumns=structureTitle&service=wsfile&format=csv""".format(PDB_ID))
	
	wholeFile = r.text
	linesFile = wholeFile.splitlines()

	if len(linesFile)>1: 
		PDBid_Name_Structure = linesFile[1].split(",")

		Name_Structure,Def_Structure = PDBid_Name_Structure[0],PDBid_Name_Structure[1]
		Structure_case = Name_Structure  + " : " + Def_Structure

		print(Structure_case)
		file.write(Structure_case)
		file.write("<br>\n")
	else : 
		print("pas de Structure 3D disponible")
		file.write("Pas de Structure 3D disponible")
		file.write("<br>\n")

def interactionNetwork(UniprotID,file):
	file.write("<td>")
	r = requests.get("https://string-db.org/api/image/network?identifiers={}".format(UniprotID))

	if not r.ok: 
		tag_String_url = "Pas de liens de reseau d'interactions String pour {}".format(UniprotID)
	else : 
		String_url = "https://string-db.org/api/image/network?identifiers={}".format(UniprotID)
		tag_String_url = "<h3><a class='card-header' href={}><i class='fa fa-bezier-curve text-danger'></i></a></h3><br>".format(String_url,UniprotID)
	print("String : ", tag_String_url)
	file.write(tag_String_url)
	file.write("</td>")


def fromUniprotToPDB_ID(firstUniprotID,file):
	#r = requests.get("https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&columns=id&format=tab")

	url = "https://www.rcsb.org/pdb/rest/search"
	data= """ 
	<orgPdbQuery>
	<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
	<accessionIdList>{}</accessionIdList>
	</orgPdbQuery>""".format(firstUniprotID)

	r = requests.post(url, data=data ,headers={"Content-Type":"application/x-www-form-urlencoded"})

	wholeFileIDs = r.text
	linesPDB_ID = wholeFileIDs.splitlines()

	file.write("<td>")
	"""i=0
	print(linesPDB_ID)
	for i in range(0,len(linesPDB_ID)): #4our:1 et :2, prendre que le premier ? 
		PDB_ID=linesPDB_ID[i].split(":")[0]
		PDB_Structure_Fetcher(PDB_ID, file)"""
	PDB_ID=linesPDB_ID[0].split(":")[0]
	PDB_Structure_Fetcher(PDB_ID, file)

	file.write("</td>")

def PfamFetcher(UniprotID,file):
	# http://pfam.xfam.org/protein/P51587?#proteinStructureBlock

	file.write("<td>")

	url = "http://pfam.xfam.org/protein/{}?output=xml".format(UniprotID)
	r = requests.get(url)

	Pfam_ACC = re.findall("PF[\d]{5}",r.text)
	Pfam_ID = re.findall(' id=".*"\s', r.text)
	print(Pfam_ACC,Pfam_ID)
	if len(Pfam_ACC)==len(Pfam_ID):
		i=0
		for i in range(0,len(Pfam_ACC)): 
			print(Pfam_ID[i],":", Pfam_ACC[i])
			test =  Pfam_ID[i].split("=")[1]
			#url a faire 
			PFAM_url = "http://pfam.xfam.org/family/{}".format(Pfam_ACC[i])
			tag_PFAM_url = "<a href='{}' class='btn btn-info rounded-pill'>{}</a>".format(PFAM_url,test)
			file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
			file.write(tag_PFAM_url)
		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
	else : print("problème d'extraction")

	file.write("</td>")

def PrositeFetcher(UniprotID,file):
	#voir pour créer graphical view https://prosite.expasy.org/mydomains/
	#lien de base https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq=P11087
	file.write("<td>")
	url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}&output=json".format(UniprotID)
	r = requests.get(url)
	decoded = r.json()

	i=0
	while i < len(decoded["matchset"]):
		print(decoded["matchset"][i]["signature_ac"])
		print(decoded["matchset"][i]["signature_id"])
		signature_ac = decoded["matchset"][i]["signature_ac"]
		signature_id = decoded["matchset"][i]["signature_id"]
		Prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?{}".format(signature_ac)
		tag_Prosite_url = "<a href='{}' class='btn btn-danger rounded-pill'>{}</a>".format(Prosite_url,signature_id)
		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
		file.write(tag_Prosite_url)
		i+=1
	file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
		
	file.write("</td>")