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

On implémente la classe **ContrainteBinaire** de manière semblable à la classe **ContrainteUnaire**. Cette fois, 
la liste des variables contiendra les noms des variable *refVar1* et *refVar2*. Les attributs sont ces deux variables ainsi
que l'opérateur *op* et la dimension de ces contraintes est de 2. Le fonctionnement des méthodes reste le même
à la différence que la valeur de référence *ref* est remplacée par la valeur de la variable *refVar2* dans la méthode
*estValide*.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 88-125
    :linenos:

A présent, il s'agit d'implémenter la classe **Variables** qui gère l'ensemble des variables présentes dans un 
problème de satisfaction de contraintes. Elle possède un seul attibut : la liste des variables, vides lors de 
l'instanciation. Afin de la remplir, on utilise la méthode *ajouteVar*. Puis, *retourneVar* permet de retourner 
une variable d'aprés son nom. La méthode *__repr__* quant à elle retourne une chaîne de caractères contenant toutes
les informations sur chaque variable.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 151-162, 173-178
    :linenos:

Comme pour les variables, on définit également une classe **Contraintes** qui s'occupe de l'ensemble des contraintes 
du PSC. Ses attributs *contraintes* et *contraintes_noms* contiennent toutes les contraintes et leur nom et sont 
également vide au départ. Lorsqu'une contrainte est ajoutée avec *ajouteContrainte*, on doit donc aussi rajouter 
son nom dans la liste *contraintes_noms*. Finalement, la méthode *__repr__* est semblable à celle de la classe 
**Variables**

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 180-187, 199-204
    :linenos:

Algorithme de backtrack
=======================

Aprés avoir défini ces quatre classes, nous pouvons implémenter l'algorithme de recherche en profondeur d'abord 
dans la fonction *backtrack*. D'abord, le premier paramètre *k* correspond à l'indice de la variable actuelle 
sur laquelle on teste les valeurs. Lorsqu'on teste les valeurs de la variable suivante, on rappelle la fonction
avec *k+1* en paramètre : cette fonction est donc récursive. Mais avant d'être rappelée, elle fait appel à la 
fonction *consistanceAvecVarsPrecedentes* qui est au coeur du fonctionnement de l'algorithme. Elle passe en revue 
toutes les contraintes portant sur la variable d'indice *k* et sur les variables d'indice plus petit que *k*
précédemment instanciées et teste si la combinaison des valeurs attribuées est consistante, c'est à dire si elle 
respecte ces contraintes. C'est donc seulement si toutes ces contraintes sont respectées qu'on peut passer à l'attribution
de la valeur de la variable d'indice *k+1*. Si le programme arrive à donner une valeur à la dernière variable
qui est consistante avec toutes les valeurs des autresvariables, cela signifie qu'on a trouvé une solution au problème et on 
retourne un dictionnaire contenant les noms des variables et leur valeur. Cependant, si aucune combinaison ne 
fonctionne, l'algorithme retourne "echec".

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 213-224, 227-237, 240-253
    :linenos:

Application à la résolution de sudokus
======================================

Afin de résoudre des sudokus à l'aide de l'algorithme de backtrack précédemment implémenté, nous
devons définir les variables, leurs domaines et les contraintes du problème. Les variables correspondent
aux cases vides des grilles de sudokus. Leur domaine est le même pour toutes et est les nombres entre 1 
et la taille de la grille (9 habituellement). Ce sont des contraintes d'inégalités qui définissent
les relations des variables entre elles et des variables avec les cases déjà numérotées : chaque case
d'une même ligne, d'une même colonne ou d'un même carré ne soit pas avoir la même valeur qu'une autre.

La fonction que nous allons développer prend en paramètre une grille sous forme de liste de listes sont 
les lignes de la grille, avec des "x" pour les valeurs inconnues, et retourne grille complétée sous ¨
le même format.

La première étape consiste alors à implémenter les fonctions *lignes*, *colonnes* et *carres* qui
retourne des listes de listes qui sont les lignes, colonnes ou carrés de la grille.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 271-293
    :linenos:

Ensuite, à partir de la grille de sudoku, on peut créer les variables pour chaque case contenant un 
"x". Leur nom est composé de l'indice *i* de la ligne et de l'indice *j* de la colonne d'où elles se 
trouvent dans la grille. En plus de créer ces variables et des les ajouter à la liste des variables 
(contenue dans une instanciation de la classe **Variables**), on remplace également les "x" de la grille
par les noms des variables.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 295-303
    :linenos:

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 305-322
    :linenos: