Comparaison des performances des algorithmes
############################################

Cette section vise à tester les algorithmes définis dans la section 
précédente et à montrer leur efficacité. Pour cela, nous allons 
nous aider d'un générateur de sudokus qui se trouve sur le site 
https://qqwing.com/generate.html et résoudre un grand nombre de grilles
différentes. Les grilles générées sont stockées dans un fichier .txt et il 
faut donc tout d'abord extraire toutes les grilles dans une liste de grilles.
Voici un exemple de deux grilles dans le format généré.

..  literalinclude:: scripts/sudokus.txt
    :lines: 1-20

Pour extraire toutes les grilles, on utilise d'abord la fonction :code:`open`
et la méthode :code:`readlines` qui crée une liste avec une chaine caractères
pour chaque ligne du fichier. Ensuite, on définit la fonction 
:code:`lines_to_sudokus` qui prend en paramètre la liste ainsi extraite.

..  literalinclude:: scripts/algorithme_sudokus.py
    :lines: 444-449, 391-405
    :linenos:
