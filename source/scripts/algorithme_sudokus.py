from abc import ABC, abstractmethod
import copy
import math
from timeit import default_timer as timer
class Variable :
    def __init__(self, nom, domaine, valeur = None):
        self.nom = nom
        self.domaine = domaine
        self.valeur = valeur
        self.label =copy.deepcopy(self.domaine)
        
    def met_a_jour_valeur(self, val) : 
        self.valeur = val

    def enleve_du_label(self, val):
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
#Suite de la classe Contrainte_binaire
    def est_possible(self, var): 
        if len(var.label) == 0:
            return False
        
        for val in var.label:
            if self.est_valide(var, val):
                return True 
        
        return False 
    
    def modifier_labels(self):
        modification = False
        
        for paire in [[self.refVar1,self.refVar2],[self.refVar2,self.refVar1]]:
            for val in paire[0].label :
                paire[0].met_a_jour_valeur(val)
                
                if not self.est_possible(paire[1]): 
                    paire[0].label.remove(val)
                    modifiee = True
            
            paire[0].met_a_jour_valeur(None)
        
        return modification
class PSC :
    def __init__(self):
        self.variables = []
        self.noms_variables = {}
        self.contraintes_binaires = []
        self.contraintes_unaires = []
        self.iterations = 0

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
    def consistance_noeuds(self):
        for c in self.contraintes_unaires:
            for val in c.refVar.label :
                if not c.est_valide(c.refVar,val) :
                    c.refVar.label.remove(val)
#Suite de la classe PSC     
    def consistance_arcs(self):
        refaire = False
        for c in self.contraintes_binaires:
            if c.modifier_labels():
                refaire == True
        if refaire : 
            self.consistance_arcs()
#Suite de la classe PSC
    def sort_variables(self):
        self.variables.sort(key=lambda var : len(var.label))
#Suite de la classe PSC
    def dynamic_ordering(self,k):
        indice_plus_petit_label = k
        taille_min = len(self.variables[k].label)
        
        for i in range(k+1,len(self.variables)):
            if len(self.variables[i].label)<taille_min:
                indice_plus_petit_label = i
                taille_min = len(self.variables[i].label)
                
        if indice_plus_petit_label != k:
            self.variables[k], self.variables[indice_plus_petit_label] = \
            self.variables[indice_plus_petit_label], self.variables[k]
                       
#Suite de la classe PSC 
    def consistance_avec_vars_precedentes(self, k): 
        for c in self.contraintes_binaires :                                
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

    def backtrack(self, k):
        self.iterations +=1
        
        if k>=len(self.variables):
            return self.retourne_solution()
        
        else :
            var = self.variables[k]
            
            for val in var.label: 
                var.met_a_jour_valeur(val)
                if self.consistance_avec_vars_precedentes(k):
                    reste = self.backtrack(k+1)
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

    def forward_checking(self, k):       
        self.iterations +=1
        
        if k>=len(self.variables):
            return self.retourne_solution()
        
        else :
            var = self.variables[k]
            anciens_labels = self.retourne_labels(k)
            
            for val in var.label:
                var.met_a_jour_valeur(val)
                if self.propagation_aux_vars_suivantes(k):
                    if k < len(self.variables)-1:
                        self.dynamic_ordering(k+1)
                    reste = self.forward_checking(k+1)
                    if reste != "echec":
                        return reste
                    
                self.met_a_jour_labels(k, anciens_labels)
        
        var.met_a_jour_valeur(None)
        return "echec"    



###############################################################################################################################################################

class Sudokus_PSC(PSC):
    
    def __init__(self, grille):
        PSC.__init__(self)
        self.grille = copy.deepcopy(grille)
        
        if not self.grille_valide() :
            raise Exception("La grille n'est pas valide")
        
        self.creation_de_toutes_les_contraintes()
        
        self.consistance_noeuds()
        
        self.consistance_arcs()
        
        self.sort_variables()

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
                if self.grille[i][j] == ".":
                    var = Variable(f"var({i},{j})",domaine)
                    self.ajoute_var(var)
                    self.grille[i][j] = f"var({i},{j})"
#Suite de la classe Sudokus_PSC
    def creation_des_contraintes(self, grille):
        for ligne in grille :
            ligne2=ligne.copy()
            for x in ligne :
                if not isinstance(x,int) :
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
        
    def solution_sudoku(self,algo,show = True):
        sol = algo(0)
        
        if show :
            if not sol == "echec":        
                for var in self.variables:
                        i = int(var.nom[4])
                        j = int(var.nom[6])
                        self.grille[i][j] = var.valeur
                    
                print(self.grille)
            
            else :
                print("Ce sudoku n'a pas de solution")

def lines_to_sudokus(lines):
    sudokus_grids = int(len(lines)/11) * [None] #Création de la liste contenant
                                                #toutes les grilles
    for i in range(int(len(lines)/11)):         #11 car il y a entre chaque grille
        grid =9*[None]                          #deux retours à la ligne,
        for j in range(9):
            grid[j]=list(lines[11*i+j])[:9]     #[:9] car le dernier caractère de
            for k in range(9):                  #chaque ligne est un "\n".
                el = grid[j][k]                 
                if el != ".":                   
                    grid[j][k] = int(el)
            
        sudokus_grids[i]=grid
    
    return sudokus_grids

def chronometre(lines):
    grids = lines_to_sudokus(lines)
    
    for grid in grids:
        
        psc = Sudokus_PSC(grid)
        start = timer()
        psc.solution_sudoku(psc.forward_checking,False)
        end = timer()
        
        print(f"{end-start};{psc.iterations}")
     
    print("-------------------------------------------------------------") 
     
    for grid in grids:
        
        psc = Sudokus_PSC(grid)
        start = timer()
        psc.solution_sudoku(psc.backtrack,False)
        end = timer()
        
        print(f"{end-start};{psc.iterations}")

file = open("sudokus.txt", "r")

lines = file.readlines()

file.close()

chronometre(lines)


psc = Sudokus_PSC(grille2)
psc.solution_sudoku(psc.forward_checking)