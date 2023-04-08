.. module:: sphinx.ext.mathbase

Notions théoriques de la programmation par contraintes
######################################################

Tout d'abord, il s'agit de présenter les éléments et notions théoriques de la programmation 
par contraintes nécessaires à l'implémentation d'un algorithme de résolution de sudokus.

Notions de bases
================

Qu'est-ce que la programmation par contraintes ? Ce paradigme est une façon de résoudre des 
problèmes décrits par un ensemble de variables sur lesquelles agissent des contraintes. Une 
solution à ces problèmes consiste à affecter à chaque variable une valeur respectant les contraintes.
Chaque variable possède un domaine qui contient toutes les valeurs qu'elle peut admettre. Les 
contraintes, quant à elles, définissent les relations que doivent entretenir les variables entre elles
ou avec des valeurs de référence et qui limitent l'ensemble des valeurs qu'elles peuvent prendre simultanément. 
Une contrainte peut notamment être de type arithmétique (=, ≠, <, <= ,>, >=) quand elle compare plusieurs valeurs.
Elles peuvent donc concerner une seule variable dans le cas des contraintes unaires,
deux variables dans le cas des contraintes binaires ou plus dans le cas des contraintes multiples. 
Par exemple, la contrainte :math:`c` imposant qu'une variable :math:`x_1` possède une valeur :math:`v_1` 
plus grande que la valeur :math:`v_2` de la variable :math:`x_2` peut s'écrire de la manière suivante : 
:math:`c = \{ (v_1, v_2 ) | v_1>v_2 \}`.

Ainsi, un problème de satisfaction de contraintes (PSC) se définit de la manière suivante :

- L'ensemble de variables :math:`X = \{x_1, x_2, ..., x_n \}`.
- L'ensemble des domaines associés aux variables : :math:`D = \{d_1, d_2, ..., d_n \}`.
- L'ensemble des contraintes qui portent sur les variables : :math:`C = \{c_1, c_2, ..., c_m \}`.

Représentation d'un PSC
=======================

Une manière simple de visualiser et de comprendre de tels problèmes est la représentation par 
un graphe de contraintes dans lequel les noeuds correspondent aux variables et les arcs correspondent
aux contraintes. Voici par exemple un réseau de contraintes binaires, qui sera réutilisé par la suite, contenant quatre 
variables :math:`x_1, x_2, x_3` et :math:`x_4`, leur domaines respectifs :math:`d_1 = \{b,c\}, d_2 = \{a,c\}, d_3 = \{b,c\}`
et :math:`d_4 = \{a,b\}` ainsi que les contraintes d'inégalité les reliant représentées par les flêches (donc les variables reliées 
ne doivent pas avoir la même valeur):

.. _reseau: 
.. figure:: reseau_contraintes_binaires.png
    
    Réseau de contraintes binaires tiré de :cite:`Ia_par_la_pratique`

Méthodes de résolution
======================

Il existent diverses méthodes de résolution des problèmes de satisfaction de contraintes à l'aide 
d'algorithmes de recherche où l'on énumère toutes les combinaisons possibles de valeurs pour 
les variables jusqu'à trouver celles respectant toutes les contraintes. 

Méthode du retour-arrière / backtracking
....................

Dans ce travail, nous nous intéresserons uniquement aux méthodes basées
sur la recherche en profondeur d'abord, aussi appelée retour-arrière ou 
backtracking : dans un 
schéma arborescent, on explore chaque branche jusqu'au bout avant de remonter et d'explorer les
autres branches. Dans la figure 2, on commence par le noeud A et on explore ensuite les autres noeuds, 
les noeuds fils, en descendant, puis en remontant dans l'arbre jusqu'à tomber sur la solution au noeud I.

.. figure:: Arbre_profondeur.png
    
    Graphe d'une recherche en profondeur

Dans un problème de satisfaction de contraintes, la profondeur des nœuds correspond au nombre de
variables satisfaisant les contraintes : on commence par tester et par attribuer une valeur pour une variable et on
fait de même avec les autres variables en descendant dans l'arbre de recherche. Lorsqu’aucune des valeurs du domaine d’une variable ne 
peut coïncider avec les valeurs des variables déjà définies et les contraintes, on remonte et on continue la recherche avec d’autres valeurs 
de la variable du niveau parent et ainsi de suite. 

Le PSC de la :numref:`reseau` peut ainsi être résolu de la manière suivante (les \* représentent les 
situations où aucune valeur du domaine d'une variable ne satisfait les contraintes, ce qui 
entraîne un retour en arrière):

..  csv-table:: Recherche en profondeur du PSC de la :numref:`reseau`
    :header: "Etape", ":math:`x_1`", ":math:`x_2`", ":math:`x_3`", ":math:`x_4`"
    :widths: 5, 10, 10, 10, 10

    1, ":math:`b`", \-, \-, \-
    2, ":math:`b`", ":math:`a`", \-, \-
    3, ":math:`b`", ":math:`a`", ":math:`c`", \-
    4, ":math:`b`", ":math:`a`", ":math:`c`", \*
    5, ":math:`b`", ":math:`a`", \*, \-
    6, ":math:`b`", ":math:`c`", \-, \-
    7, ":math:`b`", ":math:`c`", \*, \-
    8, ":math:`b`", \*, \-, \-
    9, ":math:`c`", \-, \-, \-
    10,":math:`c`", ":math:`a`", \-, \-
    11,":math:`c`", ":math:`a`", ":math:`b`", \-
    12,":math:`c`", ":math:`a`", ":math:`b`", ":math:`b`"

Méthode du forward checking
....................

A présent, il est possible d'améliorer notre recherche en profondeur d'abord grâce à la méthode du
forward checking. Ce dernier permet d'éviter à l'avance d'assigner des valeurs inconsistantes, donc qui
ne respectent pas leurs contraintes, aux variables pour lesquelles aucune valeur n'a été encore attribuée. 
Pour y parvenir, nous créons pour chaque variable :math:`x_i` un label :math:`L_i` correspondant à un sous-ensemble de son domaine :
:math:`L_i ⊂ D_i`. Les valeurs testées ne seront donc plus toutes les valeurs possibles des domaines mais toutes 
les valeurs possibles des labels actuels. Par conséquent, à chaque nouvelle affectation de valeur pour une variable
:math:`x_i`, on met à jour les labels des variables :math:`x_j` avec :math:`j>i` : on élimine toutes les valeurs inconsistantes
par rapport aux valeurs déjà attribuées de leurs labels respectifs. A chaque fois qu'un label d'une variable dont la valeur n'a pas
encore été attribuée est vide, il faut tester une autre valeur pour la variable actuelle
ou faire un retour en arrière si son label est également vide. Dans ces cas-là, on met également 
à jour les labels avec des sauvegardes qu'on a effectuées avant l'affectation de chaque valeur.

Voici ci-dessous la résolution du PSC de la :numref:`reseau` grâce à la méthode 
du forward checking.

..  csv-table:: Méthode du forward checking avec le PSC de la :numref:`reseau`
    :header: "Etape", ":math:`x_1`", ":math:`x_2`", ":math:`x_3`", ":math:`x_4`", ":math:`l_1`", ":math:`l_2`", ":math:`l_3`", ":math:`l_4`"
    :widths: 5,5,5,5,5,5,5,5,5
    
    **0**,\-,\-,\-,\-,:math:`\{ b ; c \}`,:math:`\{ a ; c \}`,:math:`\{ b ; c \}`,:math:`\{ a ; b \}`
    **1**,:math:`b`,\-,\-,\-,:math:`\{ b ; c \}`,:math:`\{ a ; c \}`,:math:`\{ c \}`,:math:`\{ a \}`
    **2**,:math:`b`,:math:`a`,\-,\-,:math:`\{ b ; c \}`,:math:`\{ a ; c \}`,:math:`\{ c \}`, :math:`\{ \}` 
    **3**,:math:`b`,:math:`c`,\-,\-,:math:`\{ b ; c \}`,:math:`\{ a ; c \}` ,:math:`\{ \}` ,:math:`\{ a \}` 
    **4**,:math:`c`,\-,\-,\-,:math:`\{ b ; c \}` ,:math:`\{ a \}`,:math:`\{ b \}`,:math:`\{ a ; b \}` 
    **5**,:math:`c`,:math:`a`,\-,\-,:math:`\{ b ; c \}` ,:math:`\{ a \}` ,:math:`\{ b \}`,:math:`\{ b \}`
    **6**,:math:`c`,:math:`a`,:math:`b`,\-,:math:`\{ b ; c \}` ,:math:`\{ a \}` ,:math:`\{ b \}` ,:math:`\{ b \}` 
    **7**,:math:`c`,:math:`a`,:math:`b`,:math:`b`,:math:`\{ b ; c \}` ,:math:`\{ a \}` ,:math:`\{ b \}` ,:math:`\{ b \}` 
    
On remarque que le nombre d'étapes nécessaires diminue déjà pour un problème facile à résoudre. On peut
dès lors s'imaginer que cette amélioration sera très bénéfique 
pour la résolution d'un problème plus complexe comme celui des sudokus.