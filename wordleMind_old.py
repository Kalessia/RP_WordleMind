import tools
from partie2 import algorithmeGenetique



nomFichier = "dico.txt"
vocabulaire = tools.acquisirVocabDepuisFichier(nomFichier)


motSecret = "dette"
motPropose = "tarte"
cptCorrectsBienPlaces, cptCorrectsMalPlaces = tools.cptCaracteresCorrects(motSecret, motPropose)
print(cptCorrectsBienPlaces, cptCorrectsMalPlaces)

a = algorithmeGenetique()
#prochainMot = a.

