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
	protList=[]
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
		protList.append(lines[i].split(":")[0])
		i+=1
	print(protList)

	#pour chaque nom, si noms =/=, afficher liens Strings et de Structure




'''
brouillon

https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&columns=id,protein%20names&format=tab

url = "https://www.rcsb.org/pdb/rest/search"
data= """ 
<orgPdbQuery>

<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>

<description>Simple query for a list of Uniprot Accession IDs: P69905</description>

<accessionIdList>P69905</accessionIdList>

</orgPdbQuery>"""

header={"Content-Type":"Application/x-www-form-urlencoded"}

r = requests.post(url,data=data,headers=header)

print(r.text)

#pfam :

url = "https://pfam.xfam.org/family?id=brca2&output=xml"
#https://pfam.xfam.org/family/Piwi/acc

r = requests.get(url)

print(r.text)

#pfam structure url : https://pfam.xfam.org/structure/1NOW#tabview=tab1
'''
