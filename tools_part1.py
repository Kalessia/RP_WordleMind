# tools for part 1

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

# returns an array with letter rightly placed, and at the wrong place [2, 1] / [colored_peg, white_peg]
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
    