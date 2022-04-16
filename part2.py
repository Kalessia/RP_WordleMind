#######################################################################################################
#   Sorbonne université Master ANDROIDE 2021 - 2022
#   Projet de résolution de problèmes : satisfaction de contraintes pour le Wordle Mind 
# 
#                                           WORDLE MIND game
#
#                                 Alessia LOI 3971668, Antoine THOMAS
#
#######################################################################################################



#------------------------------------------------------------------------------------------------------
#   Imports
#------------------------------------------------------------------------------------------------------

import random
import numpy as np
import copy
import time

import tools



#------------------------------------------------------------------------------------------------------
#   Evolutionnary algorithm
#------------------------------------------------------------------------------------------------------

random.seed(42)


class evolutionnaryAlgorithm():

    def __init__(self, popSize = 10, maxGen = 1, crossOp = 1, mutationOp = 1, mutationRate = 0.5, selectionOp = 1, indiceKTournament = 3, mu = 3, lambda_ = 3, maxTimeout = 300000, verbose = False):
        self.popSize = popSize
        self.maxGen = maxGen
        self.mutationRate = mutationRate
        self.indiceKTournament = indiceKTournament
        self.mu = mu
        self.lambda_ = lambda_

        self.maxTimeout = maxTimeout    # 5 min = 300.000 ms
        self.verbose = verbose

        if crossOp == 1:
            self.crossOp = self.onePointCrossover
        elif crossOp == 2:
            self.crossOp = self.twoPointsCrossover
        else:
            print("Crossover operator not found. Enter 1 (onePointCrossover) or 2 (twoPointsCrossover)")
            return
        

        if mutationOp == 1:
            self.mutationOp = self.aleaCharMutation
        elif mutationOp == 2:
            self.mutationOp = self.swapMutation
        else:
            print("Mutation operator not found. Enter 1 (aleaCharMutation) or 2 (swapMutation)")
            return


        if selectionOp == 1:
            self.selectionOp = self.kTournement
        elif selectionOp == 2:
            self.selectionOp = self.uPlusLambdaSelection
        elif selectionOp == 3:
            self.selectionOp = self.lambdaSelection
        else:
            print("Selection operator not found. Enter 1 (kTournment), 2 (uPlusLambdaSelection) or 3 (lambdaSelection)")
            return

        
    #---------------------------------------------------------------------------

    def initPopulation(self, firstWord, taillePop):
        """
        """
        parent = firstWord
        offspring = []

        while len(offspring) < taillePop:
            child = self.aleaCharMutation(parent, self.mutationRate)
            
            if child != parent and child not in offspring :
                offspring.append(child)

        return offspring


    #---------------------------------------------------------------------------

    def findNextTry(self, previousWord, maxSizeESet = 14):
        
        pop = self.initPopulation(previousWord.lower(), self.popSize)
        popFitnesses = self.computeFitness(pop)
        eSet = []

        if  self.verbose:
            print("\nFirst Generation Population :", pop)
            print("First Generation Fitnesses :", popFitnesses)

        nbGen = 0
        timeout = False
        while len(eSet) <= maxSizeESet and timeout:
            oldPop = pop

            if self.verbose:
                print("\n--------------------------------------------------------------------------")
                print("\n>>> Generation n.", nbGen, " <<<\n")
                print("Population :", pop)

            pop = self.selectionOp(pop, popFitnesses, self.indiceKTournament, self.mu, self.lambda_)
            popFitnesses = self.computeFitness(pop)

            newESet = self.selectionESet(pop)
            eSet = self.addESet(eSet, newESet, maxSizeESet)

            if self.verbose:
                print("\nOld population :", oldPop)
                print("New population :", pop)
                print("\neSet :", eSet)

            
            nbGen += 1

            if timeout == False and nbGen == self.maxGen and len(eSet) == 0:
                if self.verbose : 
                    print("Extra time timer started")
                timeout = True
                tStart = time.time()


            if timeout == True:
                if len(eSet) > 0:
                    timeout = False
                else:
                    t = time.time() - tStart 
                    if t >= self.maxTimeout:
                        if self.verbose : 
                            print("Extra time allowed to find a solution finished. Procedure failed.")
                        return None # fail
            

        nextTry = random.choice(eSet)
        return nextTry


    #---------------------------------------------------------------------------

    def computeFitness(self, population):
        fitnesses = []

        for p in population:
            fitnesses.append(14)
        return fitnesses


    #---------------------------------------------------------------------------

    def selectionESet(self, population):
        candidateWords = []
        
        for word in population:
            if tools.isWordValid(word):
                candidateWords.append(word)

        return candidateWords
        

    #---------------------------------------------------------------------------

    def addESet(self, eSet, newESet, maxSizeESet):
        eSet = [*eSet, *newESet]

        if len(eSet) - maxSizeESet > 0:
            return eSet[:maxSizeESet]
        return eSet


    #---------------------------------------------------------------------------
    # Crossover operations
    #       - onePointCrossover : on the leftside of a random breakpoint child = parent1, on the rightside child = parent2
    #       - twoPointsCrossover : 
    #---------------------------------------------------------------------------

    def onePointCrossover(self, parent1, parent2):
        """ 
        """
        if len(parent1) < 2:
            return parent1
           
        child = []
        breakpoint = random.randint(1, len(parent1)-1) # on exclut la 1ère case
        for i in range(len(parent1)):
            if i < breakpoint:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
       
        return "".join(child)


#---------------------------------------------------------------------------

    def twoPointsCrossover(self, parent1, parent2):

        if len(parent1) < 3:
            return parent1
        
        child = []
        breakpoint1 = 0
        breakpoint2 = 0

                         # On veut que le  pointCoupure1 précède le pointCoupure2 comme position
        while breakpoint2 <= breakpoint1:
            breakpoint1 = random.randint(1, len(parent1)-1) # on exclut la 1ère case
            breakpoint2 = random.randint(2, len(parent2)-1)
  
        for i in range(len(parent1)):
            if i < breakpoint1 or i >= breakpoint2:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
       
        return "".join(child)


    #---------------------------------------------------------------------------
    # Mutation operations
    #       - aleaCharMutation
    #       - swapMutation
    #---------------------------------------------------------------------------

    def aleaCharMutation(self, originalWord, mutationRate):
        """ 
        """
        alphabetDomain = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        child = list(originalWord)
       
        if random.random() <= mutationRate:
            pos = random.randint(0, len(child)-1)
            l = random.choice(alphabetDomain)
            while child[pos] == l:
                l = random.choice(alphabetDomain)
            child[pos] = l
       
        return "".join(child)
    
    
    #---------------------------------------------------------------------------

    def swapMutation(self, originalWord, mutationRate):

        if len(originalWord) < 2:
            return originalWord
       
        child = list(originalWord)
       
        if random.random() <= mutationRate:
            pos1 = random.randint(1, len(child)-1) # on exclut la 1ère case
            pos2 = random.randint(2, len(child)-1)

            while pos2 == pos1 or child[pos2] == child[pos1]:
                pos2 = random.randint(0, len(child)-1)

            tmp = child[pos1]
            child[pos1] = child[pos2]
            child[pos2] = tmp

        return "".join(child)


    #---------------------------------------------------------------------------
    # Selection operations:
    #       - kTournement : select k best individuals in the population
    #       - plusélection (u+l) : select u best parents and generate l childrens, pop = u+l individuals (parents + offspring)
    #       - comma-sélection (u,l) : select u best parents and generate l childrens, pop = l individuals (offspring only)
    #---------------------------------------------------------------------------

    def kTournement(self, parents, parentsFitnesses, k, mu, lambda_):
        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[:k]
        
        for pr in priority:
            pop.append(parents[pr])

        for p in pop:
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p)
            p2 = random.choice(pop_tmp)

            child1 = self.crossOp(p, p2)
            child2 = self.mutationOp(child1, self.mutationRate)
            offspring.append(child2)

            if self.verbose:
                print("\nParent1 :", p)
                print("Parent2 :", p2)
                print("\tCross effect :", child1)
                print("\tMutation effect :", child2)

        return offspring


    #---------------------------------------------------------------------------

    def uPlusLambdaSelection(self, parents, parentsFitnesses, k, mu, lambda_):

        assert (mu + lambda_) == len(parents), "Mu+Lambda must have size = population size"

        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[:mu]
        
        for pr in priority:
            pop.append(parents[pr])   # pop contains mu best elements

        for p in range(lambda_):
            p = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p)
            p2 = random.choice(pop_tmp)

            child1 = self.crossOp(p, p2)
            child2 = self.mutationOp(child1, self.mutationRate)
            offspring.append(child2)

            if self.verbose:
                print("\nParent1 :", p)
                print("Parent2 :", p2)
                print("\tCross effect :", child1)
                print("\tMutation effect :", child2)

        offspring = [*pop, *offspring]
        return offspring


    #---------------------------------------------------------------------------
   
    def lambdaSelection(self, parents, parentsFitnesses, k, mu, lambda_):

        assert lambda_ == len(parents), "Lambda and population must have the same size"

        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[:mu]
        
        for pr in priority:
            pop.append(parents[pr])   # pop contains mu best elements

        for p in range(lambda_):
            p = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p)
            p2 = random.choice(pop_tmp)

            child1 = self.crossOp(p, p2)
            child2 = self.mutationOp(child1, self.mutationRate)
            offspring.append(child2)

            if self.verbose:
                print("\nParent1 :", p)
                print("Parent2 :", p2)
                print("\tCross effect :", child1)
                print("\tMutation effect :", child2)

        return offspring


    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------








       
  


 
#     def kTournement(populationCourante, tabFitness, nbIndAEcarter):
#         """ populationCourante : liste de jeux de paramètres [param1, ... , paramN]
#             tabFitness : liste des fitness rélatives à chaque jeu de paramètres
#             nbIndAEcarter : nombre de individus à exclure dans la population résultante
#         """
       
#         if len(populationCourante) <= nbIndAEcarter:
#             nbIndAEcarter = len(populationCourante) - 1 # newPopulation contiendra un seul individu au dernier tournoi

#         borneMaximale = 10000000

#         newPopulation = list(populationCourante)
#         tabFitness_copy = list(tabFitness)
   
#         for i in range(nbIndAEcarter):          
#             minFitness = min(tabFitness_copy)
#             indiceMinFitness = [r for r, j in enumerate(tabFitness_copy) if j == minFitness]
#             tabFitness_copy[indiceMinFitness[0]] = borneMaximale
#             del newPopulation[indiceMinFitness[0]]
           
#         return newPopulation
 
#     #---------------------------------------------------------------------------
 
#     def plusSelection(tabParents, tabFitness, u, l, Y, opVar):
#         """ tabParents (populationCourante) : liste de jeux de paramètres [param1, ... , paramN]
#             tabFitness : liste des fitness rélatives à chaque jeu de paramètres
#             u : nombre de meilleurs parents constituant la population résultante
#             l : nombre d'childs constituant la population résultante
#             Y : espace de recherche
#             opVar : operateur de variation à appliquer pour la génération des childs
#         """
       
#         if u >= len(tabParents) or u+l != len(tabParents) :
#             return tabParents
       
#         newPopulation = []
#         tabFitness_copy = list(tabFitness)
               
#         # Sélection des meilleurs parents u
#         tabBestU = []
#         for i in range(u):
#             maxFitness = max(tabFitness_copy)
#             indiceMaxFitness = [r for r, j in enumerate(tabFitness_copy) if j == maxFitness]
#             tabBestU.append(tabParents[indiceMaxFitness[0]])
#             tabFitness_copy[indiceMaxFitness[0]] = 0
#         newPopulation = list(tabBestU)
       
#         # Ajout des childs générés à partir des meilleurs parents u
#         for i in range(l):
#             tabBestU_copy = list(tabBestU)
#             parent1 = random.choice(tabBestU_copy)
#             tabBestU_copy.remove(parent1)
#             if len(tabBestU_copy) > 0:
#                 parent2 = random.choice(tabBestU_copy)
#             else:
#                 parent2 = list(parent1)
#             newchild = f_operateurVariation(opVar, parent1, parent2, Y)
#             newPopulation.append(newchild)
           
#         return newPopulation
       
#     #---------------------------------------------------------------------------
   
#     def commaSelection(tabParents, tabFitness, u, l, Y, opVar):
#         """ tabParents (populationCourante) : liste de jeux de paramètres [param1, ... , paramN]
#             tabFitness : liste des fitness rélatives à chaque jeu de paramètres
#             u : nombre de meilleurs parents générant la population résultante
#             l : nombre d'childs constituant la population résultante
#             Y : espace de recherche
#             opVar : operateur de variation à appliquer pour la génération des childs
#         """
       
#         if u >= len(tabParents) or l != len(tabParents) or len(tabParents) == 1:
#             return tabParents
       
#         newPopulation = []
#         tabFitness_copy = list(tabFitness)
               
#         # Sélection des meilleurs parents u
#         tabBestU = []
#         for i in range(u):
#             maxFitness = max(tabFitness_copy)
#             indiceMaxFitness = [r for r, j in enumerate(tabFitness_copy) if j == maxFitness]
#             tabBestU.append(tabParents[indiceMaxFitness[0]])
#             del tabFitness_copy[indiceMaxFitness[0]]
       
#         # Sélection des childs générés à partir des meilleurs parents u            
#         for i in range(l):
#             tabBestU_copy = list(tabBestU)
#             parent1 = random.choice(tabBestU_copy)
#             tabBestU_copy.remove(parent1)
#             if len(tabBestU_copy) > 0:
#                 parent2 = random.choice(tabBestU_copy)
#             else:
#                 parent2 = list(parent1)
#             newchild = f_operateurVariation(opVar, parent1, parent2, Y)
#             newPopulation.append(newchild)
           
#         return newPopulation
           
   


   

#     ############################################################################
#     #   Représentation graphique des résultats
#     ############################################################################

#     def plotResults(evalCourante, bestFitness, nomFichier):
#         x = evalCourante # abscisses : evaluations
#         y = bestFitness # ordonnées : performance
       
#         plt.figure()
#         plt.suptitle("Fin optimisation ! Evolution des solutions candidates", color = 'red')
#         texte = "bestParam optimisé = " + "".join(str(bestParam))
#         plt.title(texte)
#         plt.xlabel("Evaluations")
#         plt.ylabel("Fitness")
#         plt.scatter(x, y, marker='o', color='red')
#         plt.show()

#         # Sauvegarde du tracé
#         if nomFichier != None:
#             plt.savefig(nomFichier, transparent = True)


