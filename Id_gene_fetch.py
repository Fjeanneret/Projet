import requests, sys

GeneSymbols = []
Species=[]
<<<<<<< HEAD
Gene_ID=[]
'''
fichier = open("GeneSymbols.txt")
lignes = fichier.readlines()
print(lignes)'''
=======
ID_ENSG=[]
>>>>>>> 3dbfe018df2cb5ed285a648ab6469e885c902723

with open("GeneSymbols.txt") as f:
    lines = f.read().splitlines() 

for line in lines:
	line = line.replace(" ", "_") #penser a gerer l'espace a la fin du premier Homo_sapiens
	GeneSymbolAndSpecie =  line.split("\t")
	GeneSymbols.append(GeneSymbolAndSpecie[0])
	Species.append(GeneSymbolAndSpecie[1])
#print(GeneSymbols,Species)

i = 0

while i < 1:

	server = "https://rest.ensembl.org"
	#ext = "/xrefs/symbol/homo_sapiens/BRCA2?"
	ext = "/xrefs/symbol/{}/{}".format(Species[0],GeneSymbols[0])
	r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
	 
	if not r.ok:
		server = "https://rest.ensemblgenomes.org"
		ext = "/xrefs/symbol/{}/{}?".format(Species[i],GeneSymbols[i])
		r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
		
	  #r.raise_for_status()
	  #sys.exit()
	
	decoded = r.json()
	
	
	j=0
	while j<len(decoded):
		
		Gene_ID.append(decoded[j]["id"])
		j+=1
	i+=1
	
<<<<<<< HEAD
	
	
print(ID_ENSG)
''' 
/Homo_sapiens/gene/Summary?g=

lien genome browser avec l'id
www.ensembl.org/Homo_sapiens/Location/View?db=core;g=ENSG00000139618;


lien prot avec l'ENST (prot summary mais pas protein sequence :/

http://www.ensembl.org/Homo_sapiens/Transcript/ProteinSummary?
db=core;g=ENSG00000139618;r=13:32315474-32400266;t=ENST00000380152

orthologues :

voir si orthologue avec /homology puis afficher si ok : 

http://www.ensembl.org/Homo_sapiens/Gene/Compara_Ortholog?db=core;
g=ENSG00000012048;r=17:43044295-43170245

gerer si pas dans "core"

if if if avec requests.get() if not r.ok:

http://plants.ensembl.org/Arabidopsis_thaliana/Gene/Compara_Ortholog?
db=core;g=AT2G18790;r=2:8139756-8144461

prendre type en amont ?




<?xml version="1.0" encoding="UTF-8"?>
<!-- information on Pfam-A family PF02171 (Piwi), generated: 16:37:09 26-Oct-2009 -->
<pfam xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns="https://pfam.xfam.org/"
      xsi:schemaLocation="https://pfam.xfam.org/
                          https://pfam.xfam.org/static/documents/schemas/pfam_family.xsd"
      release="24.0"
      release_date="2009-10-07">
  <entry entry_type="Pfam-A" accession="PF02171" id="Piwi" />
</pfam>%

'''

=======
print(ID_ENSG)
>>>>>>> 3dbfe018df2cb5ed285a648ab6469e885c902723
