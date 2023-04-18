.. _conclusion.rst:

Conclusion
##########

Somme toute, le jeu de sudoku a permis de mettre en pratique le fonctionnement
de la programmation par contraintes. Il a d'abord s'agit de présenter les notions
de variables, de domaines et de contraintes, constituants essentiels
du paradigme. Ensuite a été présenté théoriquement le 
fonctionnement de l'algorithme de retour-arrière basé sur la recherche en 
profonder d'abord dans un arbre de recherche où l'on assigne les valeurs
aux variables les unes après les autres. Le principe du forward checking
a lui aussi été décrit : cette méthode de résolution se base sur la propagation
des assignations de valeur aux variables non encore instanciées. Elle permet
de réduire la taille des domaines au cours de la résolution à travers les sous-ensembles
des domaines, les labels. Les algorithmes secondaires comme la consistance des
arcs et des noeuds, qui permet de supprimer à l'avance
certaines valeurs des labels, ainsi que les tris intial et
progressif de la liste des variables en fonction de la taille
des labels ont également été évoqués.

Dans la deuxième section, on a appliqué cette théorie dans un programme informatique
en python en s'aidant notamment de fonctions récursives pour les algorithmes
de backtracking et de forward checking. Il a fallu ensuite transformer un 
jeu de sudoku en un problème de satisfaction de contraintes : toutes les cases
vides constituent les variables et celles-ci sont rattachées entre elles et 
par rapport aux cases auxquelles un nombre est déjà attribué à des
contraintes d'inégalité. En rassemblant toutes ces parties de codes ensemble,
un programme fonctionnel de résolution de sudokus a ainsi pu être créé.

En dernière partie de ce travail, les algorithmes de backtracking et de 
forward checking ont été comparés : grâce à la résolution de centaines de
sudokus différents, il a pu être constaté que les performances étaient 
nettement meilleures avec le forward checking. En effet, cette
méthode a la capacité de réduire grandement le nombre d'itérations nécessaires
de l'algorithme en réduisant constamment la taille des labels, ce qui lui
permet d'économiser beaucoup de temps. Finalement, on a aussi remarqué que
les performances dépendent de manière importante des algorithmes 
secondaires de consistance des arcs et des noeuds et de tri. C'est surtout
le tri progresif, qu'on a appelé :code:`dynamic_ordering`, qui a la plus grande
influence grâce à sa fonction de guide dans l'arbre de recherche à chaque 
itération, redirigeant la résolution vers les variables avec les plus petits
labels.

Ainsi, la programmation par contraintes semble être une façon efficace de 
résoudre certains problèmes comme celui des sudokus. Mais elle ne sert
pas uniquement à trouver des solutions à des jeux logiques, elle trouve notamment
des applications dans des problèmes logistiques complexes d'emploi du temps et
d'affectation par exemple. Ce travail constitue par conséquent une introduction à une 
manière de problématiser et de conceptualiser un problème en informatique grâce
aux contraintes.

