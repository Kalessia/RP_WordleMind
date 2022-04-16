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

        assert self.maxGen > 0, "The maximum number of generations must be greater than 0."
        
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
        loop = True
        timeout = False
        while loop:
            oldPop = pop

            if self.verbose:
                print("\n--------------------------------------------------------------------------")
                print("\n>>> Generation n.", nbGen, " <<<\n")
                print("Population :", pop)

            pop = self.selectionOp(pop, self.popSize, popFitnesses, self.indiceKTournament, self.mu, self.lambda_)
            popFitnesses = self.computeFitness(pop)

            newESet = self.selectionESet(pop)
            eSet = self.addESet(eSet, newESet, maxSizeESet)
            if len(eSet) >= maxSizeESet:
                loop = False

            if self.verbose:
                print("\nOld population :", oldPop)
                print("New population :", pop)
                print("\neSet :", eSet)

            
            nbGen += 1
            if timeout == False and nbGen == self.maxGen and len(eSet) == 0:
                if self.verbose :
                    print("eSet is still empty... Extra time timer started to find a new word to play.")
                timeout = True
                tStart = time.time()

            if timeout == True:
                if len(eSet) > 0:
                    loop = False
                else:
                    t = time.time() - tStart 
                    if t >= self.maxTimeout:
                        if self.verbose : 
                            print("Extra time allowed to find a solution is finished. The procedure has failed.")
                            loop = False
            

        if len(eSet) > 0:
            nextTry = random.choice(eSet)
            return nextTry

        return None # fail


    #---------------------------------------------------------------------------

    def computeFitness(self, population):
        fitnesses = []

        for p in population:
            reward = tools.checkValidity(p)
            fitnesses.append(reward)
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

        # breakpoint1 must be situated before breakpoint2
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

    def kTournement(self, parents, parentsSize, parentsFitnesses, k, mu, lambda_):
        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[:k]
        
        for pr in priority:
            pop.append(parents[pr])

        for child in range(parentsSize):
            p1 = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p1)
            p2 = random.choice(pop_tmp)

            child1 = self.crossOp(p1, p2)
            child2 = self.mutationOp(child1, self.mutationRate)
            offspring.append(child2)

            if self.verbose:
                print("\nParent1 :", p1)
                print("Parent2 :", p2)
                print("\tCross effect :", child1)
                print("\tMutation effect :", child2)

        return offspring


    #---------------------------------------------------------------------------

    def uPlusLambdaSelection(self, parents, parentsSize, parentsFitnesses, k, mu, lambda_):

        assert (mu + lambda_) == len(parents), "Mu+Lambda must have size = population size"

        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[:mu]
        
        for pr in priority:
            pop.append(parents[pr])   # pop contains mu best elements

        for child in range(lambda_):
            p1 = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p1)
            p2 = random.choice(pop_tmp)

            child1 = self.crossOp(p1, p2)
            child2 = self.mutationOp(child1, self.mutationRate)
            offspring.append(child2)

            if self.verbose:
                print("\nParent1 :", p1)
                print("Parent2 :", p2)
                print("\tCross effect :", child1)
                print("\tMutation effect :", child2)

        offspring = [*pop, *offspring]
        return offspring


    #---------------------------------------------------------------------------
   
    def lambdaSelection(self, parents, parentsSize, parentsFitnesses, k, mu, lambda_):

        assert lambda_ == len(parents), "Lambda and population must have the same size"

        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[:mu]
        
        for pr in priority:
            pop.append(parents[pr])   # pop contains mu best elements

        for child in range(lambda_):
            p1 = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p1)
            p2 = random.choice(pop_tmp)

            child1 = self.crossOp(p1, p2)
            child2 = self.mutationOp(child1, self.mutationRate)
            offspring.append(child2)

            if self.verbose:
                print("\nParent1 :", p1)
                print("Parent2 :", p2)
                print("\tCross effect :", child1)
                print("\tMutation effect :", child2)

        return offspring

