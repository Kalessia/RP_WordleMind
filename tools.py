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
import copy


#------------------------------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------------------------------

vocabulary = None
forbiddenLetters = []
alreadyPlayed = []
constraints = []            # collects informations about the previous attempts


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

    secretWord_check = list(secretWord)
    word_check = list(word)

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

def getFitness(word):
    reward = 0

    if word not in vocabulary:
        return 0

    for letter in word:
        if letter in forbiddenLetters:
            return 0

    for letters, rp, bp in constraints:
        word_check = list(copy.deepcopy(word))
        letters_check = copy.deepcopy(letters)

        cptRightPos = 0
        cptBadPos = 0
        tmp = []

        for pos in range(len(letters_check)):
            if letters_check[pos] == word_check[pos]:
                cptRightPos += 1
                tmp.append(letters_check[pos])

        if len(tmp) > 0:
            for letter in tmp:
                word_check.remove(letter)
                letters_check.remove(letter)
 
        for letter in letters_check:
            if letter in word_check:
                cptBadPos += 1
                word_check.remove(letter)


        if cptRightPos == rp: # the word contains exactly rp letters at the same position of the constraint word
            reward += (rp*2)**2
            if cptBadPos >= bp:
                reward += (bp*2)**2

        if cptRightPos > rp: # the word contains more than rp letters at the same position of the constraint word : good indication but not correct
            reward += rp # little penalization
            if cptBadPos >= bp:
                reward += bp

    return reward
    

#---------------------------------------------------------------------------------------------------------------

def buildConstraintsRules(word, secretWord):
    
    global alreadyPlayed
    alreadyPlayed.append(word)

    cptRightPos, cptBadPos = cptCorrectsChars(word, secretWord)
    w = list(word)

    global constraints
    if cptRightPos + cptBadPos > 0:
        constraints.append([w, cptRightPos, cptBadPos])
    else:
        for letter in w:
            if not isForbiddenLetter(letter):
                forbiddenLetters.append(letter)
    
    return constraints


#---------------------------------------------------------------------------------------------------------------

def isForbiddenLetter(letter):
    if letter in forbiddenLetters:
        return True
    return False


#---------------------------------------------------------------------------------------------------------------

def respectsAllContraints(word):

    if word in alreadyPlayed:
        return False

    for letter in word:
        if letter in forbiddenLetters:
            return False


    for letters, rp, bp in constraints:
        word_check = list(copy.deepcopy(word))
        letters_check = copy.deepcopy(letters)

        cptRightPos = 0
        cptBadPos = 0
        tmp = []

        for pos in range(len(letters_check)):
            if letters_check[pos] == word_check[pos]:
                cptRightPos += 1
                tmp.append(letters_check[pos])

        if len(tmp) > 0:
            for letter in tmp:
                word_check.remove(letter)
                letters_check.remove(letter)
 
        for letter in letters_check:
            if letter in word_check:
                cptBadPos += 1
                word_check.remove(letter)
        
        if cptRightPos != rp or cptBadPos != bp:
            return False
    
    return True

