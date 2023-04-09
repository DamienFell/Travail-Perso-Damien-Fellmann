from abc import ABC, abstractmethod
import copy
import math

class Variable :
    def __init__(self, nom, domaine, valeur = None):
        self.nom = nom
        self.domaine = domaine
        self.valeur = valeur
        self.label = []
        self.init_label()
    
    def init_label(self): #(Ré)Initialise le label
        self.label =copy.deepcopy(self.domaine)
        
    def enleve_du_label(self, d): #Efface la valeur d du label
        if d in self.label :
            self.label.remove(d)
            
    def met_a_jour_valeur(self, valeur) : 
        self.valeur = valeur
        
    def nom_est_egal(self, nom):
        return self.nom == nom
    
    def taille_du_domaine(self): # Retourne la taille du domaine
        return len(self.domaine)
    
    def taille_du_label(self): # Retourne la taille du label
        return len(self.label)
    
    def __repr__(self): 
        string =f"Variable(nom={self.nom}, domaine={self.domaine}, valeur={self.valeur}) "
        return string

class Contrainte(ABC):
    def __init__(self, variables):
        self.variables = variables 

    @abstractmethod    
    def dimension(self): 
        pass
    
    @abstractmethod
    def est_valide(self, var, val):
        pass
    
    @abstractmethod
    def __repr__(self): 
        pass
#Suite de la classe Contrainte
    def propage(self, var):
        for val in var.label :
            if not self.est_valide(var,val):
                var.label.remove(val)
                
        return len(var.label)>0
        
class Contrainte_unaire(Contrainte):
    def __init__(self, refVar, op, ref):
        Contrainte.__init__(self, [refVar])
        self.op = op 
        self.ref = ref 
        self.refVar = refVar 
    
    def dimension(self) :
        return 1 
    
    def est_valide(self, var, val):
        valeur = var.valeur  
        var.met_a_jour_valeur(val)
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
            
        var.met_a_jour_valeur(valeur) 
        
        return valide
    
    def __repr__(self) :
        string = f"Contrainte_unaire(refVar={self.refVar}, op={self.op}, ref={self.ref})"
        return string
            
class Contrainte_binaire(Contrainte):
    def __init__(self, refVar1, op, refVar2):
        Contrainte.__init__(self, [refVar1,refVar2])
        self.refVar1 = refVar1 
        self.op = op #
        self.refVar2 = refVar2 
        
    def dimension(self):
        return 2 
    
    def est_valide(self, var, val): 
        valeur = var.valeur 
        var.met_a_jour_valeur(val)
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
            
        var.met_a_jour_valeur(valeur) 
        
        return valide        

    def __repr__(self) :
        string = f"Contrainte_binaire(refVar1={self.refVar1}, op={self.op}, refVar2={self.refVar2})"
        return string

    def est_possible(self, var): #Détermine si la contrainte peut être satisfaite pour au moins une valeur du domaine
        if len(var.domaine) == 0:
            return False
        
        for d in var.domaine:
            if self.est_valide(var, d):
                return True #sSi au moins une valeur convient
        
        return False #Si aucune valeur ne convient
    
    def reviser(self):
        modifiee = False
        
        for paire in [[self.refVar1,self.refVar2],[self.refVar2,self.refVar1]]:
            for x in paire[0].domaine : #Test avec chaque valeur de la première variable
                paire[0].met_a_jour_valeur(x)
                
                if not self.est_possible(paire[1]): #Si la valeur ne peut pas satisfaire la contrainte, on l'enlève du domaine
                    paire[0].domaine.remove(x)
                    modifiee = True
            
            paire[0].met_a_jour_valeur(None)
        return modifiee

class Variables :
    def __init__(self):
        self.variables = []
        self.noms_variables = {}

    def ajoute_var(self, var):
        self.variables.append(var)
        self.noms_variables[var.nom] = var

    def retourne_var(self, nom): 
        try :
            return self.noms_variables[nom]
        except :
            return None
    
    def consistance_des_noeuds(self, contraintes): #Pour chaque contrainte unaire, on supprime des domaine des variable les valeurs qui ne respectent pas la contrainte
        for c in contraintes:
            if c.dimension() == 1:
                for val in c.refVar.domaine :
                    if not c.est_valide(c.refVar,val) :
                        c.refVar.domaine.remove(val)
  
    def retourne_nb_vars(self): #Retourne le nombre de variables
        return len(self.variables)
    
    def __repr__(self):
        str = "Vars : \n"
        for var in self.variables :
            str += "\t" + var.__repr__() + "\n"
        return str

class Contraintes :
    def __init__(self):
        self.contraintes = []
    
    def ajoute_contrainte(self, c): 
        self.contraintes.append(c)
    
    def consistance_des_arcs(self):
        refaire = False
        for c in self.contraintes:
            if c.dimension == 2 and c.reviser():
                refaire == True
        if refaire : #Si on peut peut-être encore supprimer des valeurs des domaines, on refait l'algorithme.
            self.consistance_des_arcs()
    
    def retourne_nb_contraintes(self) : #Retourne le nombre de contraintes
        return len(self.contraintes)
    
    def __repr__(self):
        str = "Contraintes : \n"
        for c in self.contraintes :
            str += "\t" + c.__repr__() + "\n"
        return str



def affiche_solution(algo, solution) :
    print(f"Solutions avec l'algorithme {algo} : {str(solution)}" )

def affiche_nb_iterations(algo, iterations):
    print(f"Nombre d'itérations avec l'algorithme {algo} : {str(iterations)}" )

def consistance_avec_vars_precedentes(k, contraintes, variables): 
    for c in contraintes :                                
        if variables[k] in c.variables:
            for i in range(0,k+1):
                if variables[i] in c.variables :
                    if c.est_valide(variables[k],variables[k].valeur):
                        break
                    else :
                        return False
    return True                        

def retourne_solution(variables):
    solution = {}
        
    for var in variables :
        solution[var.nom]=var.valeur
    
    return solution

def backtrack(k, contraintes, variables, iterations = 0):
    algo="bt"
    
    iterations +=1
    
    if k>=len(variables):
        return retourne_solution(variables)
    
    else :
        var = variables[k]
        
        for val in var.domaine: 
            var.met_a_jour_valeur(val)
            if consistance_avec_vars_precedentes(k, contraintes, variables):
                reste = backtrack(k+1, contraintes, variables, iterations)
                if reste != "echec":
                    return reste
    
    var.met_a_jour_valeur(None)
    return "echec"    

def propage_aux_vars_suivantes(k, contraintes, variables):
    for c in contraintes :
        for var in variables[k+1:]:
            if val in c.variables:
                if c.propage(val):
                    break
                else :
                    return False
    
    return True

def retourne_labels(k, variables):
    labels = {}
    
    for val in variables[k+1:]:
        labels[val] = copy.deepcopy(val.label)
    
    return labels

def met_a_jour_labels(k,variables, labels):
    for val in variables[k+1:]:
        val.label = copy.deepcopy(labels[val])

def forward_checking(k, contraintes, variables, iterations = 0):
    algo="fc"
    
    iterations +=1
    
    if k>=len(variables):
        return retourne_solution(variables)
    
    else :
        var = variables[k]
        anciens_labels = retourne_labels(k, variables)
        
        for val in var.label:
            var.met_a_jour_valeur(val)
            if propage_aux_vars_suivantes(k,contraintes, variables):
                reste = forward_checking(k+1, contraintes, variables, iterations)
                if reste != "echec":
                    return reste
                
            met_a_jour_labels(k, variables, anciens_labels)
    
    var.met_a_jour_valeur(None)
    return "echec"    
        
###############################################################################################################################################################


def grille_valide(grille):
    for ligne in grille :
        if not len(ligne) == len(grille):
            return False
    return True
    
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
                variables.ajoute_var(var)
                grille[i][j] = f"var({i},{j})"
    return grille


def creation_des_contraintes(grille, contraintes, variables):
    for ligne in grille :
        ligne2=ligne.copy()
        for x in ligne :
            if not type(x) is int :
                var = variables.retourne_var(x)
                ligne2.remove(x)                                
                for y in ligne2 :
                    if isinstance(y,int):
                        contrainte = Contrainte_unaire(var,"!=",y)
                        if not contrainte in contraintes.contraintes :
                            contraintes.ajoute_contrainte(contrainte)
                    else :
                        var2 = variables.retourne_var(y)
                        contrainte = Contrainte_binaire(var,"!=",var2)
                        if not contrainte in contraintes.contraintes :
                            contraintes.ajoute_contrainte(contrainte)        
                        
def creation_de_toutes_les_contraintes(grille, contraintes, variables):
    
    grille = creation_des_variables(grille, variables)
    
    Lignes = lignes(grille)
    Colonnes = colonnes(grille)
    Carres = carres(grille)
    
    creation_des_contraintes(Lignes, contraintes, variables)
    creation_des_contraintes(Colonnes, contraintes, variables)
    creation_des_contraintes(Carres, contraintes, variables)
    
    #variables.consistance_des_noeuds(contraintes.contraintes)
    #contraintes.consistance_des_arcs()

def solution_sudoku(grille):      
    contraintes = Contraintes()
    variables = Variables()
    
    if not grille_valide(grille) :
        raise Exception("La grille n'est pas valide")

    creation_de_toutes_les_contraintes(grille, contraintes, variables)
    
    sol = forward_checking(0,contraintes.contraintes,variables.variables)
    
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
#solution_sudoku(grille1)

x1 = Variable("x1", ["b","c"],"b")
x2 = Variable("x2", ["a","c"])
x3 = Variable("x3", ["b","c"])
x4 = Variable("x4", ["a","b"])

variables = Variables()
variables.ajoute_var(x1)
variables.ajoute_var(x2)
variables.ajoute_var(x3)
variables.ajoute_var(x4)

c12 = Contrainte_binaire(x1,"!=",x2)
c13 = Contrainte_binaire(x1,"!=",x3)
c14 = Contrainte_binaire(x1,"!=",x4)
c23 = Contrainte_binaire(x2,"!=",x3)
c24 = Contrainte_binaire(x2,"!=",x4)

contraintes = Contraintes()
contraintes.ajoute_contrainte(c12)
contraintes.ajoute_contrainte(c13)
contraintes.ajoute_contrainte(c14)
contraintes.ajoute_contrainte(c23)
contraintes.ajoute_contrainte(c24)

propage_aux_vars_suivantes(0, contraintes.contraintes, variables.variables)


sol = backtrack(0,contraintes.contraintes,variables.variables)
print(sol)