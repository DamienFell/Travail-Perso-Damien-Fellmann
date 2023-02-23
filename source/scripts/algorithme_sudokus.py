import copy
import math

class Variable :
    def __init__(self, nom, domaine):
        self.nom = nom
        self.domaine = domaine
        self.valeur = None
        self.label = []
        self.initLabel()
    
    def initLabel(self): #(Ré)Initialise le label
        self.label =copy.deepcopy(self.domaine)
        
    def enleveDuLabel(self, d): #Efface la valeur d du label
        if d in self.label :
            self.label.remove(d)
            
    def metAJourValeur(self, valeur) : 
        self.valeur = valeur
        
    def nomEstEgal(self, nom):
        return self.nom == nom
    
    def tailleDuDomaine(self): # Retourne la taille du domaine
        return len(self.domaine)
    
    def tailleDuLabel(self): # Retourne la taille du label
        return len(self.label)
    
    def __repr__(self): 
        string =f"{self.nom} : valeur : {self.valeur}, domaine : {self.domaine}"
        return string

class Contrainte:
    def __init__(self, variables):
        self.variables = variables 
        
    def dimension(self): 
        return 0
    
    def estValide(self, var, val):
        return False
    
    def __repr__(self): 
        string = f"Contrainte : variables = {self.variables}"
        return string
        
class ContrainteUnaire(Contrainte):
    def __init__(self, refVar, op, ref):
        Contrainte.__init__(self, [refVar.nom])
        self.op = op 
        self.ref = ref 
        self.refVar = refVar 
    
    def dimension(self) :
        return 1 
    
    def estValide(self, var, val):
  
        valeur = var.valeur  
        var.metAJourValeur(val)
        valide = False
        
        if self.op == "<":
            valide = self.refVar.valeur < self.ref
        elif self.op == "<=":
            valide = self.refVar.valeur <= self.ref
        elif self.op == ">":
            valide = self.refVar.valeur > self.ref
        elif self.op == ">=":
            valide = self.refVar.valeur >= self.ref
        elif self.op == "==":
            valide = self.refVar.valeur == self.ref
        elif self.op == "!=":
            valide = self.refVar.valeur != self.ref
        else :
            print(f"Opérateur : {self.op}, non implémenté")
            
        var.metAJourValeur(valeur) 
        
        return valide
    
    def __repr__(self) :
        string = f"Contrainte unaire : variable = {self.refVar}, opérateur : {self.op}, valeur de référence : {self.ref}"
        return string
            
class ContrainteBinaire(Contrainte):
    def __init__(self, refVar1, op, refVar2):
        Contrainte.__init__(self, [refVar1.nom,refVar2.nom])
        self.refVar1 = refVar1 #Valeur de référence à droite de l'opérateur
        self.op = op #Opérateur (<,<=,>,>=,==,!=)
        self.refVar2 = refVar2 #Valeur de référence à gauchee de l'opérateur
        
    def dimension(self):
        return 2 #Car c'est une contrainte binaire
    
    def estValide(self, var, val):
 
        valeur = var.valeur #Sauvegarde la valeur actuelle de la variable var avant qu'elle soit modifiée
        var.metAJourValeur(val)
        valide = False
        
        if self.op == "<":
            valide = self.refVar1.valeur < self.refVar2.valeur
        elif self.op == "<=":
            valide = self.refVar1.valeur <= self.refVar2.valeur
        elif self.op == ">":
            valide = self.refVar1.valeur > self.refVar2.valeur
        elif self.op == ">=":
            valide = self.refVar1.valeur >= self.refVar2.valeur
        elif self.op == "==":
            valide = self.refVar1.valeur == self.refVar2.valeur
        elif self.op == "!=":
            valide = self.refVar1.valeur != self.refVar2.valeur
        elif self.op == "NAND":
            valide = not(self.refVar1.valeur == True and self.refVar2.valeur == True)
        elif self.op == "->":
            valide = (self.refVar1.valeur == False and self.refVar2.valeur == True)
        else :
            print(f"Opérateur : {self.op}, non implémenté")
            
        var.metAJourValeur(valeur) #Annule la sauvegarde de la valeur val dans la variable
        
        return valide        

    def __repr__(self) :
        string = f"Contrainte binaire : variables = {self.refVar1} et {self.refVar2}  , opérateur : {self.op}"
        return string

    def estPossible(self, var): #Détermine si la contrainte peut être satisfaite pour au moins une valeur du domaine
        if len(var.domaine) == 0:
            return False
        
        for d in var.domaine:
            if self.estValide(var, d):
                return True #sSi au moins une valeur convient
        
        return False #Si aucune valeur ne convient
    
    def reviser(self):
        modifiee = False
        
        for paire in [[self.refVar1,self.refVar2],[self.refVar2,self.refVar1]]:
            for x in paire[0].domaine : #Test avec chaque valeur de la première variable
                paire[0].metAJourValeur(x)
                
                if not self.estPossible(paire[1]): #Si la valeur ne peut pas satisfaire la contrainte, on l'enlève du domaine
                    paire[0].domaine.remove(x)
                    modifiee = True
            
            paire[0].metAJourValeur(None)
        return modifiee

class Variables :
    def __init__(self):
        self.variables = []
    
    def retourneVar(self, nom): #Retourne une variable d'après son nom
        for var in self.variables :
            if var.nomEstEgal(nom) :
                return var
        return None
    
    def ajouteVar(self, var): #Ajoute une nouvelle variable dans la liste des variables
        self.variables.append(var)
    
    def consistanceDesNoeuds(self, contraintes): #Pour chaque contrainte unaire, on supprime des domaine des variable les valeurs qui ne respectent pas la contrainte
        for c in contraintes:
            if c.dimension() == 1:
                for val in c.refVar.domaine :
                    if not c.estValide(c.refVar,val) :
                        c.refVar.domaine.remove(val)
  
    def retourneNbVars(self): #Retourne le nombre de variables
        return len(self.variables)
    
    def __repr__(self):
        str = "Vars : \n"
        for var in self.variables :
            str += "\t" + var.__repr__() + "\n"
        return str

class Contraintes :
    def __init__(self):
        self.contraintes = []
        self.contraintes_noms = []
    
    def ajouteContrainte(self, c): #Ajoute une nouvelle contrainte dans la liste des contraintes
        self.contraintes.append(c)
        self.contraintes_noms.append(repr(c))
    
    def consistanceDesArcs(self):
        refaire = False
        for c in self.contraintes:
            if c.dimension == 2 and c.reviser():
                refaire == True
        if refaire : #Si on peut peut-être encore supprimer des valeurs des domaines, on refait l'algorithme.
            self.consistanceDesArcs()
    
    def retourneNbContraintes(self) : #Retourne le nombre de contraintes
        return len(self.contraintes)
    
    def representation(self):
        str = "Contraintes : \n"
        for c in self.contraintes :
            str += "\t" + c.__repr__() + "\n"
        return str



def afficheSolution(algo, solution) :
    print(f"Solutions avec l'algorithme {algo} : {str(solution)}" )

def afficheNbIterations(algo, iterations):
    print(f"Nombre d'itérations avec l'algorithme {algo} : {str(iterations)}" )

def consistanceAvecVarsPrecedentes(k, contraintes, variables): #Vérifie si chaque contrainte portant sur la variable k 
    for c in contraintes :                                     #et sur au moins une des variables précédentes est satisfaite
        if variables[k].nom in c.variables:
            for i in range(0,k+1):
                if variables[i].nom in c.variables :
                    if c.estValide(variables[k],variables[k].valeur):
                        break
                    else :
                        return False
    return True                        
            
def backtrack(k, contraintes, variables, iterations = 0): #k : indice de la variable actuelle
    algo="bt"
    
    iterations +=1
    
    if k>=len(variables): #si la dernière variable a été trouvée, on affiche la solution trouvée et l'ajoute à la liste des solutions
        
        afficheNbIterations(algo,iterations)
        
        solution = {}
        
        for var in variables :
            solution[var.nom]=var.valeur
        
        #afficheSolution(algo,solution) 
        
        return solution
    
    else :
        var = variables[k]
        
        for val in var.domaine: #teste toutes les valeurs du domaine
            var.metAJourValeur(val)
            if consistanceAvecVarsPrecedentes(k, contraintes, variables): #Si la consistance est valide, on continue l'algorithme sur la variable k+1
                reste = backtrack(k+1, contraintes, variables, iterations)
                if reste != "echec":
                    return reste
    #Si aucune valeur n'est consistante à cette étape, on retourne à l'étape précédente sans avoir attribué de valeur à la variable actuelle
    var.metAJourValeur(None)
    return "echec"    



###############################################################################################################################################################


def grille_valide(grille):
    for ligne in grille :
        if not len(ligne) == len(grille):
            return False
    return True

def grille_de_vrai_sudoku(grille):
    if math.sqrt(len(grille))-int(math.sqrt(len(grille)))==0:
        return True
    return False
    
def lignes(grille):
    return grille

def colonnes(grille):
    result = []
    for i in range(len(grille)):
        colonne = []
        for j in range(len(grille)):
            colonne.append(grille[j][i])
        result.append(colonne)
    return result

def carres(grille):
    result = []
    taille_carre = int(math.sqrt(len(grille)))
    for i in range(taille_carre):
        for j in range(taille_carre):
            carre = []
            for k in range(taille_carre):
                for l in range(taille_carre):
                    carre.append(grille[taille_carre*i+k][taille_carre*j+l])
            result.append(carre)
    return result

def creation_des_variables(grille, variables):
    for i in range(len(grille)) :
        for j in range(len(grille)) :
            if grille[i][j] == "x":
                domaine = list(range(1,len(grille)+1))
                var = Variable(f"var({i},{j})",domaine)
                variables.ajouteVar(var)
                grille[i][j] = f"var({i},{j})"
    return grille

def creation_des_contraintes(grille, contraintes, variables):
    for ligne in grille :
        ligne2=ligne.copy() #Création d'une copie de la ligne qui peut être modifiée mais qui n'affectera pas la ligne originale
        for x in ligne :
            if not type(x) is int : #si la case est ne contient pas encore de chiffre
                var = variables.retourneVar(x)
                ligne2.remove(x) #on enlève la variable en question pour ne pa générer
                                #de contrainte avec elle-même et ne pas avoir 2 contraintes identiques 
                for y in ligne2 :
                    if type(y) is int:
                        contrainte = ContrainteUnaire(var,"!=",y)
                        if not repr(contrainte) in contraintes.contraintes_noms :
                            contraintes.ajouteContrainte(contrainte)
                    else :
                        var2 = variables.retourneVar(y)
                        contrainte = ContrainteBinaire(var,"!=",var2)
                        if not repr(contrainte) in contraintes.contraintes_noms :
                            contraintes.ajouteContrainte(contrainte)        
                        
def creation_de_toutes_les_contraintes(grille, contraintes, variables):
    
    if not grille_valide(grille) or not grille_de_vrai_sudoku(grille):
        raise Exception("La grille n'est pas valide")
    
    grille = creation_des_variables(grille, variables)
    
    Lignes = lignes(grille)
    Colonnes = colonnes(grille)
    Carres = carres(grille)
    
    creation_des_contraintes(Lignes, contraintes, variables)
    creation_des_contraintes(Colonnes, contraintes, variables)
    creation_des_contraintes(Carres, contraintes, variables)
    
    #variables.consistanceDesNoeuds(contraintes.contraintes)
    #contraintes.consistanceDesArcs()

def solution_sudokus(grille):
       
    contraintes = Contraintes()
    variables = Variables()
    
    creation_de_toutes_les_contraintes(grille, contraintes, variables)
    
    sol = backtrack(0,contraintes.contraintes,variables.variables)
    
    for var in variables.variables:
        i = int(var.nom[4])
        j = int(var.nom[6])
        
        grille[i][j] = var.valeur
    
    print(grille)

grille1=[[1,"x",3,"x"],["x",3,2,"x"],[3,"x","x",2],[2,"x","x","x"]]
grille2 = [[5,4,"x","x",2,"x",8,"x",6],
           ["x",1,9,"x","x",7,"x","x",3],
           ["x","x","x",3,"x","x",2,1,"x"],
           [9,"x","x",4,"x",5,"x",2,"x",],
           ["x","x",1,"x","x","x",6,"x",4],
           [6,"x",4,"x",3,2,"x",8,"x"],
           ["x",6,"x","x","x","x",1,9,"x"],
           [4,"x",2,"x","x",9,"x","x",5],
           ["x",9,"x","x",7,"x",4,"x",2]
           ]


solution_sudokus(grille2)

