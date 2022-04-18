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


def plotMeanTime(tab_n, tab_meanTime, nbIterations, plotfile = None):
    x = tab_n
    y = tab_meanTime


    plt.figure()

    plt.suptitle(f"Temps moyen de résolution en fonction de la taille du mot")
    plt.title(f"sur {nbIterations} itérations")
    plt.xlabel("n : taille du mot")
    plt.ylabel("temps (s)")
    plt.plot(x, y)

    if plotfile != None:
        plt.savefig(plotfile + "_tempsMoyen.pdf", transparent = True)

    plt.show()


#------------------------------------------------------------------------------------------------------

def plotNbAttempts(tab_n, tab_nbAttempts, nbIterations, plotfile = None):
    x = tab_n
    z = tab_nbAttempts

    plt.figure()

    plt.suptitle(f"Nombre moyen de essais en fonction de la taille du mot")
    plt.title(f"sur {nbIterations} itérations")
    plt.xlabel("n : taille du mot")
    plt.ylabel("nombre d'essais")
    plt.plot(x, z)

    if plotfile != None:
        plt.savefig(plotfile + "_nbEssaisMoyen.pdf", transparent = True)

    plt.show()


#------------------------------------------------------------------------------------------------------

def plotSuccesses(tab_n, tabSuccesses, nbIterations, plotfile = None):
    x = tab_n
    y = tabSuccesses


    plt.figure()

    plt.suptitle(f"Pourcentage des victoires")
    plt.title(f"sur {nbIterations} itérations")
    plt.xlabel("n : taille du mot")
    plt.ylabel("% victoires")
    plt.plot(x, y)

    if plotfile != None:
        plt.savefig(plotfile + "_nbSuccesses.pdf", transparent = True)

    plt.show()