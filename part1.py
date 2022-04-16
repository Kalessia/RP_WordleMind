import random

# Return an list of string from the dico with length of the word = wordSize
# Ex: var = getDico("dico.txt", 4)
def getDico(filename, wordSize):
    filteredDico = []
    with open(filename, "r") as f:
        dico = f.read().split("\n")

    for word in dico :
        n = len(word)
        if len(word) == wordSize:
            filteredDico.append(word)
    
    return filteredDico

# return an array with letter rightly placed, and at the wrong place [2, 1] / [colored_peg, white_peg]
def wordlemind(guess, secret):
    colored_peg=0
    white_peg=0
    
    flag = [1] * len(secret)

    for a in range(len(secret)):
        if (guess[a] == secret[a]):
            flag[a] = 0
            colored_peg += 1
    
    for a in range(len(secret)):
        if flag[a] == 1:
            for b in range(len(secret)):
                if guess[a] == secret[b] and flag[b] == 1:
                    white_peg += 1
                    flag[b] = 0

    return [colored_peg, white_peg]


# Tests
# print(wordlemind('jeck', 'keja'))
# print(getDico("dico.txt", 4))

from itertools import combinations
from time import process_time
import numpy as np
import logging
import sys
sys.setrecursionlimit(100000)


dico = []
rounds = 0
secret = ""
globalIndexes = []
currentIndexes = []


debug = False



# return string (word) from the dico
# remove: boolean => if true, remove the word from the dico
def getRandomWord(remove):
    global dico

    index = random.randint(0, len(dico) - 1)
    word = dico[index]
    if remove:
        dico.pop(index)
    return word

# Initialise globalIndexes variable. 
# Indexes of the letter we gonna freeze when searching for a new word
# ex: [ [0,1], [0,2], [1,2] ]
def initIndexes(x, y):
    global globalIndexes
    global secret

    # n=3 [0,1,2]
    arr = [i for i in range(len(secret))] 

    # [ [0,1], [0,2], [1,2] ]
    indexes = [list(i) for i in list(combinations(arr, x))]

    globalIndexes = indexes
    if (debug): print(globalIndexes) ###


# Find the next word to guess with the freeze indexes (ex: JACK with [0,1] can be JARE)
# Return the word if found, else return false
def findNextWord(guess):
    global globalIndexes
    global dico
    global currentIndexes

    # For each indexes group, try to find a word, otherwise go to the next indexes group
    for indexes in globalIndexes:
        word = findWordWithIndex(indexes, guess)
        if word != False:
            currentIndexes = indexes
            return word

    # Cannot find the word...
    return False


# Return a word with the freeze indexes
# Ex :
#           VV
#           JACK
# Result:   JAxx (can be JARE, JAME...)
def findWordWithIndex(indexes, guess):
    global secret
    global dico

    # Only for print purpose
    freezeArray = [' '] * len(secret)
    for i in indexes:
        freezeArray[i] = "V"
    freezeString = ""
    for i in freezeArray:
        freezeString += i

    

    for i in range(len(dico)):
        word = dico[i]
        lettersCorrect = 0
        for j in indexes:
            if word[j] != guess[j]:
                break
            else:
                lettersCorrect += 1
            if lettersCorrect == len(indexes):
                dico.pop(i)
                if (debug): print('Freeze:', freezeString) ###
                return word
    
    # This case should not be possible
    # print('No word found for those indexes: ', indexes, 'Change index...')
    return False


# Clean dico
# 
def cleanDico(guess, indexes):
    global dico

    wordIndexList = []

    for i in range(len(dico)):
        word = dico[i]
        lettersCorrect = 0
        for j in indexes:
            if word[j] != guess[j]:
                break
            else:
                lettersCorrect += 1
            if lettersCorrect == len(indexes):
                wordIndexList.append(i)
    
    for i in sorted(wordIndexList, reverse=True):
        del dico[i]


# Return the score of the word regarding x and y
# We are only taking care of x
def getScore(x, y):
    return x*1 + y*0


# Recursive function returning the word found with the number of rounds
# Ex: ['jack', 78]
def playRound(guess, results):
    global secret
    global dico
    global rounds
    global currentIndexes

    x,y = wordlemind(guess, secret)
    newScore = getScore(x, y)
    if (debug): print('Guess: ', guess, '(', x, ',', y, ') ==> ', newScore) ###

    rounds += 1

    # end
    if x == len(secret):
        return [guess, rounds]

    # Rerun with a random word. We prevent strating the main algo with x === 0
    if not bool(results) and x == 0:
        if (debug): print('Restart') ###
        return playRound(getRandomWord(True), {})

    # Add contraint (Forward checking)
    if bool(results) and newScore < results["score"]:
        cleanDico(guess, currentIndexes)

    # If a new guessed word have a better score, then we continue the algo with this new word and results (x, y and score)
    if not bool(results) or (newScore > results["score"]):
        if (debug):
            print('################################') ###
            print('### Best word: ', guess, ' ==> ', newScore, '###') ###
            print('################################') ###
        
        # Update results param with the new values
        results["word"] = guess
        results["score"] = newScore
        results["x"] = x
        results["y"] = y

        initIndexes(x, y)
    
    # Find a new word with the best word we found
    newGuess = findNextWord(results["word"])

    # This can't happen, but in case we have it...
    if newGuess == False:
        print('Cannot find the word...')
        return [0, 0]

    # Continue algo with the new guess word to test
    return playRound(newGuess, results)



def startGame(n):
    global dico
    global rounds
    global secret
    global globalIndexes

    if (debug): print('Start new game') ###

    # Define global variables
    dico = getDico("dico.txt", n)
    rounds = 0
    secret = getRandomWord(False)
    globalIndexes = []

    if (debug): print('Secret to find: ', secret) ###

    return playRound(getRandomWord(True), {})


# For statistics purpose

def statistics():
    roundsArray = []
    for n in range(4,9):
        for i in range(20):
            result = startGame(n)
            # print(result)
            if result[1] != 0:
                roundsArray.append(result[1])

        average = sum(roundsArray) / len(roundsArray)
        print('Average n=', n, ":", average, '20 iter')




t1_start = process_time()


# For single game, set debug = True for enable logs
print(startGame(4))

# For statistics, set debug = False for disabling logs
# statistics()


t1_stop = process_time()
print("Elapsed time in seconds:", t1_stop-t1_start)