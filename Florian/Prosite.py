import requests

def Prosite(UniprotID,file):
	file.write("<td>")
	prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}".format(UniprotID)
	r = requests.get(prosite_url + "&output=json")
	decoded = r.json()

	liste=[]
	i=0
	while i < len(decoded["matchset"]):
		signature_ac = decoded["matchset"][i]["signature_ac"]
		signature_id = decoded["matchset"][i]["signature_id"]
		liste.append(signature_id)
		Prosite_url = "https://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?{}".format(signature_ac)
		tag_Prosite_url = "<a href='{}' class='btn btn-danger rounded-pill'>{}</a>".format(Prosite_url,signature_id)
		file.write("<br><span class='btn btn-light border border-light text-light rounded-0'>|</span><br>")
		file.write(tag_Prosite_url)
		i+=1
	file.write("<a href='{}'>view</a>".format(prosite_url))
	file.write("</td>")