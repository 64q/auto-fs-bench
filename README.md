Projet « auto-fs-bench »
========================

---

Application de benchmark automatisé sur systèmes de fichier

## Installation

Dépendances python nécessaires à installer sur les clients :

* `python-argparse, python-psutil, python-matplotlib, python-pylab`

Dépendances python nécessaires à installer sur le serveur :

* `python-argparse`

Pour utiliser le logiciel, vous devez simplement cloner le dépôt `git clone https://github.com/KenTiN/auto-fs-bench.git`.

* Pour lancer le client `python client.py`
* Pour lancer le serveur `python server.py -s`

## Configuration

### Configuration de la plateforme

Pour configurer la plateforme, il faut éditer le fichier `conf/server.py`. Vous devrez alors renseigner la liste des clients de votre plateforme,
ainsi que d'autres informations documentées dans le fichier. N'oubliez pas de vérifier les chemins vers les scripts de benchmark ainsi que la
validité du répertoire de sauvegarde des données (le dossier doit exister !).

Le fichier `conf/client.py` permet lui de configurer le comportement du client.

### Configuration du test

Afin de déployer d'autres tests, vous pouvez être amené à créer un type de test bien particulier.

Pour créer un nouveau test, il faut copier le fichier d'exemple de config d'un test dans `config/tests/example.py`

Voici un exemple de configuration.

```python
# configuration du test de benchmark

# nom du test de benchmark (doit être identique au nom du fichier)
name = "simple"

# commentaire éventuel sur le test
comment = "Simple benchmark example"

# modules de test à lancer
modules = ["dd"]

# liste des clients cibles du test
clients = {
    "localhost": {"path": "/srv", "times": 1}
}

# spécifications sur le système de fichier testé
fs = {
    "name": "rozofs",
    "version": "0.1"
}

# fin de configuration du test
```

Il suffit donc de recopier ce squelette et de lancer ensuite la nouvelle configuration avec `run config`.

## Utilisation

Le serveur de tests permet de contrôler les clients lancés et de lancer des tests de benchmarks. Les résultats sont
ensuite directement rapatriés sur le serveurs et stockés dans une arborescence logique.

### Différents types de lancement

Vous pouvez lancer le serveur en mode interactif avec un sous-shell ou lancer directement un test.

* Pour lancer en mode interactif, entrez `python server.py -s`
* Pour lancer le test `test` directement, entrez `python server.py test`

### Liste des commandes du shell serveur

* `list clients` permet de lister les clients lancés sur la plateforme
* `test [test]` permet de tester si un test est valide et lançable
* `run [test]` permet de lancer un test de benchmark

## Développement

Pour développer dans les meilleures conditions, veuillez respecter les quelques
règles élémentaires détaillées ci-dessous.

* Les fichiers doivent être encodées en UTF-8 (sans BOM) ;
* Les tabulations doivent être composées de 4 espaces ;
* A chaque début de fichier source, il convient d'ajouter `#encoding: utf-8` afin
de garantir la bonne prise en charge de l'encodage.

Les fichiers de test de configuration devront être placés dans le dossier `tests/`
pour être ignoré par Git.

### Structure du projet

Le projet est découpé en modules pythons

    core/       -- contient les fichiers de base du projet
    config/     -- concentre l'essentiel de la configuration
        tests/  -- contient les fichiers de configuration des tests
    commands/   -- contient l'ensemble des commandes client/serveur
    modules/    -- contient les modules de benchmark lançables par la plateforme
    server.py   -- executable pour lancer le serveur
    client.py   -- executable pour lancer le client


## Auteurs

* Blin Olivier
* Lebourgeois Quentin

Pour nous contacter, veuillez nous envoyer un mail ou message directement sur Github.

Contact universitaire, <prenom.nom@etu.univ-nantes.fr>

## Licence

	auto-fs-bench, automated benchmark software.
    Copyright (C) 2013  O. Blin, Q. Lebourgeois

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
