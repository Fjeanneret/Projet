import requests, re

def Pfam(UniprotID,file):
	# http://pfam.xfam.org/protein/P51587?#proteinStructureBlock

	file.write("<td>")
	url = "http://pfam.xfam.org/protein/{}".format(UniprotID)
	r = requests.get(url + '?output=xml')
	Pfam_ACC = re.findall("PF[\d]{5}",r.text)
	Pfam_ID = re.findall(' id=".*"\s', r.text)

	if len(Pfam_ACC)==len(Pfam_ID):
		i=0
		cpt=1

		for i in range(0,len(Pfam_ACC)-1): 
			IDonly =  Pfam_ID[i].split("=")[1]
			PFAM_url = "http://pfam.xfam.org/family/{}".format(Pfam_ACC[i])

			if (Pfam_ID[i]==Pfam_ID[i+1]):
				cpt+=1

			else :
				if cpt > 2 :
					tag_PFAM_url = """"<a href='{}' class='btn btn-info rounded-pill'>
					{}<span class='badge badge-pill badge-light'>
					{}</span></a>""".format(PFAM_url,IDonly, cpt)
				
				else :
					tag_PFAM_url = "<a href='{}' class='btn btn-info rounded-pill'>{}</a>".format(PFAM_url,IDonly)
				
				cpt=0
				file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
				file.write(tag_PFAM_url)

		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
		file.write("<a href='{}' >view</a>".format(url))

	else : 
		file.write("problème d'extraction")

	file.write("</td>")