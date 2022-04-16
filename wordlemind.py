
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

import tools
import analysis

import part2


#------------------------------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------------------------------

# general : set these variables to play with one of the proposed algorithms
wordLength = 4
filename = "dico.txt"
maxNbAttempts = 5
verbose = True                  # set 'True' to see a trace of the algorithm            default is False
plot = False                    # set 'True' to see a plot of the results               default is False


# part 2 : set these variables to play with the evolutionnary algorithm
popSize = 10                    # number of individuals in one population               default is 10
maxGen = 1                      # number of generations to run                          default is 1

crossOp = 1                     # crossover operation choice                            default is 1
                                #       1 = OnePointCrossover
                                #       2 = TwoPointsCrossover 

mutationOp = 1                  # mutation operation choice                             default is 1
                                #       1 = 
                                #       2 = 
mutationRate = 1                # mutation probability, value between [0,1]             default is 0.5

selectionOp = 1                 # selection operator choice                             default is 1
                                #       1 = 
                                #       2 = 
                                #       3 = 
indiceKTournament = 3           # number of selected best individuals in one generation. Default is 3
mu = 3                          # number of selected parents in one generation          default is 3
lambda_ = 3                     # number of generated childrens in one generation       default is 3

maxTimeout = 5000               # extra time allowed to find a valid word to play if the e.a. fails. Default is 300.000 ms = 5 minutes

maxSizeESet = 14                # maximal size of valid words to collect                default is 14




#------------------------------------------------------------------------------------------------------
#   WORDLE MIND game - play mode methods
#------------------------------------------------------------------------------------------------------

vocabulary = tools.getVocabFromFile(filename, wordLength)
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
    ea = part2.evolutionnaryAlgorithm(popSize, maxGen, crossOp, mutationOp, mutationRate, selectionOp, indiceKTournament, mu, lambda_, maxTimeout, verbose)

    nextTry = firstTry
    nbAttempt = 0
    while nbAttempt < maxNbAttempts and nextTry != secretWord:
        nbAttempt += 1

        if verbose :
            print(f"\nAttempt n.{nbAttempt} : played word is {nextTry}")

        nextTry = ea.findNextTry(nextTry, maxSizeESet)
        if nextTry == None:
            break
    
    if plot:
        analysis.plotResults()
    
    return getOutcome("part2_ea", nextTry, nbAttempt)


#------------------------------------------------------------------------------------------------------

def getOutcome(algo, finalPlayedWord, nbAttempt):
    
    if algo == "part2_ea":
        print(f"\nPlay Evolutionnary algorithm mode                                                                             \
            \n\tpopSize : {popSize}, \n\tmaxGen : {maxGen}, \n\tcrossOp : {crossOp}, \n\tmutationOp : {mutationOp},             \
            \n\tmutationRate : {mutationRate}, \n\tselectionOp : {selectionOp}, \n\tindiceKTournament : {indiceKTournament},    \
            \n\tmu : {mu}, \n\tlambda : {lambda_}, \n\tmaxTimeout : {maxTimeout}, \n\tmaxSizeESet : {maxSizeESet}")


    print(f"\n\nLast played word : {finalPlayedWord}, \tSecret word : {secretWord}")
    if finalPlayedWord == secretWord:
        print(f"Congratulations ! The correct word has been found in {nbAttempt} attempts")
    else:
        cptRightPos, cptBadPos = tools.cptCorrectsChars(finalPlayedWord, secretWord)
        print(f"Oooooops... The last played word has {cptRightPos} letters at the correct position and {cptBadPos} letters at a wrong position.")
        print("Next time will be a good one !")




#######################################################################################################
#   WORDLE MIND game - play : toogle line comment to play with your preferred algorithm
#######################################################################################################

#playA1
#playA2
playEvolutionnary()