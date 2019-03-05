import requests, sys

def qGO(UniprotID, file, geneCount):

	bioProcess = []
	molFunction = []
	cellComponent = []

	requestURL = """https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&geneProductId={}""".format(UniprotID)
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})

	if not r.ok:
		print("aie qgo")
	else: 
		d = r.json()
	i=0
	#print(d)
	#print(d["results"])
	while i < len(d["results"]):
		goName = d["results"][i]["goName"]
		
		if d["results"][i]["goAspect"] == "biological_process":
			#a = d["results"][i]["goId"]
			if goName not in bioProcess:
				bioProcess.append(goName)
		elif d["results"][i]["goAspect"] == "molecular_function":
			if goName not in molFunction:
				molFunction.append(goName)	
		elif d["results"][i]["goAspect"] == "cellular_component":
			if goName not in cellComponent:
				cellComponent.append(goName)		

		i+=1
	print(bioProcess,molFunction,cellComponent)

	listAnnotations = [bioProcess, molFunction, cellComponent]
	elementCount = 0 + geneCount
	for annotation in listAnnotations:

		file.write("<td><ul class='list-group'>")
		if len(annotation)>1:

			first_element = annotation.pop(0)
			tag_go = """<p>
							<span  class='list-group-item text-muted bg-light#'>{}</span>
							<span class="btn btn-primary" type="button" data-toggle="collapse" data-target="#collapse{}" aria-expanded="false" aria-controls="collapse{}">
	    						<i class="fas fa-plus">  </i>  <span class='badge badge-light'>{}</span>
							</span></p>
					""".format(first_element, elementCount, elementCount, len(annotation))
			
			file.write(tag_go)
			file.write("<div class='collapse' id='collapse{}'>".format(elementCount))
			for element in annotation:
				tag_go = """
						
		 					
		    					<span  class='list-group-item text-muted bg-light#'>{}</span>
							""".format(element)

				#tag_go = """<span  class='list-group-item text-muted bg-light
				#'>{}</span>""".format(element)
				file.write(tag_go)
			elementCount +=1
			file.write("</div>")
		elif len(annotation)==1:
			file.write("<span  class='list-group-item text-muted bg-light#'>{}</span>".format(annotation[0]))
			elementCount +=1
		else : 
			elementCount +=1

		file.write("</ul></td>")