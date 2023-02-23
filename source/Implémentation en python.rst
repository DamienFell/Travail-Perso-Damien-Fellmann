Implémentation en python
########################

Maintenant que les notions théoriques de la programmation par contraintes ont
été abordées, nous pouvons implémenter notre algorithme de résolution de sudoku 
en python.

Modélisation des variables et des contraintes
=============================================

Tout d'abord, nous allons modéliser les variables et les contraintes d'un PSC 
en créant leurs classes respectives.  

Premièrement, nous définissons la classe **Variable** : elle possède les attibuts *nom*, *domaine* et *valeur* (actuelle).
De plus, elle contient plusieurs méthodes : *metAJourValeur* met à jour la valeur de la variable, *nomEstEgal* vérifie
que le nom donné en paramètre est le même que celui de la variable et *__repr__* retourne le nom de la variable, sa 
valeur et son domaine dans une chaîne de caractère.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 4-8, 18-24, 31-33
    :linenos:
 
Deuxièmement, la classe **Contrainte** doit aussi être définie. Cependant, elle ne sera jamais directement utilisée
et sera héritée par les classes plus spécifiques **ContrainteUnaire** et **ContrainteBinaire**. Son unique attibut 
*variables* contient la liste des noms des variables sur lesquelles porte la contrainte. Sa méthode *dimension* retourne 
le nombre de variables sur lesquelles elle agit, *estValide* teste si la contrainte est respectée en choisissant la 
valeur *val* pour la vairable *val* et *__repr__* retourne la représentation sous format str de la contrainte.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 35-47
    :linenos:

Désormais, nous devons donc modéliser la classe fille **ContrainteUnaire** qui s'applique aux contraintes portant
sur une seule variable. La liste des variables ne contiendra donc que le nom de la variable impliquée dans la contrainte *refVar* prise en 
paramètre lors de l'instanciation. Cette classe contient également les attirbuts *op*, l'opérateur de la contrainte
(<,<=,>,>=,==,!=), la valeur de référence pour l'opérateur *ref*, et la variable *refVar*. Puis, on redéfinit les méthodes
de la classe **Contrainte** : *dimension* retourne logiquement 1 et *__repr__* retourne la variable impliquée,
l'opérateur et la valeur de référence. Pour la méthode *estValide*, on doit d'abord stocker la valeur actuelle de la variabe 
et la mettre à jour avec la valeur rentrée en paramètre. Ensuite, on teste cette valeur par rapport 
à l'opérateur et la valeur de référence. Finalement, il faut remettre à jour la valeur initiale de la variable.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 49-86
    :linenos:

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 88-139
    :linenos:


Algorithme de backtrack
=======================



Application à la résolution de sudokus
======================================
