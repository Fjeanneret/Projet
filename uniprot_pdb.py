#prot ensembl 

#là faut prot id selon specie et genesymbol d'Uniprot : 

#avoir id uniprot avec espèce et genesymbol : 


import requests, sys

r = requests.get("https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&format=tab&colums=id")

a = r.content
#b = a.json()
print(a)

'''

r = requests.get("https://www.uniprot.org/uniprot/?query=organism:homo_sapiens+gene_exact:BRCA2&reviewed:yes&format=txt&colums=id")
#r.raise_for_status()
#sys.exit()
print(r)
decoded = r.json()
print(repr(decoded))
 



#pour avoir pdb acc avec uniprot acc : 

'from':'ACC',
'to':'P_REFSEQ_AC',
'format':'tab',
'query':'P13368 P20806 Q9UM73 P97793 Q17192'<<


'''
