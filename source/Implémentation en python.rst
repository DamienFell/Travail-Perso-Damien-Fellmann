Implémentation en python
########################

Maintenant que les notions théoriques de la programmation par contraintes ont
été abordées, nous pouvons implémenter notre algorithme de résolution de sudoku 
en python.

Modélisation des variables et des contraintes
=============================================

Tout d'abord, nous allons modéliser les variables et les contraintes d'un PSC 
en créant leurs classes respectives. Cette section est inspirée en partie de :cite:`Ia_par_la_pratique`.

Premièrement, nous définissons la classe :code:`Variable` : elle possède les attibuts :code:`nom`, :code:`domaine`,
:code:`valeur` (actuelle) et :code:`label`, qui est initalement une copie du domaine.
De plus, elle contient plusieurs méthodes : :code:`metAJourValeur` met à jour la valeur de la variable, 
:code:`enleve_du_label` supprime la valeur rentrée en paramètre
du label et :code:`__repr__` retourne le nom de la variable, son domaine et sa 
valeur dans une chaîne de caractère.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 5-21
    :linenos:
 
Deuxièmement, la classe :code:`Contrainte` doit aussi être définie. Cependant, elle ne sera jamais directement utilisée
et sera héritée par les classes plus spécifiques :code:`ContrainteUnaire` et :code:`ContrainteBinaire` : il s'agit donc
d'une classe abstraite. Son attribut 
:code:`variables` contient la liste des variables sur lesquelles porte la contrainte et
:code:`dimension` détermine 
le nombre de variables sur lesquelles elle agit. La méthode
:code:`estValide` teste si la contrainte est respectée en choisissant la 
valeur :code:`val` pour la variable :code:`var` et :code:`__repr__` retourne 
la représentation sous format :code:`str` de la contrainte.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 23-34
    :linenos:

Désormais, nous devons donc modéliser la classe fille :code:`ContrainteUnaire` qui s'applique aux contraintes portant
sur une seule variable. La liste des variables ne contiendra donc que le nom de la variable impliquée dans la contrainte 
:code:`refVar` prise en paramètre lors de l'instanciation et la dimension vaudra logiquement 1.
Cette classe contient également les attributs :code:`op`, l'opérateur de la contrainte
(<,<=,>,>=,==,!=), la valeur de référence pour l'opérateur :code:`ref`, et la variable :code:`refVar`. Puis, on redéfinit les méthodes
de la classe :code:`Contrainte` : :code:`dimension` retourne logiquement 1 et :code:`__repr__` retourne la variable impliquée,
l'opérateur et la valeur de référence. Pour la méthode :code:`estValide`, on doit d'abord stocker la valeur actuelle de la variabe 
et la mettre à jour avec la valeur rentrée en paramètre. Ensuite, on teste cette valeur par rapport 
à l'opérateur et à la valeur de référence. Finalement, il faut remettre à jour la valeur initiale de la variable.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 43-77
    :linenos:

On implémente la classe :code:`ContrainteBinaire` de manière semblable à la classe :code:`ContrainteUnaire`. Cette fois, 
la liste des variables contiendra les noms des variables :code:`refVar1` et :code:`refVar2`. Les attributs sont ces deux variables ainsi
que l'opérateur :code:`op` et la dimension de ces contraintes est de 2. Le fonctionnement des méthodes reste le même
à la différence que la valeur de référence :code:`ref` est remplacée par la valeur de la variable :code:`refVar2` dans la méthode
:code:`estValide`.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 79-113
    :linenos:

A présent, il s'agit d'implémenter la classe :code:`PSC` qui gère l'ensemble d'un problème 
de satisfaction de contraintes. Elle possède les attributs suivants :
:code:`variables` qui contient la liste des variables, le dictionaire 
:code:`noms_variables` ayant pour clés les noms des variables et pour valeurs les 
variables elles-mêmes, les listes :code:`contraintes_binaires` et :code:`contraintes_unaires`
contenant toutes les contraintes du PSC, ainsi que :code:`iterations` : le nombre
d'appels des algorhithmes récursifs de backtracking ou de forward checking. Puis,
on utilise la méthode :code:`ajouteVar` pour ajouter une 
variable :code:`var` dans :code:`variables` et pour remplir en même temps
:code:`noms_variables`. Ensuite, :code:`retourneVar` permet de retourner 
une variable d'après son nom. La méthode :code:`__repr__` quant à elle retourne 
une chaîne de caractères contenant toutes les informations sur chaque variable et
chaque contrainte.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 139-162
    :linenos:

Modélisation des algorhithmes de pré-résolution
=============================================

Dans cette sous-section, on implémente les méthodes de pré-résolution présentées 
précédemment. 

On définit d'abord la méthode :code:`consistance_contraintes_unaires` afin de réduire les 
labels de chaque variable en enlevant toutes les valeurs inconsistantes par rapport
aux contraintes unaires, ce qui signifie que les algorhitmes de backtracking et de
forward checking n'utiliseront ensuite que les contraintes binaires.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 167-173
    :linenos:

La consistance par rapport aux contraintes binaires est implémentée de la manière 
suivante. D'abord, on définit au sein de la classe :code:`Contrainte_binaire` une 
méthode :code:`modifier_labels` qui supprime les valeurs inconsistances entre les
deux variables d'une contrainte binaire. Elle examine une par une chaque valeur 
des labels des deux variables et utilise la méthode :code:`est_possible` pour déterminer 
s'il existe au moins une valeur de l'autre variable consistante avec la valeur
testée. A la fin, :code:`modifier_labels` retourne un booléen signifiant si les 
labels ont été réduits ou non. 

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 114-138
    :linenos:

Ensuite, la méthode :code:`consistance_contraintes_binaires` effectue 
:code:`modifier_labels` sur chaque contrainte et si au moins une contrainte
a modifié des labels, on réexécute l'algorithme. 

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 173-180
    :linenos:

Pour effectuer le tri initial des variables, on utilise la  méthode sort sur la liste 
des variables qui effectue le tri par rapport à la taille des labels.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 181-183
    :linenos:

Algorithme de backtracking
==========================

Nous allons maintenant implémenter à l'intérieur de la 
classe :code:`PSC` l'algorithme de recherche en profondeur d'abord 
dans la méthode :code:`backtrack`. D'abord, le premier paramètre :code:`k` correspond à l'indice de la variable actuelle 
sur laquelle on teste les valeurs, valant initalement 0. Lorsqu'on teste les valeurs de la variable suivante, on rappelle la fonction
avec :code:`k+1` en paramètre : cette fonction est donc récursive. Mais avant d'être rappelée, elle fait appel à la 
fonction :code:`consistance_avec_vars_precedentes` qui est au coeur du fonctionnement de l'algorithme. Elle passe en revue 
toutes les contraintes portant sur la variable d'indice :code:`k` et sur les variables d'indice plus petit que :code:`k`
précédemment instanciées et teste si la combinaison des valeurs attribuées est consistante, c'est à dire si elle 
respecte ces contraintes. C'est donc seulement si toutes ces contraintes sont respectées qu'on peut passer à l'attribution
de la valeur de la variable d'indice :code:`k+1`. Si le programme arrive à donner une valeur à la dernière variable
qui est consistante avec toutes les valeurs des autres variables, cela signifie qu'on a trouvé une solution au problème et on 
retourne un dictionnaire contenant les noms des variables et leur valeur. Cependant, si aucune combinaison ne 
fonctionne, l'algorithme retourne "echec".

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 198-235
    :linenos:

Afin de mieux comprendre l'algorithme de backtracking, prenons l'exemple du PSC de la 
:numref:`reseau`. Tout d'abord, il s'agit d'instancier les différentes variables et contraintes :
par exemple on a le code suivant pour la première variable : :code:`x1 = Variable("x1", ["b","c"])`, et pour la 
contrainte entre la variable :code:`x1` et :code:`x2` on a ceci : :code:`c12 = Contrainte_binaire(x1,"!=",x2)`. Après 
avoir ajouter toutes nos variables et contraintes dans les instances des classes :code:`Variables` et 
:code:`Contraintes`, nous pouvons exécuter l'algorhitme de backtracking, représenté par la 
pseudo-exécution suivante dans laquelle les assignations des valeurs solutions sont représentées 
en jaune :

.. figure:: backtrack_exemple.png
    :align: left
    
    Pseudo-exécution de l'algorithme de backtracking du PSC de la :numref:`reseau`

Algorithme de forward checking
=============================

Il s'agit maintenant d'implémenter l'algorhitme de forward checking dont
la structure récursive est la même que pour le backtracking. A chaque
niveau :code:`k`, on commence par définir la variable actuelle et par
effectuer une copie des labels actuels dans la variable :code:`anciens_labels`
grâce à la fonction :code:`retourne_labels`. Ensuite, on a le même code
que la fonction :code:`backtrack` mais :code:`consistance_avec_vars_precedentes`
est remplacée par :code:`propagation_aux_vars_suivantes`. Cette fonction regarde
pour chaque contrainte si une variable d'indice plus grand que :code:`k`
est l'une des variables sur laquelle la contrainte s'applique. Si c'est le cas,
on utilise la méthode de la classe :code:`Contrainte propage`. Cette dernière
supprime les valeurs inconsistantes par rapport à la contrainte du label
de la variable et à la fin, on retourne :code:`True` si le label contient
encore des valeurs et :code:`False` s'il est vide. Ainsi, si le label
n'est pas vide après la propagation, on peut continuer la propagation
avec les contraintes suivantes. Sinon, la
:code:`propagation_aux_vars_suivantes` de la variable actuelle 
retourne :code:`False` et on s'arrête
, car on ne peut pas continuer la recherche avec un label vide, et on remet 
à jour les labels avec la variable :code:`anciens_labels` et la fonction
:code:`met_a_jour_labels`. De plus, avant de réappeler le :code:`forward_checking`
avec l'indice :code:`k+1`, on réorganise légèrement la liste des variables avec la 
méthode :code:`dynamic_ordering` qui échange la variable d'indice `k+1` avec une
variable avec le plus petit label afin d'effectuer l'algorhithme  de forward checking
de l'étape suivante avec une variable la plus restrictive.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 35-42, 184-196, 239-284
    :linenos:

Application à la résolution de sudokus
======================================

Afin de résoudre des sudokus à l'aide de l'algorithme de backtracking ou
de forward checking précédemment implémenté, nous
devons définir les variables, leurs domaines et les contraintes du problème. Les variables correspondent
aux cases vides des grilles de sudokus. Leur domaine est le même pour toutes et est les nombres entre 1 
et la taille de la grille (9 habituellement). Ce sont des contraintes d'inégalités qui définissent
les relations des variables entre elles et des variables avec les cases déjà numérotées : chaque case
d'une même ligne, d'une même colonne ou d'un même carré ne doit pas avoir la même valeur qu'une autre.

Pour y parvenir, nous allons développer la classe :code:`Sudokus_PSC` qui est une classe
fille de la classe :code:`PSC`. Lors de son instanciation, elle prend comme attribut la grille 
de sudoku qu'il faut résoudre, sous forme de liste de listes qui sont 
les lignes de la grille, avec des "." pour les valeurs inconnues.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 290-294
    :linenos:
    
La prochaine étape consiste ensuite à implémenter les méthodes 
:code:`lignes`, :code:`colonnes` et :code:`carres` qui
retournent des listes de listes qui sont les lignes, colonnes ou carrés de la grille.

Pour illustrer cela, voici ci-dessous une grille de sudokus qui correspond à la liste
:code:`[[5,1,4,8,.,6,.,.,9],
[.,.,6,.,5,.,.,.,.],
[.,3,8,.,1,9,6,4,.],
[6,.,.,4,8,.,5,.,.],
[4,8,.,9,.,.,7,6,.],
[3,7,9,5,.,1,.,8,.],
[9,6,.,7,4,.,1,3,.],
[.,.,.,.,.,8,.,.,2],
[.,.,3,.,9,.,4,7,.]]` (les :code:`.` sont en réalité des :code:`"."`) :

.. figure:: exemple_sudoku.png
    
    Exemple de sudoku tiré de :cite:`1000_sudokus`

En vert est mise en évidence la première ligne de la liste retournée par la fonction :code:`lignes`,
représentée par la liste :code:`[5,1,4,8,.,6,.,.,9]`, en
bleu la première colonne de la fonction :code:`colonnes` représentée par la liste 
:code:`[5,.,.,6,4,3,9,.,.]` et en orange le premier carré de la fonction 
:code:`carres` représenté par la liste :code:`[5,1,4,.,.,6,.,3,8]`.

Voici donc le code implémentant ces trois méthodes :

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 312-335
    :linenos:

Ensuite, à partir de la grille de sudoku, on peut créer les variables pour chaque case contenant un 
".". Leur nom est composé de l'indice :code:`i` de la ligne et de l'indice :code:`j` de la colonne d'où elles se 
trouvent dans la grille. En plus de créer ces variables et de les ajouter à la liste des variables,
on remplace également les "." de la grille
par les noms des variables.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 336-344
    :linenos:

Pour instancier les contraintes, on implémente la méthode :code:`creation_des_contraintes` qui prend dans le
paramètre :code:`grille` soit la liste des lignes, soit celle des colonnes, soit celle des carrés générées par
les fonctions précédemment définies. Pour chaque case qui contient un nom de variable, on crée les
contraintes unaires portant sur cette variable (par rapport aux cases de la même "ligne" 
contenant un chiffre) et les contraintes binaires portant sur elle et une autre variable de la "ligne". 
De plus, afin d'éviter de créer des contraintes identiques, une copie de la ligne actuelle :code:`ligne2` est 
créée et lorsqu'on instancie les contraintes d'une variable, on la supprime de :code:`ligne2`.
On contrôle également que chaque contrainte ne se trouve pas déjà dans la liste
des contraintes (cette étape est surtout nécessaire lorsqu'on rajoute les contraintes issues des carrés qui 
ont souvent déjà été ajoutées lors des appels de la fonction avec les lignes et les colonnes).

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines:  345-362
    :linenos:

Puis, la méthode:code:`creation_de_toutes_les_contraintes` génère l'ensemble des 
contraintes en appelant d'abord la méthode :code:`creation_des_variables` pour  
instancier les variables et créer la nouvelle grille contenant le nom de ces
dernières, ainsi qu'en créant 
les listes des lignes, colonnes et carrés avec lesquelles peuvent être générées 
toutes les contraintes. 

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 363-373
    :linenos:

Finalement, il est l'heure de définir la méthode :code:`solution_sudoku` qui doit 
être appelée après avoir créer une instance :code:`Sudokus_PSC` et qui résout donc
toute grille de sudoku réalisable. En fait, lors de l'instanciation du PSC, on va déjà 
vérifier que la grille contrôler que la grille de sudoku 
est dans les normes avec la méthode :code:`grille_valide`, qui vérifie si chaque ligne
a le même nombre d'éléments que la grille a de lignes. Puis, on crée les contraintes 
avec :code:`creation_de_toutes_les_contraintes` et
on appelle les 3 méthodes de pré-résolution code:`consistance_contraintes_unaires`,
:code:`consistance_contraintes_binaires` et :code:`sort_variables`. La méthode 
:code:`solution_sudoku` ne s'occupe que de résoudre le sudoku avec l'algorithme de
backtracking ou de forward checking choisi en paramètre. Si la recherche a été fructueuse, on
insère les valeurs valides des variables dans la grille et on l'imprime, sinon on 
imprime un message indiquant que le sudoku ne peut pas être résolu, ce qui signifie
qu'il n'a pas été généré correctement.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 306-311, 374-388
    :linenos: