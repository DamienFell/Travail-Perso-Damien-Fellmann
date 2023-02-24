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
        self.refVar1 = refVar1 
        self.op = op #
        self.refVar2 = refVar2 
        
    def dimension(self):
        return 2 
    
    def estValide(self, var, val): 
        valeur = var.valeur 
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
        else :
            print(f"Opérateur : {self.op}, non implémenté")
            
        var.metAJourValeur(valeur) 
        
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

    def ajouteVar(self, var): 
        self.variables.append(var)

    def retourneVar(self, nom): 
        for var in self.variables :
            if var.nomEstEgal(nom) :
                return var
        return None
    
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
    
    def ajouteContrainte(self, c): 
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
    
    def __repr__(self):
        str = "Contraintes : \n"
        for c in self.contraintes :
            str += "\t" + c.__repr__() + "\n"
        return str



def afficheSolution(algo, solution) :
    print(f"Solutions avec l'algorithme {algo} : {str(solution)}" )

def afficheNbIterations(algo, iterations):
    print(f"Nombre d'itérations avec l'algorithme {algo} : {str(iterations)}" )

def consistanceAvecVarsPrecedentes(k, contraintes, variables): 
    for c in contraintes :                                
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
    
    if k>=len(variables):
        
        #afficheNbIterations(algo,iterations)
        
        solution = {}
        
        for var in variables :
            solution[var.nom]=var.valeur
        
        #afficheSolution(algo,solution) 

        return solution
    
    else :
        var = variables[k]
        
        for val in var.domaine: 
            var.metAJourValeur(val)
            if consistanceAvecVarsPrecedentes(k, contraintes, variables): #Si la consistance est valide, on continue l'algorithme sur la variable k+1
                reste = backtrack(k+1, contraintes, variables, iterations)
                if reste != "echec":
                    return reste
    
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
        ligne2=ligne.copy()
        for x in ligne :
            if not type(x) is int :
                var = variables.retourneVar(x)
                ligne2.remove(x)                                
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
    
    grille = creation_des_variables(grille, variables)
    
    Lignes = lignes(grille)
    Colonnes = colonnes(grille)
    Carres = carres(grille)
    
    creation_des_contraintes(Lignes, contraintes, variables)
    creation_des_contraintes(Colonnes, contraintes, variables)
    creation_des_contraintes(Carres, contraintes, variables)
    
    #variables.consistanceDesNoeuds(contraintes.contraintes)
    #contraintes.consistanceDesArcs()

def solution_sudoku(grille):      
    contraintes = Contraintes()
    variables = Variables()
    
    if not grille_valide(grille) or not grille_de_vrai_sudoku(grille):
        raise Exception("La grille n'est pas valide")

    creation_de_toutes_les_contraintes(grille, contraintes, variables)
    
    sol = backtrack(0,contraintes.contraintes,variables.variables)
    
    if not sol == "echec":        
        for var in variables.variables:
                i = int(var.nom[4])
                j = int(var.nom[6])
                grille[i][j] = var.valeur
            
        print(grille)
    
    else :
        print("Ce sudoku n'a pas de solution")
    
grille1=[[1,"x",3,4],[1,"x",3,4],[1,"x",3,4],[1,"x",3,4]]
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


solution_sudoku(grille2)
solution_sudoku(grille1)


