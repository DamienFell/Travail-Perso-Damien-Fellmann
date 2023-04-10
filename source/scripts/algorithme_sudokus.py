from abc import ABC, abstractmethod
import copy
import math

class Variable :
    def __init__(self, nom, domaine, valeur = None):
        self.nom = nom
        self.domaine = domaine
        self.valeur = valeur
        self.label =copy.deepcopy(self.domaine)
        
    def met_a_jour_valeur(self, val) : 
        self.valeur = val

    def enleve_du_label(self, val)
        if d in self.label :
            self.label.remove(val)
                
    def __repr__(self): 
        string =f"Variable(nom={self.nom}, domaine={self.domaine}, valeur={self.valeur})"
        return string

class Contrainte(ABC):
    def __init__(self, variables):
        self.variables = variables
        self.dimension = 0
    
    @abstractmethod
    def est_valide(self, var, val):
        pass
    
    @abstractmethod
    def __repr__(self): 
        pass
    
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
        self.dimension = 1
    
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
        self.op = op 
        self.refVar2 = refVar2
        self.dimension = 2
        
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

class PSC :
    def __init__(self):
        self.variables = []
        self.noms_variables = {}
        self.contraintes_binaires = []
        self.contraintes_unaires = []

    def ajoute_var(self, var):
        self.variables.append(var)
        self.noms_variables[var.nom] = var

    def retourne_var(self, nom): 
        try :
            return self.noms_variables[nom]
        except :
            return None
    
    def __repr__(self):
        str = "Variables : \n"
        for var in self.variables :
            str += var.__repr__() + "\n"
        str += "Contraintes : \n"
        for c in self.contraintes_unaires :
            str += c.__repr__() + "\n"
        for c in self.contraintes_binaires :
            str += c.__repr__() + "\n"
        return str
#Suite de la classe PSC        
    def consistance_contraintes_unaires(self):
        for c in self.contraintes_unaires:
            for val in c.refVar.label :
                if not c.est_valide(c.refVar,val) :
                    c.refVar.label.remove(val)
    
    def consistance_des_arcs(self):
        refaire = False
        for c in self.contraintes:
            if c.dimension == 2 and c.reviser():
                refaire == True
        if refaire : #Si on peut peut-être encore supprimer des valeurs des domaines, on refait l'algorithme.
            self.consistance_des_arcs()
#Suite de la classe PSC 
    def consistance_avec_vars_precedentes(self, k): 
        for c in contraintes_binaires :                                
            if self.variables[k] in c.variables:
                for i in range(0,k+1):
                    if self.variables[i] in c.variables :
                        if c.est_valide(self.variables[k],self.variables[k].valeur):
                            break
                        else :
                            return False
        return True                        

    def retourne_solution(self):
        solution = {}
            
        for var in self.variables :
            solution[var.nom]=var.valeur
        
        return solution

    def backtrack(self, k, iterations = 0):
        algo="bt"
        
        iterations +=1
        
        if k>=len(self.variables):
            return self.retourne_solution()
        
        else :
            var = self.variables[k]
            
            for val in var.domaine: 
                var.met_a_jour_valeur(val)
                if self.consistance_avec_vars_precedentes(k):
                    reste = self.backtrack(k+1, iterations)
                    if reste != "echec":
                        return reste
        
        var.met_a_jour_valeur(None)
        return "echec"    
#Suite de la classe PSC 
    def propagation_aux_vars_suivantes(self, k):
        for c in self.contraintes_binaires :
            for var in self.variables[k+1:]:
                if var in c.variables:
                    if c.propage(var):
                        break
                    else :
                        return False
        
        return True

    def retourne_labels(self, k):
        labels = {}
        
        for var in self.variables[k+1:]:
            labels[var] = copy.deepcopy(var.label)
        
        return labels

    def met_a_jour_labels(self, k, labels):
        for var in self.variables[k+1:]:
            var.label = copy.deepcopy(labels[var])

    def forward_checking(self, k, iterations = 0):
        algo="fc"
        
        iterations +=1
        
        if k>=len(self.variables):
            return self.retourne_solution()
        
        else :
            var = self.variables[k]
            anciens_labels = self.retourne_labels(k)
            
            for val in var.label:
                var.met_a_jour_valeur(val)
                if self.propagation_aux_vars_suivantes(k):
                    reste = self.forward_checking(k+1, iterations)
                    if reste != "echec":
                        return reste
                    
                self.met_a_jour_labels(k, anciens_labels)
        
        var.met_a_jour_valeur(None)
        return "echec"    
        
###############################################################################################################################################################

class Sudokus_PSC(PSC):
    
    def __init__(self, grille):
        PSC.__init__(self)
        self.grille = grille
#Suite de la classe Sudokus_PS    
    def grille_valide(self):
        for ligne in self.grille :
            if not len(ligne) == len(self.grille):
                return False
        return True
#Suite de la classe Sudokus_PSC    
    def lignes(self):
        return self.grille

    def colonnes(self):
        result = []
        for i in range(len(self.grille)):
            colonne = []
            for j in range(len(self.grille)):
                colonne.append(self.grille[j][i])
            result.append(colonne)
        return result

    def carres(self):
        result = []
        taille_carre = int(math.sqrt(len(self.grille)))
        for i in range(taille_carre):
            for j in range(taille_carre):
                carre = []
                for k in range(taille_carre):
                    for l in range(taille_carre):
                        carre.append(self.grille[taille_carre*i+k][taille_carre*j+l])
                result.append(carre)
        return result
#Suite de la classe Sudokus_PSC
    def creation_des_variables(self):
        domaine = list(range(1,len(self.grille)+1))
        for i in range(len(self.grille)) :
            for j in range(len(self.grille)) :
                if self.grille[i][j] == "x":
                    var = Variable(f"var({i},{j})",domaine)
                    self.ajoute_var(var)
                    self.grille[i][j] = f"var({i},{j})"
#Suite de la classe Sudokus_PSC
    def creation_des_contraintes(self, grille):
        for ligne in grille :
            ligne2=ligne.copy()
            for x in ligne :
                if not type(x) is int :
                    var = self.retourne_var(x)
                    ligne2.remove(x)                                
                    for y in ligne2 :
                        if isinstance(y,int):
                            c = Contrainte_unaire(var,"!=",y)
                            if not c in self.contraintes_unaires :
                                self.contraintes_unaires.append(c)
                        else :
                            var2 = self.retourne_var(y)
                            c = Contrainte_binaire(var,"!=",var2)
                            if not c in self.contraintes_binaires :
                                self.contraintes_binaires.append(c)
#Suite de la classe Sudokus_PSC                        
    def creation_de_toutes_les_contraintes(self):
        self.creation_des_variables()
        
        lignes = self.lignes()
        colonnes = self.colonnes()
        carres = self.carres()
        
        self.creation_des_contraintes(lignes)
        self.creation_des_contraintes(colonnes)
        self.creation_des_contraintes(carres)
        
    def solution_sudoku(self):
        
        if not self.grille_valide() :
            raise Exception("La grille n'est pas valide")

        self.creation_de_toutes_les_contraintes()
        
        self.consistance_contraintes_unaires()
        
        sol = self.forward_checking(0) # ou self.backward(0) 
        
        if not sol == "echec":        
            for var in self.variables:
                    i = int(var.nom[4])
                    j = int(var.nom[6])
                    self.grille[i][j] = var.valeur
                
            print(self.grille)
        
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


psc2 = Sudokus_PSC(grille2)
psc2.solution_sudoku()
#solution_sudoku(grille1)
