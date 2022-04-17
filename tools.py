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
forbiddenLetters = []
alreadySeen = []
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
    reward = 0

    # The word must be a new attempt, never tried before
    global alreadySeen
    if word in alreadySeen or word not in vocabulary:
        return 0
    else:
        alreadySeen.append(word)
        buildConstraintsRules(word)

    for letters, bp, mp in constraints:  # c = number of letters in 'letters' that must be in 'word_check'
        word_check = list(copy.deepcopy(word))
        cpt_bp = 0
        cpt_mp = 0
        tmp = []

        for i in range(len(letters)):
            if letters[i] == word_check[i]:
                cpt_bp += 1
                tmp.append(letters[i])

        if cpt_bp == bp: # the word contains exactly bp letters at the same position of the constraint word
            reward += (bp**2) * 2
            letter_check = copy.deepcopy(word_check)
            for letter in tmp:
                word_check.remove(letter)
                letter_check.remove(letter)
            for letter in letter_check:
                if letter in word_check:
                    cpt_mp += 1
                    word_check.remove(letter)
                    if cpt_mp == mp:
                        reward += mp**2
                        break

        if cpt_bp > bp: # the word contains more than bp letters at the same position of the constraint word : good indication but not correct
            reward += bp # little penalization
            for letter in letters:
                if letter in word_check:
                    cpt_mp += 1
                    word_check.remove(letter)
                    if cpt_mp == mp:
                        reward += mp**2
                        break

    return reward
    

#---------------------------------------------------------------------------------------------------------------

def buildConstraintsRules(word):
    
    cptRightPos, cptBadPos = cptCorrectsChars(word, secretWord)
    w = list(word)

    global constraints
    if cptRightPos + cptBadPos > 0:
        constraints.append([w, cptRightPos, cptBadPos])
    else:
        for letter in w:
            if w not in forbiddenLetters:
                forbiddenLetters.append(letter)


#---------------------------------------------------------------------------------------------------------------

def isForbiddenLetter(letter):
    if letter in forbiddenLetters:
        return True
    return False
