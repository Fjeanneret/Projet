# Projet M1 S2

## Projet d'extraction et d'organisation d'annonations à partir d'un gene et de l'espèce concernée.

Les bases de données impliquées sont :

	- Ensembl ; 
	- NCBI ;
	- Refseq
	- Uniprot ;
	- PDB ;
	- GO ;
	- KEGG ;
	- Pfam ;
	- Prosite ; 
	- String.	

## Vue d'ensemble

L'intégralité du projet est codé en python

Le fichier *interface_test.py* permet de lancer et de tester le script par le biais d'une interface graphique.

```
L'interface graphique est développée en *python* à l'aide du module tkinter, module installé par défaut, comme tous ceux utilisés (voir paragraphe suivant).

**Aucune installation n'est donc requise pour faire fonctionner l'interface.**
```
## Avantage

Le choix de l'interface permet une grande portabilité, sur tous les sytèmes d'exploitation et permet de fournir une solution d'extraction d'annotations rapides, simple, et facilement modifiable. 

### Organisation du script

Pour un schéma global voir le **GitHub** : [Fjeanneret/projet](https://github.com/Fjeanneret/Projet)
 
```
L'interface propose 3 scripts principaux différents. lançant le projet de la personne concernée. 
```

* Les boutons Parcourir et Envoyer sont disponibles dès l'ouverture.
* Les boutons Afficher et Sauvegarder apparaissent à la fin du script.

### Etat de la progression

Deux manières différentes d'observer la progression du script sont possibles avec la sortie standard ou l'interface.

> Pour la capture d'écran voir le **GitHub**

### Modules utilisés

* tkinter
* requests
* re



## Tester le script

Chacun des dossier des projets individuels contient son fichier test GeneSymbol.txt avec des tabulations comme séparateurs.


## Modifications possibles

* Ajouter la possibilité de choisir les annotations souhaitées dans l'interface avant le lancement. 

* Produire un fichier exécutable afin de fournir python et un code compilé dans un seul dossier.

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

