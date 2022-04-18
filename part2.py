#######################################################################################################
#   Sorbonne université Master ANDROIDE 2021 - 2022
#   Projet de résolution de problèmes : satisfaction de contraintes pour le Wordle Mind 
# 
#                                           WORDLE MIND game
#
#                                     Alessia LOI, Antoine THOMAS
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


class evolutionnaryAlgorithm():

    def __init__(self, popSize = 10, maxGen = 1, crossOp = 1, crossRate = 0.5, mutationOp = 1,  mutationRate = 0.5, selectionOp = 1, indiceKTournament = 3, mu = 3, lambda_ = 3, maxTimeout = 300, debug = False):
        self.popSize = popSize
        self.maxGen = maxGen
        self.crossRate = crossRate
        self.mutationRate = mutationRate
        self.indiceKTournament = indiceKTournament
        self.mu = mu
        self.lambda_ = lambda_

        self.maxTimeout = maxTimeout    # default is 5 min = 300 seconds
        self.debug = debug

        
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
            self.selectionOp = self.kTournament
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
        offspring = [parent]

        while len(offspring) < taillePop:
            child = self.aleaCharMutation(parent, self.mutationRate)
            
            if child != parent and child not in offspring :
                offspring.append(child)

        return offspring


    #---------------------------------------------------------------------------

    def findNextTry(self, previousWord, maxSizeESet = 14):
        eSet = []
        pop = self.initPopulation(previousWord.lower(), self.popSize)
        popFitnesses = self.computeFitnesses(pop)
        newESet = self.selectionESet(pop)
        eSet = self.addESet(eSet, newESet, maxSizeESet)
        

        if  self.debug:
            print("\nFirst Generation Population :", pop)
            print("First Generation Fitnesses :", popFitnesses)
            print("\neSet :", eSet)


        nbGen = 1
        loop = True
        timeout = False
        while loop == True:
            pop = self.selectionOp(pop, self.popSize, popFitnesses, self.indiceKTournament, self.mu, self.lambda_, self.crossRate, self.mutationRate)
            popFitnesses = self.computeFitnesses(pop)

            newESet = self.selectionESet(pop)
            eSet = self.addESet(eSet, newESet, maxSizeESet)
            if len(eSet) >= maxSizeESet:
                loop = False

            if self.debug:
                print("\n--------------------------------------------------------------------------")
                print("\n>>> Generation n.", nbGen, " - timeout :", timeout, " <<<\n")
                print("\nNew population :", pop)
                print("New fitnesses :", popFitnesses)
                print("\neSet :", eSet)



            if timeout == False and nbGen == self.maxGen:
                if len(eSet) == 0:
                    timeout = True
                    tStart = time.time()
                    if self.debug :
                        print("\neSet is still empty... Extra time timer started to find a new word to play.")
                else:
                    loop = False

            if timeout == True:
                if len(eSet) > 0:
                    loop = False
                else:
                    t = time.time() - tStart 
                    if t >= self.maxTimeout:
                        loop = False
                        if self.debug : 
                            print("\nExtra time allowed to find a solution is finished. The procedure has failed.")

            nbGen += 1 


        if len(eSet) > 0:
            nextTry = random.choice(eSet)
            return nextTry

        return None # fail


    #---------------------------------------------------------------------------

    def computeFitnesses(self, population):
        
        fitnesses = []
        for p in population:
            reward = tools.getFitness_part2(p)
            fitnesses.append(reward)

        return fitnesses


    #---------------------------------------------------------------------------

    def selectionESet(self, population):
        
        candidateWords = []
        for p in population:
            if tools.respectsAllConstraints(p):
                candidateWords.append(p)

        return candidateWords
        

    #---------------------------------------------------------------------------

    def addESet(self, eSet, newESet, maxSizeESet):
        eSet = []
        for elem in newESet:
            if elem not in eSet:
                eSet.append(elem)

        if len(eSet) - maxSizeESet > 0:
            return eSet[:maxSizeESet]
        return eSet


    #---------------------------------------------------------------------------
    # Crossover operations
    #       - onePointCrossover : on the leftside of a random breakpoint child = parent1, on the rightside child = parent2
    #       - twoPointsCrossover : in the middle between two random breakpoints child = parent2, on the extrema sides child = parent1
    #---------------------------------------------------------------------------

    def onePointCrossover(self, parent1, parent2, crossRate):
        """ 
        """
        if len(parent1) < 2:
            return parent1
           
        child = parent1

        if random.random() <= crossRate:
            child = []
            breakpoint = random.randint(1, len(parent1)-1) # on exclut la 1ère case
            for i in range(len(parent1)):
                if i < breakpoint:
                    child.append(parent1[i])
                else:
                    child.append(parent2[i])
       
        return "".join(child)


#---------------------------------------------------------------------------

    def twoPointsCrossover(self, parent1, parent2, crossRate):

        if len(parent1) < 3:
            return parent1
        
        child = parent1

        if random.random() <= crossRate:
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

        alphabetDomain = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        child = list(originalWord)
       
        if random.random() <= mutationRate:
            pos = random.randint(0, len(child)-1)
            l = random.choice(alphabetDomain)
            while child[pos] == l or tools.isForbiddenLetter(l):
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

    def kTournament(self, parents, parentsSize, parentsFitnesses, k, mu, lambda_, crossRate, mutationRate):
        pop = []
        popFitnesses = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[::-1][:k]
        
        for pr in priority:
            pop.append(parents[pr])
            popFitnesses.append(parentsFitnesses[pr])


        while len(offspring) < parentsSize:
            p1 = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p1)
            p2 = random.choice(pop_tmp)

            child = self.crossOp(p1, p2, crossRate)
            child = self.mutationOp(child, mutationRate)
            child = tools.getNearestWord(child)
            if child not in offspring:
                offspring.append(child)

            # if self.debug:
            #     print("\nParent1 :", p1)
            #     print("Parent2 :", p2)
            #     print("\tCross effect :", child1)
            #     print("\tMutation effect :", child2)

        offFitnesses = self.computeFitnesses(offspring)

        allIndividuals = [*pop, *offspring]
        allFitnesses = [*popFitnesses, *offFitnesses ]

        priority = np.argsort(allFitnesses)[::-1][:parentsSize]
        
        offspring = []
        for pr in priority:
            offspring.append(allIndividuals[pr])

        return offspring


    #---------------------------------------------------------------------------

    def uPlusLambdaSelection(self, parents, parentsSize, parentsFitnesses, k, mu, lambda_, crossRate, mutationRate):

        assert (mu + lambda_) == len(parents), f"Mu+Lambda must have size = population size = {len(parents)}"

        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[::-1][:mu]
        
        for pr in priority:
            pop.append(parents[pr])   # pop contains mu best elements


        while len(offspring) < lambda_:
            p1 = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p1)
            p2 = random.choice(pop_tmp)

            child = self.crossOp(p1, p2, crossRate)
            child = self.mutationOp(child, mutationRate)
            child = tools.getNearestWord(child)
            if child not in offspring:
                offspring.append(child)

            # if self.debug:
            #     print("\nParent1 :", p1)
            #     print("Parent2 :", p2)
            #     print("\tCross effect :", child1)
            #     print("\tMutation effect :", child2)

        offspring = [*pop, *offspring]
        return offspring


    #---------------------------------------------------------------------------
   
    def lambdaSelection(self, parents, parentsSize, parentsFitnesses, k, mu, lambda_, crossRate, mutationRate):

        assert lambda_ == len(parents), f"Lambda and population must have the same size = {len(parents)}"

        pop = []
        offspring = []
        priority = np.argsort(parentsFitnesses)[::-1][:mu]
        
        for pr in priority:
            pop.append(parents[pr])   # pop contains the mu best parents


        while len(offspring) < lambda_:
            p1 = random.choice(pop)
            pop_tmp = copy.deepcopy(pop)
            pop_tmp.remove(p1)
            p2 = random.choice(pop_tmp)

            child = self.crossOp(p1, p2, crossRate)
            child = self.mutationOp(child, mutationRate)
            child = tools.getNearestWord(child)
            if child not in offspring:
                offspring.append(child)

            # if self.debug:
            #     print("\nParent1 :", p1)
            #     print("Parent2 :", p2)
            #     print("\tCross effect :", child1)
            #     print("\tMutation effect :", child2)

        return offspring

