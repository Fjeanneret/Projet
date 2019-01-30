#prot ensembl 

#là faut prot id selon specie et genesymbol d'Uniprot : 

#avoir id uniprot avec espèce et genesymbol : 


import requests, sys

#r = requests.get("https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&columns=id&format=tab")

url = "https://www.rcsb.org/pdb/rest/search"
data= """ 
<orgPdbQuery>

<queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>

<accessionIdList>P51587</accessionIdList>

</orgPdbQuery>"""

r = requests.post(url, data=data ,headers={"Content-Type":"application/x-www-form-urlencoded"})




wholeFileIDs = r.text
print(r.text)
lines = wholeFileIDs.splitlines()
#print(lines[2])
#FirstUniprotID = lines[1]
#print(FirstUniprotID)

#UniprotRefID = lineOne[O]

#print(UniprotRefID)


'''
https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&columns=id,protein%20names&format=tab

r = requests.get("https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&format=txt&colums=id")
#r.raise_for_status()
#sys.exit()
print(r)
decoded = r.json()
print(repr(decoded))
'''



#pour avoir pdb acc avec uniprot acc : 


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
'''
#pfam :

url = "https://pfam.xfam.org/family?id=brca2&output=xml"
#https://pfam.xfam.org/family/Piwi/acc

r = requests.get(url)

print(r.text)

#pfam structure url : https://pfam.xfam.org/structure/1NOW#tabview=tab1
'''
