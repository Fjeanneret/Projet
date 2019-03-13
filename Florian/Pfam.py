import requests, re

def Pfam(UniprotID,file):
	'''
	Get protein families fetching Pfam database thanks to Uniprot ID and represent a protein 
	and its families in the html output file.
	'''
	print("Pfam...")
	file.write("<td>")

	# API request
	url = "http://pfam.xfam.org/protein/{}".format(UniprotID)
	r = requests.get(url + '?output=xml')

	# Pfam accession and ID fetching
	Pfam_ACC = re.findall("PF[\d]{5}",r.text)
	Pfam_ID = re.findall(' id=".*"\s', r.text)

	if len(Pfam_ACC)==len(Pfam_ID): # check if we have accession and ID same number
		i=0
		cpt=1

		## ALgoritmh to collapse in one button numerous and followed same family proteins
		## a btn-info represents a family and a btn-light a piece of the protein without family
		## Each button have a link to see the family in pfam website 
		for i in range(0,len(Pfam_ACC)-1): 
			IDonly =  Pfam_ID[i].split("=")[1]
			PFAM_url = "http://pfam.xfam.org/family/{}".format(Pfam_ACC[i])

			if (Pfam_ID[i]==Pfam_ID[i+1]): # Check if 2 families are the same
				cpt+=1 #in this case count + 1

			else : # When the next don't the same we looking for number of repetitions
				if cpt > 2 : # Collapsing, badge enable to see number of repetitions
					tag_PFAM_url = """<a href='{}' class='btn btn-info rounded-pill'>
					{}<span class='badge badge-pill badge-light'>
					{}</span></a>""".format(PFAM_url,IDonly, cpt)
				
				else : # Just write the button
					tag_PFAM_url = "<a href='{}' class='btn btn-info rounded-pill'>{}</a>".format(PFAM_url,IDonly)
				
				cpt=0
				file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
				file.write(tag_PFAM_url)

		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>") #end of protein
		file.write("<a href='{}' >view</a>".format(url)) # Link of protein card on pfam website

	else : 
		file.write("problème d'extraction")

	file.write("</td>")