#!/usr/bin/env python
import requests
import re

def functionNcbiIDName(organism,query) :
    print("Querying NCBI ...")
    Dict={}

    r = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term={}[Gene Name]+AND+{}[Organism]&format=json".format(
            query, organism))

    if r.ok:
        decoded = r.json()
        list_id = decoded["esearchresult"]["idlist"]
        for id in list_id :
            r2 = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id={}&retmode=json".format(id))
            if r2.ok :
                decoded2 = r2.json()
                officialFullName = repr(decoded2["result"]["{}".format(id)]["description"])
                officialFullName_clean = re.sub("'", "", officialFullName)
                Dict[id]=officialFullName_clean
    print("Querying End")
    return(list_id,Dict)

def functionKeggID(list_id):
    print("Querying Kegg ...")
    r=requests.get("http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(list_id[0]))
    if r.ok:
        result = r.text.rstrip() #rsprip : enlève caractères de fin de lignes (ici espaces)
        result_split = result.split("\t")
        keggID = str(result_split[1::2]) #[startAt:endBefore:skip]
        keggID_clean = re.sub("[\[\'][\'\]]", "", keggID)
        prefixKegg = re.sub("\:.+","",keggID_clean)
    return (keggID_clean,prefixKegg)

def functionKeggPathway(keggID,prefixKegg):
    r= requests.get("https://www.genome.jp/dbget-bin/get_linkdb?-t+pathway+{}".format(keggID))
    Dict={}
    if r.ok:
        listIDName = re.findall("{}\d.+".format(prefixKegg), r.text)
        for element in listIDName:
            #recuperation des voies metaboliques
            #parsing html
            line = re.sub("\+.+</a>", "", element)
            line_clean = re.sub("\s{2,}", "\t", line)
            list_temporary = re.split("\t",line_clean)
            keggPathway=list_temporary[1]
            IDPathway=list_temporary[0]
            Dict[IDPathway]=keggPathway
    print("Querying End")
    return(Dict)

