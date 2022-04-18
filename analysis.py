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

import matplotlib.pyplot as plt


#------------------------------------------------------------------------------------------------------
#   Parameters
#------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------
#   Analysis
#------------------------------------------------------------------------------------------------------


def plotResults(tab_n, tab_tempsMoyen, tab_nbEssais, filename = None):
    x = tab_n
    y = tab_tempsMoyen
    z = tab_nbEssais


    plt.figure()

    plt.title("Temps moyen de résolution en fonction de la taille du mot")
    plt.xlabel("n")
    plt.ylabel("temps")
    plt.plot(x, y)
    plt.show()

    if filename != None:
        plt.savefig(filename + "_tempsMoyen", transparent = True)


    plt.title("Nombre moyen de essais en fonction de la taille du mot")
    plt.xlabel("n")
    plt.ylabel("nb essais")
    plt.plot(x, z)
    plt.show()

    if filename != None:
        plt.savefig(filename + "_nbEssaisMoyen", transparent = True)
