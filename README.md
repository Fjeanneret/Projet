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


> L'interface graphique est développée en *python* à l'aide du module tkinter, module installé par défaut, comme tous ceux utilisés (voir paragraphe suivant).

**Aucune installation n'est donc requise pour faire fonctionner l'interface.**

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

Pour la capture d'écran voir le **GitHub**

### Modules utilisés

* tkinter
* requests
* re



## Tester le script

> Chacun des dossier des projets individuels contient son fichier test GeneSymbol.txt avec des tabulations comme séparateurs.


## Modifications possibles

* Ajouter la possibilité de choisir les annotations souhaitées dans l'interface avant le lancement. 

* Produire un fichier exécutable afin de fournir python et un code compilé dans un seul dossier.