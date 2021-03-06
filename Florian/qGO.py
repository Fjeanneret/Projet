import requests, sys

def qGO(UniprotID, file, collapseValue):
	"""
	Get biological process, molecular function and cellular component
	 Gene Ontology information
	"""

	print("qGO...")
	bioProcess = []
	molFunction = []
	cellComponent = []

	# API request
	requestURL = """https://www.ebi.ac.uk/QuickGO/services/annotation/
	search?includeFields=goName&geneProductId={}""".format(UniprotID) 
	r = requests.get(requestURL, headers={ "Accept" : "application/json"})

	if not r.ok:
		file.write("<td><ul class='list-group bg-warning'>Requete API GO - Echec</ul></td>")
	else: 
		annotationWholeFile = r.json()

	i=0
	while i < len(annotationWholeFile["results"]): # Iteration of each lines which could be one of 3 types
		goName = annotationWholeFile["results"][i]["goName"] # goName is annotation index for three types
		
		if annotationWholeFile["results"][i]["goAspect"] == "biological_process": 
			if goName not in bioProcess:
				bioProcess.append(goName) # add annotation in bioProcess list if line is about a biological process
		elif annotationWholeFile["results"][i]["goAspect"] == "molecular_function":
			if goName not in molFunction:
				molFunction.append(goName)	
		elif annotationWholeFile["results"][i]["goAspect"] == "cellular_component":
			if goName not in cellComponent:
				cellComponent.append(goName)		
		i+=1

	listAnnotations = [bioProcess, molFunction, cellComponent]
	for annotation in listAnnotations:
		file.write("<td><ul class='list-group'>") 

		if len(annotation)>1: # create a collapsable list if list lenght > 1

			first_element = annotation.pop(0) #Only the first element would be seen without expand action
			tag_go = """<p>
							<span  class='list-group-item text-muted bg-light#'>{}</span>
							<span class="btn btn-primary" type="button" data-toggle="collapse" data-target="#collapse{}" aria-expanded="false" aria-controls="collapse{}">
	    						<i class="fas fa-plus">  </i>  <span class='badge badge-light'>{}</span>
							</span></p>
					""".format(first_element, collapseValue, collapseValue, len(annotation)) #bootstrap 4 collapsing and font-awesome (fa) icon
			
			file.write(tag_go)

			# Hidden part before expand action
			file.write("<div class='collapse' id='collapse{}'>".format(collapseValue))
			for element in annotation: # We create a list with elements remaining in
				tag_go = """
		    					<span  class='list-group-item text-muted bg-light#'>{}</span>
							""".format(element)
				file.write(tag_go)

			collapseValue +=1 # We have to get a collapseValue different between each case of collapsing
			file.write("</div>")

		elif len(annotation)==1:
			file.write("<span  class='list-group-item text-muted bg-light#'>{}</span>".format(annotation[0]))
			collapseValue +=1

		else : 
			file.write("Pas d'annotations de GO")
			collapseValue +=1

		file.write("</ul></td>")