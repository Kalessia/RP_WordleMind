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


#------------------------------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------------------------------

vocabulary = None
forbiddenLetters = []
alreadyPlayed = []
constraints = []            # collects informations about the previous attempts

historyTot = 0
cptGen = 0


#------------------------------------------------------------------------------------------------------
#   Tools
#------------------------------------------------------------------------------------------------------

def getVocabFromFile(filename, wordSize):
    wordsList = []
    vocabulary_tmp = []
    with open(filename, "r") as f:
        wordsList = f.read().split("\n")

    for word in wordsList :
        if len(word) == wordSize:
            vocabulary_tmp.append(word.lower())
    
    global vocabulary
    vocabulary = vocabulary_tmp


#---------------------------------------------------------------------------------------------------------------

def getWord():
    return random.choice(vocabulary)


#---------------------------------------------------------------------------------------------------------------

def cptCorrectsChars(word, secretWord):
    cptRightPos = 0
    cptBadPos = 0

    word_check = list(word)
    secretWord_check = list(secretWord)
    
    tmp = []
    for pos in range(len(word_check)):
        if word_check[pos] == secretWord_check[pos]:
            cptRightPos += 1
            tmp.append(word_check[pos])
    
    if len(tmp) > 0:
        for pos in tmp:
            word_check.remove(pos)
            secretWord_check.remove(pos)

    for letter in word_check:
        if letter in secretWord_check:
            cptBadPos += 1
            secretWord_check.remove(letter)

    return cptRightPos, cptBadPos

    
#---------------------------------------------------------------------------------------------------------------

def buildConstraintsRules(word, secretWord):
    
    global alreadyPlayed
    alreadyPlayed.append(word)

    cptRightPos, cptBadPos = cptCorrectsChars(word, secretWord)

    global constraints
    if cptRightPos + cptBadPos > 0:
        constraints.append([word, cptRightPos, cptBadPos])
    else:
        for letter in word:
            if not isForbiddenLetter(letter):
                forbiddenLetters.append(letter)
    
    return constraints, forbiddenLetters


#---------------------------------------------------------------------------------------------------------------

def isForbiddenLetter(letter):
    if letter in forbiddenLetters:
        return True
    return False


#---------------------------------------------------------------------------------------------------------------

def respectsAllConstraints(word):

    if word in alreadyPlayed:
        return False

    if word not in vocabulary:
        return False

    for letter in word:
        if letter in forbiddenLetters:
            return False

    for letters, rp, bp in constraints:
        cptRightPos, cptBadPos = cptCorrectsChars(word, letters)
        
        if cptRightPos != rp or cptBadPos != bp:
            return False
    
    return True


#---------------------------------------------------------------------------------------------------------------

def getNearestWord(word):
    nearestWord = []
    distMin = len(word) + 1
    for v in vocabulary:
        dist = hammingDistance(word, v)
        if dist < distMin:
            nearestWord = [v]
            distMin = dist
        if dist == distMin:
            nearestWord.append(v)

    if len(nearestWord) > 0:
        random.shuffle(nearestWord)
        return random.choice(nearestWord)

    return None


#---------------------------------------------------------------------------------------------------------------

def hammingDistance(word1, word2):
    dist = 0
    for l1, l2 in zip(word1, word2):
        if l1 != l2 :
            dist += 1
    return dist



#######################################################################################################
#   Specific methods part 2
#######################################################################################################


def getFitness_part2(word):
    reward = 0

    for letter in word:
        if letter in forbiddenLetters:
            return 0

    for letters, rp, bp in constraints:
        cptRightPos, cptBadPos = cptCorrectsChars(word, letters)
        
        if cptRightPos == rp or cptBadPos == bp:
           reward += 1

    return reward




#######################################################################################################
#   Specific methods part 3
#######################################################################################################


def getFurthestWord():
    distMax = 0
    for word in vocabulary:
        dist = len(set(word))
        if dist > distMax:
            distMax = dist
            furthestWord = [word]
        if dist == distMax:
            furthestWord.append(word)

    return random.choice(furthestWord)


#---------------------------------------------------------------------------------------------------------------

def getFitness_part3(word):
    reward = 0

    for letter in word:
        if letter in forbiddenLetters:
            return 0

    for letters, rp, bp in constraints:
        cptRightPos, cptBadPos = cptCorrectsChars(word, letters)

        if cptRightPos == rp: # the word contains exactly rp letters at the same position of the constraint word
            reward += (rp*2)**2
            if cptBadPos >= bp:
                reward += (bp*2)**2

        if cptRightPos > rp: # the word contains more than rp letters at the same position of the constraint word : good indication but not correct
            reward += rp # little penalization
            if cptBadPos >= bp:
                reward += bp

        if word  in vocabulary:
            reward += len(word)

    return reward


#---------------------------------------------------------------------------------------------------------------

def checkStagnation(pop, popFitnesses):
    global historyTot, cptGen

    tot = 0
    for i in range(len(popFitnesses)):
        tot += (i+1) * (popFitnesses[i]+1)

    if tot == historyTot:
        cptGen += 1
        if cptGen > 10:
            dist = 0
            for p in pop:
                dist += hammingDistance(pop[0], p)
            if dist != 0:
                dist = dist / len(pop)
            if dist < len(pop[0])/3:
                historyTot = 0
                cptGen = 0
                return getFurthestWord()
    else:
        historyTot = tot

    return None


#---------------------------------------------------------------------------------------------------------------

def getBestTry(eSet):
    bestFitness = -1
    bestWord = None
    random.shuffle(eSet)
    for word, fitness in eSet:
        if fitness > bestFitness:
            bestFitness = fitness
            bestWord = word
    return bestWord