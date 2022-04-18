
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
import part2
import part3
import analysis



#------------------------------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------------------------------

# general : set these variables to play with one of the proposed algorithms
wordLength = 4
filename = "dico.txt"
maxNbAttempts = 20

nbIterations = 1                # number of iterations for one evaluation (used to compute mean values in statistics)
plot = False                    # set 'True' to see a plot of the results               default is False
plotfile = None                 # set a filename to save plots
debug = True                    # set 'True' to see a trace of the algorithm            default is False

# part 2 : set these variables to play with the evolutionnary algorithm
popSize = 20                    # number of individuals in one population               default is 10
maxGen = 50                     # number of generations to run                          default is 1

crossOp = 2                     # crossover operation choice                            default is 1
                                #       1 = OnePointCrossover
                                #       2 = TwoPointsCrossover 
crossRate = 0.5                 # crossover probability, value between [0,1]             default is 0.5

mutationOp = 1                  # mutation operation choice                             default is 1
                                #       1 = aleaCharMutation
                                #       2 = swapMutation
mutationRate = 0.5              # mutation probability, value between [0,1]             default is 0.5

selectionOp = 1                 # selection operator choice                             default is 1
                                #       1 = kTournament
                                #       2 = uPlusLambdaSelection
                                #       3 = lambdaSelection
indiceKTournament = 3           # number of selected best individuals in one generation. Default is 3
mu = 3                          # number of selected parents in one generation           default is 3
lambda_ = 12                    # number of generated childrens in one generation       default is 3

maxTimeout = 10                 # extra time allowed to find a valid word to play if the e.a. fails. Default is 300 s = 5 minutes

maxSizeESet = 5                 # maximal size of valid words to collect                default is 14




#------------------------------------------------------------------------------------------------------
#   WORDLE MIND game - play mode methods
#------------------------------------------------------------------------------------------------------

tools.getVocabFromFile(filename, wordLength)
secretWord = tools.getWord().lower()
firstTry = tools.getWord().lower()


def playEvolutionnary_part2():
    victory = False
    ea = part2.evolutionnaryAlgorithm(popSize, maxGen, crossOp, crossRate, mutationOp, mutationRate, selectionOp, indiceKTournament, mu, lambda_, maxTimeout, debug)

    nextTry = firstTry
    nbAttempt = 0
    while nbAttempt < maxNbAttempts and nextTry != None:
        nbAttempt += 1
        cptRightPos, cptBadPos = tools.cptCorrectsChars(nextTry, secretWord)

        if verbose:
            print("\n--------------------------------------------------------------------------")
            print(f"\nAttempt n.{nbAttempt} : played word is  *** {nextTry} ***     [debug] SECRET WORD : {secretWord}")
            print(f"Letters at the correct position : {cptRightPos}, letters at a wrong position : {cptBadPos}.")

        if cptRightPos == len(nextTry):
            victory = True
            break

        constraintsRules, forbiddenLetters = tools.buildConstraintsRules(nextTry, secretWord)
        nextTry = ea.findNextTry(nextTry, maxSizeESet)

        if debug:
            print(f"New constraints generated : {constraintsRules}")
            print(f"Forbidden letters : {forbiddenLetters}")


    if verbose:
        getOutcome(nextTry, nbAttempt)

    return victory, nbAttempt


#------------------------------------------------------------------------------------------------------

def playEvolutionnary_part3():
    victory = False
    ea = part3.evolutionnaryAlgorithm(popSize, maxGen, crossOp, crossRate, mutationOp, mutationRate, selectionOp, indiceKTournament, mu, lambda_, maxTimeout, debug)

    nextTry = firstTry
    nbAttempt = 0
    while nbAttempt < maxNbAttempts and nextTry != None:
        nbAttempt += 1
        cptRightPos, cptBadPos = tools.cptCorrectsChars(nextTry, secretWord)

        if verbose:
            print("\n--------------------------------------------------------------------------")
            print(f"\nAttempt n.{nbAttempt} : played word is  *** {nextTry} ***     [debug] SECRET WORD : {secretWord}")
            print(f"Letters at the correct position : {cptRightPos}, letters at a wrong position : {cptBadPos}.")

        if cptRightPos == len(nextTry):
            victory = True
            break

        constraintsRules, forbiddenLetters = tools.buildConstraintsRules(nextTry, secretWord)
        nextTry = ea.findNextTry(nextTry, maxSizeESet)

        if debug:
            print(f"New constraints generated : {constraintsRules}")
            print(f"Forbidden letters : {forbiddenLetters}")


    if verbose:
        getOutcome(nextTry, nbAttempt)

    return victory, nbAttempt


#------------------------------------------------------------------------------------------------------

def getOutcome(finalPlayedWord, nbAttempt):
    
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

def plotResults(algo, nomAlgo, nMin, nMax, nbIterations, plotfile = None):

    for n in range(nMin, nMax):
        global wordLength
        wordLength = n

        tmp_meanTime = []
        tmp_nbAttempts = []
        tab_n = []
        tab_meanTime = []
        tab_nbAttempts = []
        tabSuccesses = []
        cptVictories = 0

        for _ in range(nbIterations):
            tStart = time.time()
            victory, nbAttempt = algo()
            if victory:
                cptVictories += 1
                tmp_meanTime.append(time.time() - tStart)
                tmp_nbAttempts.append(nbAttempt)
        tab_n.append(n)
        tab_meanTime.append(np.mean(tmp_meanTime)) 
        tab_nbAttempts.append(np.mean(tmp_nbAttempts))
        tabSuccesses.append(round(cptVictories/nbIterations))

    analysis.plotMeanTime(tab_n, tab_meanTime, nbIterations, plotfile = nomAlgo)
    analysis.plotNbAttempts(tab_n, tmp_nbAttempts, nbIterations, plotfile = nomAlgo)
    
    analysis.plotSuccesses(tab_n, tabSuccesses, nbIterations, plotfile)

    print(">>>>" + nomAlgo)
    print("\ntab_n", tab_n, "\nmean_time", tab_meanTime, "\nmean_round", tmp_nbAttempts, "\nnbIterations", nbIterations)






#######################################################################################################
#   WORDLE MIND game - play : toogle line comments to play with your preferred algorithm
#######################################################################################################


if plot: # set global plot = 'True' to see a plot of the results
    nMin = 4
    nMax = 5
    debug = False
    verbose = False
    plotResults(playEvolutionnary_part2, "EA_part2", nMin, nMax, nbIterations, plotfile)
    #plotResults(playEvolutionnary_part3, "EA_part3", nMin, nMax, nbIterations, plotfile)

else:   # set global plot = 'False' to play a simple run 
    verbose = True                  # set 'True' to see a trace of the game actions
    playEvolutionnary_part2()
    #playEvolutionnary_part3()