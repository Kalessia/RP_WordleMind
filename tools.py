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


#------------------------------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------------------------------

vocabulary = None



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
            vocabulary_tmp.append(word)
    
    global vocabulary
    vocabulary = vocabulary_tmp


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

def isWordConsistent(word):
    return True
    

#---------------------------------------------------------------------------------------------------------------

def isWordValid(word):
    if word in vocabulary and isWordConsistent(word):
        return True
    return False
