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

def PDB_Structure_Fetcher(PDB_ID,file):
	r = requests.get("""https://www.rcsb.org/pdb/rest/customReport.xml?pdbids={}
		&customReportColumns=structureTitle&service=wsfile&format=csv""".format(PDB_ID))
	
	wholeFile = r.text
	linesFile = wholeFile.splitlines()

	if len(linesFile)>1: 
		PDBid_Name_Structure = linesFile[1].split(",")

		Name_Structure,Def_Structure = PDBid_Name_Structure[0],PDBid_Name_Structure[1]
		Structure_case = Name_Structure  + " : " + Def_Structure

		file.write(Structure_case)
		file.write("<br>\n")
	else : 
		file.write("Pas de Structure 3D disponible")
		file.write("<br>\n")

def interactionNetwork(UniprotID,file):
	file.write("<td>")
	r = requests.get("https://string-db.org/api/image/network?identifiers={}".format(UniprotID))

	if not r.ok: 
		tag_String_url = "Pas de liens de reseau d'interactions String pour {}".format(UniprotID)
	else : 
		String_url = "https://string-db.org/api/image/network?identifiers={}".format(UniprotID)
		tag_String_url = """<iframe src='{}' height='30%' width='80%' scrolling="no" frameborder="0"></iframe><h3><a class='card-header' href={}><i class='fa fa-search-plus  text-danger'></i></a></h3><br>
		""".format(String_url, String_url)
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
	PDB_ID = linesPDB_ID[0].split(":")[0]
	PDB_Structure_Fetcher(PDB_ID, file)

	file.write("</td>")

def PfamFetcher(UniprotID,file):
	# http://pfam.xfam.org/protein/P51587?#proteinStructureBlock

	file.write("<td>")

	url = "http://pfam.xfam.org/protein/{}".format(UniprotID)
	r = requests.get(url + '?output=xml')

	Pfam_ACC = re.findall("PF[\d]{5}",r.text)
	Pfam_ID = re.findall(' id=".*"\s', r.text)
	if len(Pfam_ACC)==len(Pfam_ID):
		i=0
		cpt=1
		for i in range(0,len(Pfam_ACC)-1): 
			IDonly =  Pfam_ID[i].split("=")[1]
			PFAM_url = "http://pfam.xfam.org/family/{}".format(Pfam_ACC[i])
			if (Pfam_ID[i]==Pfam_ID[i+1]):
				cpt+=1
			else :

				if cpt > 2 :
					tag_PFAM_url = "<a href='{}' class='btn btn-info rounded-pill'>{}<span class='badge badge-pill badge-light'>{}</span></a>".format(PFAM_url,IDonly, cpt)
				else :
					tag_PFAM_url = "<a href='{}' class='btn btn-info rounded-pill'>{}</a>".format(PFAM_url,IDonly)
				cpt=0
				file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
				file.write(tag_PFAM_url)
		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
		file.write("<a href='{}' >view</a>".format(url))
	else : file.write("problème d'extraction")

	file.write("</td>")

def PrositeFetcher(UniprotID,file):
	#voir pour créer graphical view https://prosite.expasy.org/mydomains/
	#lien de base https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq=P11087
	file.write("<td>")
	prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}".format(UniprotID)
	r = requests.get(prosite_url + "&output=json")
	decoded = r.json()

	liste=[]
	i=0
	while i < len(decoded["matchset"]):
		signature_ac = decoded["matchset"][i]["signature_ac"]
		signature_id = decoded["matchset"][i]["signature_id"]
		liste.append(signature_id)
		Prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?{}".format(signature_ac)
		tag_Prosite_url = "<a href='{}' class='btn btn-danger rounded-pill'>{}</a>".format(Prosite_url,signature_id)
		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
		file.write(tag_Prosite_url)
		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
		i+=1
	file.write("<a href='{}'>view</a>".format(prosite_url))
	file.write("</td>")

def quickGO(UniprotID, file, geneCount):
	import requests, sys

	bioProcess = []
	molFunction = []
	cellComponent = []

	requestURL = """https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&geneProductId={}""".format(UniprotID)
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})

	if not r.ok:
		print("aie qgo")
	else: 
		d = r.json()
	i=0
	#print(d)
	#print(d["results"])
	while i < len(d["results"]):
		goName = d["results"][i]["goName"]
		
		if d["results"][i]["goAspect"] == "biological_process":
			#a = d["results"][i]["goId"]
			if goName not in bioProcess:
				bioProcess.append(goName)
		elif d["results"][i]["goAspect"] == "molecular_function":
			if goName not in molFunction:
				molFunction.append(goName)	
		elif d["results"][i]["goAspect"] == "cellular_component":
			if goName not in cellComponent:
				cellComponent.append(goName)		

		i+=1
	print(bioProcess,molFunction,cellComponent)

	listAnnotations = [bioProcess, molFunction, cellComponent]
	elementCount = 0 + geneCount
	for annotation in listAnnotations:

		file.write("<td><ul class='list-group'>")
		if len(annotation)>1:

			first_element = annotation.pop(0)
			tag_go = """<p>
							<span  class='list-group-item text-muted bg-light#'>{}</span>
							<span class="btn btn-primary" type="button" data-toggle="collapse" data-target="#collapse{}" aria-expanded="false" aria-controls="collapse{}">
	    						<i class="fas fa-plus">  </i>  <span class='badge badge-light'>{}</span>
							</span></p>
					""".format(first_element, elementCount, elementCount, len(annotation))
			
			file.write(tag_go)
			file.write("<div class='collapse' id='collapse{}'>".format(elementCount))
			for element in annotation:
				tag_go = """
						
		 					
		    					<span  class='list-group-item text-muted bg-light#'>{}</span>
							""".format(element)

				#tag_go = """<span  class='list-group-item text-muted bg-light
				#'>{}</span>""".format(element)
				file.write(tag_go)
			elementCount +=1
			file.write("</div>")
		elif len(annotation)==1:
			file.write("<span  class='list-group-item text-muted bg-light#'>{}</span>".format(annotation[0]))
			elementCount +=1
		else : 
			elementCount +=1

		file.write("</ul></td>")