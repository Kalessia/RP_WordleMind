
#######################################################################################################
#   Sorbonne université Master ANDROIDE 2021 - 2022
#   Projet de résolution de problèmes : satisfaction de contraintes pour le Wordle Mind 
# 
#                                           WORDLE MIND game
#
#                                   Alessia LOI 3971668, Antoine THOMAS
#
#######################################################################################################




#------------------------------------------------------------------------------------------------------
#   Imports
#------------------------------------------------------------------------------------------------------

import numpy as np
import time

import tools
import analysis
import part2


#------------------------------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------------------------------

# general : set these variables to play with one of the proposed algorithms
wordLength = 4
filename = "dico.txt"
maxNbAttempts = 10
verbose = True                  # set 'True' to see a trace of the algorithm            default is False
plot = False                    # set 'True' to see a plot of the results               default is False


# part 2 : set these variables to play with the evolutionnary algorithm
popSize = 30                    # number of individuals in one population               default is 10
maxGen = 20                     # number of generations to run                          default is 1

crossOp = 1                     # crossover operation choice                            default is 1
                                #       1 = OnePointCrossover
                                #       2 = TwoPointsCrossover 

mutationOp = 1                  # mutation operation choice                             default is 1
                                #       1 = aleaCharMutation
                                #       2 = swapMutation
mutationRate = 1                # mutation probability, value between [0,1]             default is 0.5

selectionOp = 2                 # selection operator choice                             default is 1
                                #       1 = kTournament
                                #       2 = uPlusLambdaSelection
                                #       3 = lambdaSelection
indiceKTournament = 5           # number of selected best individuals in one generation. Default is 3
mu = 5                          # number of selected parents in one generation          default is 3
lambda_ = 25                    # number of generated childrens in one generation       default is 3

maxTimeout = 10                 # extra time allowed to find a valid word to play if the e.a. fails. Default is 300 s = 5 minutes

maxSizeESet = 5                 # maximal size of valid words to collect                default is 14




#------------------------------------------------------------------------------------------------------
#   WORDLE MIND game - play mode methods
#------------------------------------------------------------------------------------------------------

tools.getVocabFromFile(filename, wordLength)
secretWord = tools.getWord().lower()
firstTry = tools.getWord().lower()



#------------------------------------------------------------------------------------------------------

def playA1():
    return
    #return getOutcome("part1_a1", nextTry, nbAttempt)


#------------------------------------------------------------------------------------------------------

def playA2():
    return
    #return getOutcome("part1_a2", nextTry, nbAttempt)


#------------------------------------------------------------------------------------------------------

def playEvolutionnary():
    victory = False
    ea = part2.evolutionnaryAlgorithm(popSize, maxGen, crossOp, mutationOp, mutationRate, selectionOp, indiceKTournament, mu, lambda_, maxTimeout, verbose)

    nextTry = firstTry
    nbAttempt = 0
    while nbAttempt < maxNbAttempts and nextTry != None:
        nbAttempt += 1
        cptRightPos, cptBadPos = tools.cptCorrectsChars(nextTry, secretWord)

        print("\n--------------------------------------------------------------------------")
        print(f"\nAttempt n.{nbAttempt} : played word is  *** {nextTry} ***     [debug] SECRET WORD : {secretWord}")
        print(f"Letters at the correct position : {cptRightPos}, letters at a wrong position : {cptBadPos}.")

        if cptRightPos == len(nextTry):
            victory = True
            break

        contraintsRules = tools.buildConstraintsRules(nextTry, secretWord)
        nextTry = ea.findNextTry(nextTry, maxSizeESet)

        if verbose:
            print(f"New constraints generated : {contraintsRules}")


    if verbose:
        getOutcome("part2_ea", nextTry, nbAttempt)

    return victory, nbAttempt


#------------------------------------------------------------------------------------------------------

def getOutcome(algo, finalPlayedWord, nbAttempt):
    
    if algo == "part2_ea":
        print(f"\nPlay Evolutionnary algorithm mode                                                                             \
            \n\tpopSize : {popSize}, \n\tmaxGen : {maxGen}, \n\tcrossOp : {crossOp}, \n\tmutationOp : {mutationOp},             \
            \n\tmutationRate : {mutationRate}, \n\tselectionOp : {selectionOp}, \n\tindiceKTournament : {indiceKTournament},    \
            \n\tmu : {mu}, \n\tlambda : {lambda_}, \n\tmaxTimeout : {maxTimeout}, \n\tmaxSizeESet : {maxSizeESet}")


    print(f"\n\nLast played word : {finalPlayedWord} \tSecret word : {secretWord}")
    if finalPlayedWord == secretWord:
        print(f"Congratulations ! The correct word has been found in {nbAttempt} attempts")
    elif finalPlayedWord == None:
        print(f"Game over : the algorithm hasn't found a new valid word to play...")
    else:
        cptRightPos, cptBadPos = tools.cptCorrectsChars(finalPlayedWord, secretWord)
        print(f"Oooooops... The last played word has {cptRightPos} letters at the correct position and {cptBadPos} letters at a wrong position.")
        print("Next time will be a good one !")


#------------------------------------------------------------------------------------------------------

def plotResults(algo, nMin, nMax, nbIterations, filename = None):

    for n in range(nMin, nMax):
        global wordLength
        wordLength = n

        tmp_meanTime = []
        tmp_nbAttempts = []
        tab_n = []
        tab_meanTime = []
        tab_nbAttempts = []

        for _ in range(nbIterations):
            tStart = time.time()
            _, nbAttempt = algo()
            tmp_meanTime.append(time.time() - tStart)
            tmp_nbAttempts.append(nbAttempt)
        tab_n.append(n)
        tab_meanTime.append(np.mean(tmp_meanTime)) 
        tab_nbAttempts.append(np.mean(tmp_nbAttempts))

    analysis.plotResults(tab_n, tab_meanTime, tab_nbAttempts, filename = filename)




#######################################################################################################
#   WORDLE MIND game - play : toogle line comments to play with your preferred algorithm
#######################################################################################################


if plot: # set global plot = 'True' to see a plot of the results
    nMin = 4
    nMax = 5
    nbIterations = 1
    filename = None
    verbose = False

    #plotResults(playA1, nMin, nMax)
    #plotResults(playA2, nMin, nMax)
    plotResults(playEvolutionnary, nMin, nMax, nbIterations, filename)

else:
    #playA1
    #playA2
    playEvolutionnary()