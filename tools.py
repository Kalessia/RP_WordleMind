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
secretWord = ""
alreadyPlayed = []
constraints = []


#------------------------------------------------------------------------------------------------------
#   Tools
#------------------------------------------------------------------------------------------------------

def getVocabFromFile_setSecretWord(filename, wordSize):
    wordsList = []
    vocabulary_tmp = []
    with open(filename, "r") as f:
        wordsList = f.read().split("\n")

    for word in wordsList :
        if len(word) == wordSize:
            vocabulary_tmp.append(word.lower())
    
    global vocabulary, secretWord
    vocabulary = vocabulary_tmp
    secretWord = random.choice(vocabulary)
    return secretWord


#---------------------------------------------------------------------------------------------------------------

def getWord():
    return random.choice(vocabulary)


#---------------------------------------------------------------------------------------------------------------

def cptCorrectsChars(word, secretWord):

    cptRightPos = 0
    cptBadPos = 0

    secretWord = list(secretWord)
    word = list(word)

    tmp = []
    for i in range(len(word)):
        if word[i] == secretWord[i]:
            cptRightPos += 1
            tmp.append(word[i])
    
    for letter in tmp:
        word.remove(letter)
        secretWord.remove(letter)

    for letter in word:
        if letter in secretWord:
            cptBadPos += 1
            secretWord.remove(letter)

    return cptRightPos, cptBadPos


#---------------------------------------------------------------------------------------------------------------

def checkValidity(word):
    
    # The word must be a new attempt, never tried before
    if word in alreadyPlayed:
        return 0
    else:
        global alreadyPlayed
        alreadyPlayed.append(word)

    for letters, c in constraints:  # c = number of letters in 'letters' that must be in 'word_check'
        word_check = list(copy.deepcopy(word))
        cpt = 0
        for l in letters:
            if l in word_check:
                cpt += 1
                word_check.remove(l)
                if cpt == c:
                    reward += 1 # reward is the number of respected constraints
                    break

    buildConstraintsRules(word)
    return True
    

#---------------------------------------------------------------------------------------------------------------

def buildConstraintsRules(word):
    
    cptRightPos, cptBadPos = cptCorrectsChars(word, secretWord)

    global constraints
    constraints.append([list(word), cptRightPos + cptBadPos])

    print("Constraints :", constraints)

