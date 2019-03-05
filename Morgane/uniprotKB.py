#!/usr/bin/env python
import requests
import re

# ---Uniprot---
def functionUniprot(organism,query):
    print ("Querying Uniprot ...")
    r=requests.get("""https://www.uniprot.org/uniprot/?query=organism:{}+gene_exact:{}+fragment:no&sort=score&
    columns=id,entry name,protein_names,genes,organism,database(PDB)&format=tab""".format(organism,query))
    result1=r.text
    result2=result1.split("\n")
    del result2[0]
    del result2[-1]
    IDUniprot=[]
    Dict={}
    for element in result2 :
        result3=element.split("\t")
        ID=result3[0]
        IDUniprot.append(ID) #liste avec les ID
        ProtName=re.sub('(\((.*)\))','',result3[3])
        Dict[ID]=ProtName #Dictionnaire:clé=ID&valeur=Protname
    while '' in IDUniprot :
        IDUniprot.remove('')
    print ("Querying End")

    return(IDUniprot,Dict)
# ---String---
def functionString(IDUniprot):
    """Crée un dictionnaire avec en clé les id uniprot et en valeur l'url string correspondant."""
    print ("Querying String ...")
    Dict={}
    for id in IDUniprot :
        url="https://string-db.org/api/image/network?identifiers={}".format(id)
        #test de l'url :
        if requests.get(url).status_code==200 :
            Dict[id]=url
    print ("Querying End")
    return (Dict)
# ---PDB---
def functionPDB(IDUniprot):
    print("Querying PDB ...")
    list_pdb = []
    url = 'http://www.rcsb.org/pdb/rest/search'
    query_text = """
    <orgPdbQuery>
    <queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
    <accessionIdList>"""+ IDUniprot[0] +"""</accessionIdList>
    </orgPdbQuery>
    """
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url, data=query_text, headers=header)
    if r.text == "null\n":
        list_pdb+="No Data Available"
        list_idpdb="No Data Available"
    else :
        list_idpdb=re.sub("\n",",",r.text[0:-1])
        list_idpdb=re.sub(":\d","",list_idpdb)
        ext = "http://www.rcsb.org/pdb/rest/customReport.xml?pdbids="+ list_idpdb + "&customReportColumns=structureTitle&Service=wsfile&format=csv"
        response = requests.get(ext)
        structure_pdb=response.text.splitlines()
        for pdb in structure_pdb[1:]:
            namepdb_clean=re.sub('"','',pdb)
            namepdb_clean=re.sub(",",":",namepdb_clean)
            list_pdb.append(namepdb_clean)

    print("Querying End")
    return (list_pdb,list_idpdb)
# ---PFAM---
def functionPFAM(IDUniprot):
    print("Querying pfam ...")
    Dict={}
    for id in IDUniprot :
        url = "https://pfam.xfam.org/protein/{}?output=xml".format(id)
        xml = """
        <?xml version='1.0' encoding='utf-8'?>
        """
        headers = {'Content-Type': 'application/xml'}

        r=requests.get(url,data=xml,headers=headers)
        if r.ok:
            acc = re.findall("<match accession=\"(.*)\" type",r.text)
        if acc :    #test si liste vide
            for element in acc :
                element_clean=re.sub('" id="',"\t",element)
                element_split=element_clean.split("\t")
                Dict[element_split[0]]=element_split[1]
    print ("Querying End")
    return (Dict)
# ---GO---
def functionGoTerm(IDUniprot):
    print("Querying GO ...")
    molecularFunction=[]
    biologicalProcess=[]
    cellularComponent=[]
    for id in IDUniprot :
        url = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&geneProductId={}".format(id)
        headers = {'Content-Type': 'application/json'}
        r=requests.get(url,headers=headers)
        if r.ok:
            decoded=r.json()
            numberResult=0
            while numberResult < len(decoded["results"]) :
                if str(decoded["results"][numberResult]["goAspect"]) == "molecular_function" :
                    molecularFunction.append(decoded["results"][numberResult]["goName"])
                elif decoded["results"][numberResult]["goAspect"] == "biological_process" :
                    biologicalProcess.append(decoded["results"][numberResult]["goName"])
                elif decoded["results"][numberResult]["goAspect"] == "cellular_component" :
                    cellularComponent.append(decoded["results"][numberResult]["goName"])
                numberResult+=1
    #Suppression des doublons
    molecularFunction_clean=list(set(molecularFunction))
    cellularComponent_clean=list(set(cellularComponent))
    biologicalProcess_clean=list(set(biologicalProcess))
    print("Querying End")
    return(molecularFunction_clean,cellularComponent_clean,biologicalProcess_clean)
# ---Prosite---
def functionProsite(IDUniprot):
    listLinkProsite=[]
    for id in IDUniprot:
        url='https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}'.format(id)
        r=requests.get(url)
        if r.ok:
            result=r.text
            link=re.findall("<a href=\"(.*)\">Graphical view</a>", result)
            listLinkProsite.append(link)
        return (listLinkProsite)

