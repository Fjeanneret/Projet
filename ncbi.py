import requests, biopython

'''
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=nuccore&id=675&term=srcdb_refseq_known[prop]


https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=protein,nuccore&id=675&term=srcdb_refseq_known[prop] ????

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=nuccore&linkname=protein_nuccore_mrna&id=363743782

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=155030234&rettype=fasta&retmode=text


https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=NP_037367

'''


#avec espece et gene :

#
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=homo_sapiens[ORGN]+brca2[GENE]&idtype=acc&retmode=json

#avec id ncbi du gene : 
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=675&retmode=json
NG_012772.3

##### pr n acc nm

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term=homo_sapiens[ORGN]+brca2[GENE]&idtype=acc&retmode=json

###

#NP 

#
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gene&db=protein&id=675&idtype=acc&retmode=text