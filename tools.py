
from inspect import modulesbyfile


def acquisirVocabDepuisFichier(nomFichier):
    """Retourne un dictionnaire ayant comme clés les différents longueurs des mots 
    et comme valeurs un tableau contenant les mots de telle longueur, crée à partir d'un fichier texte contenant des mots

    :param nomFichier : fichier texte contenant les mots du vocabulaire
    """

    listeMots = []
    vocabulaire = {}
    with open(nomFichier, "r") as f:
        listeMots = f.read().split("\n")

    for mot in listeMots :
        n = len(mot)
        if n in list(vocabulaire.keys()):
            vocabulaire[n].append(mot)
        else:
            vocabulaire[n] = [mot]
    
    return vocabulaire


#---------------------------------------------------------------------------------------------------------------

def cptCaracteresCorrects(motPropose, motSecret):
    """Retorune le nombre de caracteres corrects bien placés et le nombre de caractères corrects mal placés

    :param motPropose : mot proposée par le joueur
    :param motSecret : mot à déviner
    """
    cptCorrectsBienPlaces = 0
    cptCorrectsMalPlaces = 0

    motSecret = list(motSecret.lower())
    motPropose = list(motPropose.lower())

    tmp = []
    for i in range(len(motPropose)):
        if motPropose[i] == motSecret[i]:
            cptCorrectsBienPlaces += 1
            tmp.append(motPropose[i])
    
    for lettre in tmp:
        motPropose.remove(lettre)
        motSecret.remove(lettre)

    for lettre in motPropose:
        if lettre in motSecret:
            cptCorrectsMalPlaces += 1
            motSecret.remove(lettre)

    return cptCorrectsBienPlaces, cptCorrectsMalPlaces


#---------------------------------------------------------------------------------------------------------------

def estCompatibile(motPropose, motSecret, listeLettresInterdites):
    """Retourne un booléan :
        - true, si le motPropose est compatible avec les informations obtenues avec les essais précedents
        - false, sinon.
    
    :param motPropose : mot proposée par le joueur
    :param motSecret : mot à déviner
    :param listeLettresInterdites : liste de lettres qui ne doivent pas apparaitre dans motPropose, car éliminées lors des essais précédents
    """

    for c in motPropose:
        if c in listeLettresInterdites:
            return False
    
    return True

    #---------------------------------------------------------------------------------------------------------------
    # tools for part1

    