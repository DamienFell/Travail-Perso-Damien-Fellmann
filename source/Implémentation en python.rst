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
valeur *val* pour la variable *var* et *__repr__* retourne la représentation sous format str de la contrainte.

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
à l'opérateur et à la valeur de référence. Finalement, il faut remettre à jour la valeur initiale de la variable.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 49-59, 61-86
    :linenos:

On implémente la classe **ContrainteBinaire** de manière semblable à la classe **ContrainteUnaire**. Cette fois, 
la liste des variables contiendra les noms des variables *refVar1* et *refVar2*. Les attributs sont ces deux variables ainsi
que l'opérateur *op* et la dimension de ces contraintes est de 2. Le fonctionnement des méthodes reste le même
à la différence que la valeur de référence *ref* est remplacée par la valeur de la variable *refVar2* dans la méthode
*estValide*.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 88-125
    :linenos:

A présent, il s'agit d'implémenter la classe **Variables** qui gère l'ensemble des variables présentes dans un 
problème de satisfaction de contraintes. Elle possède un seul attibut : la liste des variables, vide lors de 
l'instanciation. Afin de la remplir, on utilise la méthode *ajouteVar*. Puis, *retourneVar* permet de retourner 
une variable d'aprés son nom. La méthode *__repr__* quant à elle retourne une chaîne de caractères contenant toutes
les informations sur chaque variable.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 151-162, 173-178
    :linenos:

Comme pour les variables, on définit également une classe **Contraintes** qui s'occupe de l'ensemble des contraintes 
du PSC. Ses attributs *contraintes* et *contraintes_noms* contiennent toutes les contraintes et leur nom et sont 
également vides au départ. Lorsqu'une contrainte est ajoutée avec *ajouteContrainte*, on doit donc aussi rajouter 
son nom dans la liste *contraintes_noms*. Finalement, la méthode *__repr__* est semblable à celle de la classe 
**Variables**.

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
qui est consistante avec toutes les valeurs des autres variables, cela signifie qu'on a trouvé une solution au problème et on 
retourne un dictionnaire contenant les noms des variables et leur valeur. Cependant, si aucune combinaison ne 
fonctionne, l'algorithme retourne "echec".

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 213-224,229, 233-237, 240-253
    :linenos:

Algorithme de forwardchecking
=============================

Chapitre pas encore écrit

Application à la résolution de sudokus
======================================

Afin de résoudre des sudokus à l'aide de l'algorithme de backtrack précédemment implémenté, nous
devons définir les variables, leurs domaines et les contraintes du problème. Les variables correspondent
aux cases vides des grilles de sudokus. Leur domaine est le même pour toutes et est les nombres entre 1 
et la taille de la grille (9 habituellement). Ce sont des contraintes d'inégalités qui définissent
les relations des variables entre elles et des variables avec les cases déjà numérotées : chaque case
d'une même ligne, d'une même colonne ou d'un même carré ne doit pas avoir la même valeur qu'une autre.

La fonction que nous allons développer prend en paramètre une grille sous forme de liste de listes qui sont 
les lignes de la grille, avec des "x" pour les valeurs inconnues, et retourne la grille complétée sous 
le même format.

La première étape consiste alors à implémenter les fonctions *lignes*, *colonnes* et *carres* qui
retourne des listes de listes qui sont les lignes, colonnes ou carrés de la grille.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 271-293
    :linenos:

Ensuite, à partir de la grille de sudoku, on peut créer les variables pour chaque case contenant un 
"x". Leur nom est composé de l'indice *i* de la ligne et de l'indice *j* de la colonne d'où elles se 
trouvent dans la grille. En plus de créer ces variables et de les ajouter à la liste des variables 
(contenue dans une instanciation de la classe **Variables**), on remplace également les "x" de la grille
par les noms des variables.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 295-303
    :linenos:

Pour instancier les contraintes, on implémente la fonction *creation_des_contraintes* qui prend dans le
paramètre *grille* soit la liste des lignes, soit celle des colonnes, soit celle des carrés générées par
les fonctions précédemment définies. Pour chaque case qui contient un nom de variable, on crée les
contraintes unaires portant sur cette variable (par rapport aux cases de la même "ligne" 
contenant un chiffre) et les contraintes binaires portant sur elle et une autre variable de la "ligne". 
De plus, afin d'éviter de créer des contraintes identiques, une copie de la ligne actuelle *ligne2* est 
créée et lorsqu'on instancie les contraintes d'une variable, on la supprime de *ligne2*.
On contrôle également que chaque contrainte ne se trouve pas déjà dans la liste
des contraintes (cette étape est surtout nécessaire lorsqu'on rajoute les contraintes issues des carrés qui 
ont souvent déjà été ajoutées lors des appels de la fonction avec les lignes et les colonnes).

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 306-322
    :linenos:

Puis, la fonction *creation_de_toutes_les_contraintes* génère l'ensemble des 
contraintes en appelant d'abord la fonction *creation_des_variables* pour  
instancier les variables et créer la nouvelle grille contenant le nom de ces
dernières, ainsi qu'en créant 
les listes des lignes, colonnes et carrés avec lesquelles peuvent être générées 
toutes les contraintes. 

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 324-334
    :linenos:

Finalement, il est l'heure de définir la fonction *solution_sudoku* qui peut
résoudre tout sudoku réalisable. On commence par créer des instances des classes
**Contraintes** et **Variables**. Ensuite, on contrôle que la grille de sudoku 
est dans les normes avec les fonctions *grille_valide*, qui vérifie si chaque ligne
a le même nombre d'éléments que la grille a de lignes, et *grille_de_vrai_sudoku*,
qui teste si le nombre de lignes est un carré parfait (car le nombre de carrés 
dans une grille de sudoku correspond à la racine carrées du nombre de lignes) 
(on n'admet donc pas seulement des grilles 9x9 mais aussi par exemple des grilles
16x16). Puis, on appelle la fonction *creation_de_toutes_les_contraintes* qui appelle
aussi la fonction *creation_des_variables* pour ensuite utiliser l'algorithme
de recherche en profondeur d'abord *backtrack* qui prend en paramètre la grille ainsi
que les listes de variables et de contraintes. Si la recherche a été fructueuse, on
insère les valeurs valides des variables dans la grille et on l'imprime, sinon on 
imprime un message indiquant que le sudoku ne peut pas être résolu.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 260-270, 339-359
    :linenos: