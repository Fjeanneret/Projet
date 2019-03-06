import requests


def interactionNetwork(UniprotID,file):
	print("qGO...")
	file.write("<td>")
	r = requests.get("https://string-db.org/api/image/network?identifiers={}".format(UniprotID))

	if not r.ok: 
		tag_String_url = "Pas de liens de reseau d'interactions String pour {}".format(UniprotID)

	else : 
		String_url = "https://string-db.org/api/image/network?identifiers={}".format(UniprotID)
		tag_String_url = """<iframe src='{}' scrolling="no" frameborder="0">
		</iframe><h3><a class='card-header' href={}>
		<i class='fa fa-search-plus  text-danger'></i>
		</a></h3><br>""".format(String_url, String_url)

	file.write(tag_String_url)
	file.write("</td>")

