#!/usr/bin/env python
import requests
import sys
import re

def functionEnsemblID(organism,query):
    print("Querying Ensembl ...")
    organism_clean=organism.rstrip() #enleve l'espace à la fin de la ligne
    server = "https://rest.ensembl.org"
    ext = "/xrefs/symbol/{}/{}?".format(organism_clean, query)
    r= requests.get(server+ext, headers={"Content-Type": "application/json"})
    EnsemblID=[]
    if not r.ok:   #test si l'organisme est un vegetaux
        server = "https://rest.ensemblgenomes.org"
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
    decoded = r.json()
    id=repr(decoded[0]["id"])
    id_clean=re.sub("'","",id) #enleve les guillemets
    EnsemblID.append(id_clean)
    if len(decoded) != 1 :
        id2=repr(decoded[1]["id"])
        id2_clean=re.sub("'","",id2)
        EnsemblID.append(id2_clean)
    return (EnsemblID,server,organism_clean)

def functionEnsembl(decoded, list, option) :
    i=0
    while i<len(decoded["Transcript"]):
        if decoded["Transcript"][i]["biotype"]=="protein_coding":
            if option == "Transcript" :
                TranscriptID=repr(decoded["{}".format(option)][i]["id"])
                TranscriptID_clean=re.sub("'","",TranscriptID)
                list.append(TranscriptID_clean)
            else :
                TranslateID=repr(decoded["Transcript"][i]["{}".format(option)]["id"])
                TranslateID_clean=re.sub("'","",TranslateID)
                list.append(TranslateID_clean)
        i+=1
    return(list)

