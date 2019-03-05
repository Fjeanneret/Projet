#!/usr/bin/env python
#Construction du HTML dans le main
#file
from uniprotKB import *
from EnsemblEBI import *
from ncbiFunction import *
from refseq import *

#library
from requests import *
import time

#start
start = time.time()

startfile = open('start.html', 'r')
outputfile = open('projet_tableau.html', 'w')
outputfile.write(startfile.read())
startfile.close()

#body
file = open("gene1.txt", "r")
lines = file.readlines()
for line in lines:
    data = line[:-1].split("\t")
    organism = data[1]
    query = data[0]
    print(organism)

#GeneSymbol-----------------------------------------------------------------
    outputfile.write("<tr><td>{}</td>\n".format(query))
#Specie---------------------------------------------------------------------
    outputfile.write("<td>{}</td>\n".format(organism))
#ID&OfficialFullName--------------------------------------------------------
    IDNcbi, dictNcbi = functionNcbiIDName(organism, query)
    outputfile.write("<td>")
    for k, v in dictNcbi.items():
        outputfile.write('<a href="https://www.ncbi.nlm.nih.gov/gene/{k}">{k}:{v}</a><br/>'.format(k=k, v=v))
    outputfile.write("</td>\n")
#RefSeq_--------------------------------------------------------------------
    RefSeqTranscript = []
    RefSeqTranslation = []
    #Transcript-------------------------------------------------------------
    IDTranscriptRS = functionRefSeq(organism, query, "Nucleotide", "M", RefSeqTranscript)
    outputfile.write("<td>")
    for id in IDTranscriptRS:
        outputfile.write('<a href="https://www.ncbi.gov/nuccore/{i}">{i}</a><br/>'.format(i=id))
    outputfile.write("</td>\n")
    #Translation------------------------------------------------------------
    IDTranslationRS = functionRefSeq(organism, query, "Protein", "P", RefSeqTranslation)
    outputfile.write("<td>")
    for idprot in IDTranslationRS:
        outputfile.write('<a href="https://www.ncbi.gov/protein/{i}">{i}</a><br/>'.format(i=idprot))
    outputfile.write("</td>\n")
#KeggID---------------------------------------------------------------------
    IDKegg, prefixKegg = functionKeggID(IDNcbi)
    outputfile.write('<td><a href="https://www.genome.jp/dbget-bin/www_bget?{i}">{i}</a></td>\n'.format(i=IDKegg))
    print (IDKegg)
#KeggPathway----------------------------------------------------------------
    dictKeggPathway = functionKeggPathway(IDKegg, prefixKegg)
    outputfile.write("<td>")
    for k,v in dictKeggPathway.items():
        outputfile.write('<a href="www.genome.jp/kegg-bin/show_pathway?{k}">{k}:{v}</a><br/>\n'.format(k=k,v=v))
    outputfile.write("</td>\n")
#EnsemblID-----------------------------------------------------------------
    IDEnsembl, server, organism_clean = functionEnsemblID(organism, query)
    outputfile.write("<td>")
    for idens in IDEnsembl :
        outputfile.write('<a href="www.ensembl.org/{o}/Gene/Summary?db=core;g={i}">{i}</a><br/>'.format(o=organism_clean,i=idens))
    outputfile.write("</td>\n")
#Ensembl-------------------------------------------------------------------
    EnsemblTranscript = []
    EnsemblTranslation = []
    listIDtransc=[]
    listIDtransl=[]
    for id in IDEnsembl:
        ext = "/lookup/id/{}?expand=1".format(id)
        r = get(server + ext, headers={"Content-Type": "application/json"})
        if r.ok:
            decoded = r.json()
            #Transcript----------------------------------------------------
            IDTranscriptE = functionEnsembl(decoded, EnsemblTranscript, option="Transcript")
            for id in IDTranscriptE:
                listIDtransc.append(id)
            #Translation---------------------------------------------------
            IDTranslationE = functionEnsembl(decoded, EnsemblTranslation, option="Translation")
            for id in IDTranslationE:
                listIDtransl.append(id)

    listIDtransc_clean=list(set(listIDtransc)) #suppresion des doublons
    listIDtransl_clean=list(set(listIDtransl)) #suppression des doublons

    outputfile.write("<td>")
    for idt in listIDtransc_clean :
        outputfile.write('<a href="www.ensembl.org/{o}/Transcript/Summary?db=core;t={t}">{t}</a><br/>'.format(o=organism_clean,t=idt))
    outputfile.write("</td>\n")

    outputfile.write("<td>")
    for idp in listIDtransl_clean:
        outputfile.write('<a href="www.ensembl.org/{o}/Transcript/ProteinSummary?db=core;p={p}">{p}</a><br/>'.format(o=organism_clean,p= idp))
    outputfile.write("</td>\n")
    print("Querying End")
#ProteinID&Name(Uniprot)---------------------------------------------------
    IDUniprot,dictUniprot=functionUniprot(organism,query)
    outputfile.write("<td>")
    for k,v in dictUniprot.items():
        outputfile.write('<a href="www.uniprot.org/uniprot/{k}">{k}:{v}</a><br/>'.format(k=k, v=v))
    outputfile.write("</td>\n")
#GoTerm---------------------------------------------------------------------
    MF, CC, BP = functionGoTerm(IDUniprot)
    #BiologicalProcess------------------------------------------------------
    outputfile.write("<td>")
    for gobp in BP:
        outputfile.write('{}<br/>'.format(gobp))
    outputfile.write("</td>\n")
    #MolecularFunction------------------------------------------------------
    outputfile.write("<td>")
    for gomf in MF:
        outputfile.write('{}<br/>'.format(gomf))
    outputfile.write("</td>\n")
    #CellularComponent------------------------------------------------------
    outputfile.write("<td>")
    for gocc in CC:
        outputfile.write('{}<br/>'.format(gocc))
    outputfile.write("</td>\n")
#PDBID----------------------------------------------------------------------
    listPdb,listIDPdb=functionPDB(IDUniprot)
    outputfile.write("<td>")
    i=0
    for element in listPdb:
        outputfile.write('<a href="www.rcsb.org/structure/{i}">{e}</a><br/>'.format(i=listIDPdb[i],e=element))
        i+=1
    outputfile.write("</td>\n")
#String---------------------------------------------------------------------
    dictString = functionString(IDUniprot)
    outputfile.write("<td>")
    for k , v in dictString.items():
        outputfile.write('<a href="{}">{}:Network </a><br/>'.format(v , k))
    outputfile.write("</td>\n")

#PrositeID-------------------------------------------------------------------
    outputfile.write("<td>No data available yet</td>")
    GV=functionProsite(IDUniprot)
    print(GV)
#PfamID----------------------------------------------------------------------
    dictPfam=functionPFAM(IDUniprot)
    outputfile.write("<td>")
    for k , v in dictPfam.items():
        outputfile.write('<a href="pfam.xfam.org/protein/{k}">{k}:{v}</a><br/>'.format(k=k, v=v))
    outputfile.write("</td>\n")

#bottom
outputfile.write("</tr></tbody>\n</table>\n</body>\n</html>")

end=time.time()
print("time",(end-start)/60,"minutes")

outputfile.close()
file.close()