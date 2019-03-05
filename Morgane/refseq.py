#!/usr/bin/env python
import requests
import re

def functionRefSeq(organism,query,database,option,list_id) :
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={}&term={}[Organism]+{}[Gene Name]&idtype=acc&retmode=json".format(database,organism,query)
    r=requests.get(url)
    if not r.ok :
        list_id+=["No Data Available"]
    else :
        decoded = r.json()
        result=repr(decoded["esearchresult"]["idlist"])
        list_id=re.findall("[NX]{}_\d+.\d".format(option),result)
    return(list_id)